import os
from pathlib import Path
from typing import Annotated, TypedDict

import google.generativeai as genai
from dotenv import load_dotenv
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph

from domain.agent.rate_limiter import call_with_retry
from domain.agent.text_to_sql import generate_sql
from domain.reranker.reranker import Reranker
from infra.databases.vector_database import DB_PATH, VectorStore

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def add_list(messages, new_messages):
    if isinstance(new_messages, list):
        return messages + new_messages

    return messages + [new_messages]


"""For now the query is the new user message and messages contains the whole history.
This might change to support query rewriting (passing almost all the conv history to the retriever)"""


class AgentState(TypedDict):
    query: str
    messages: Annotated[list, add_list]
    chunks: list[dict]
    sql_rows: list[str]
    answer: str


RULES_RETRIEVAL_NODE = "rules_retrieval"
T2SQL_RETRIEVAL_NODE = "sql_retrieval"
RERANK_NODE = "rerank"
GENERATION_NODE = "generation"

if not Path(DB_PATH).exists():
    Path(DB_PATH).mkdir()

store = VectorStore()
reranker = Reranker()

if store.count() == 0:
    n = store.index_markdown()
    print(f"Indexed {n} chunks, collection size: {store.count()}")


def rules_retrieval(input: AgentState) -> dict:
    return {"chunks": reranker.rerank(input["query"], store.search(input["query"]), 3)}


def sql_retrieval(input: AgentState) -> dict:
    return {"sql_rows": generate_sql(input["query"])}


def pick_retrieval_method(input: AgentState) -> list[str]:
    user_query = input["query"]

    prompt = f"""You are an intelligent router for a miniature wargame assistant.
Analyze this question: "{user_query}"

Where should the information be searched?
1. GLOBAL RULES (return "rag"): game phases, terrain, line of sight, core rules, how to play.
2. STATISTICS (return "sql"): unit characteristics, factions, detachments, weapons, abilities (datasheets), keywords.
3. BOTH (return "both"): if the question mixes a global rule and a specific unit, or if it is ambiguous.

Return ONLY "rag", "sql", or "both". No punctuation, no explanations."""

    try:
        model = genai.GenerativeModel(model_name="gemini-3.5-flash")
        response = call_with_retry(model.generate_content, prompt)
        if not response or not response.text:
            return ["rules_retrieval", "sql_retrieval"]

        decision = response.text.strip().lower()
        print(f"Routing decision : {decision}")

        if "both" in decision:
            return ["rules_retrieval", "sql_retrieval"]
        elif "sql" in decision:
            return ["sql_retrieval"]
        else:
            return ["rules_retrieval"]

    except Exception as e:
        print(f"Routing error : {e}")
        return ["rules_retrieval", "sql_retrieval"]


def generation(input: AgentState):

    chunks = input.get("chunks", [])
    sql_rows = input.get("sql_rows", [])

    context_text = "\n\n".join([c.get("text", "") for c in chunks])

    system_prompt = f"""You are an expert assistant on the Warhammer game rules.
Use ONLY the following information to answer the question.

RULES DOCUMENTS:
{context_text}

STATISTICAL DATA (SQL):
{sql_rows}

If the answer is not found in this information, state that you do not know.
"""

    gemini_messages = [
        {
            "role": "model" if msg["role"] == "assistant" else "user",
            "parts": [msg["content"]],
        }
        for msg in input["messages"]
    ]

    if gemini_messages and gemini_messages[-1]["role"] == "model":
        gemini_messages.append({"role": "user", "parts": ["Please answer my request."]})

    model = genai.GenerativeModel(
        model_name="gemini-3.5-flash", system_instruction=system_prompt
    )
    response = call_with_retry(model.generate_content, gemini_messages)

    return {
        "answer": response.text,
        "messages": {"role": "assistant", "content": response.text},
    }


graph = StateGraph(AgentState)
graph.add_node(RULES_RETRIEVAL_NODE, rules_retrieval)
graph.add_node(T2SQL_RETRIEVAL_NODE, sql_retrieval)
graph.add_node(GENERATION_NODE, generation)

graph.add_conditional_edges(
    START, pick_retrieval_method, [RULES_RETRIEVAL_NODE, T2SQL_RETRIEVAL_NODE]
)

graph.add_edge(T2SQL_RETRIEVAL_NODE, GENERATION_NODE)
graph.add_edge(RULES_RETRIEVAL_NODE, GENERATION_NODE)
graph.add_edge(GENERATION_NODE, END)

checkpointer = InMemorySaver()


def get_app():
    return graph.compile(checkpointer=checkpointer)


app = get_app()
config = {"configurable": {"thread_id": "session_test_02"}}


# To actually keep history, keep session based on thread-id, using:
# config = {"configurable": {"thread_id": thread_id}}
