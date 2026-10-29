from langgraph.graph import StateGraph, MessagesState, START, END
from domain.reranker.reranker import Reranker
from infra.databases.vector_database import VectorStore
from typing import TypedDict

class InputState(TypedDict):
    query: str



class RetrieveState(TypedDict):
    chunks:list[dict]


class OutputState(TypedDict):

    answer:str


class GenerationState(TypedDict):
    chunks: list[dict]
    rows: list[str]


RULES_RETRIEVAL_NODE = "rules_retrieval"
T2SQL_RETRIEVAL_NODE = "sql_retrieval"
RERANK_NODE = "rerank"
GENERATION_NODE = "generation"
store = VectorStore()
reranker = Reranker()



def rules_retrieval(input:InputState)-> RetrieveState:
    return { "chunks" : store.search(input["query"])}

def rerank(input:RetrieveState) -> RetrieveState:
    return {"chunks" :reranker.rerank(input["query"],input["chunks"])}

def sql_retrieval(input_state):
    return {"sql_rows" : ["s","q","l"]}

def pick_retrieval_method(input:InputState)-> list[str]:
    #TODO : Implement picking logic 
    return [RULES_RETRIEVAL_NODE,T2SQL_RETRIEVAL_NODE]
def mock_lm(input: GenerationState):
    #TODO: Implement LLM interaction 
    return {"answer" : input["query"]}


graph = StateGraph(MessagesState)
graph.add_node(RULES_RETRIEVAL_NODE,rules_retrieval)
graph.add_node(T2SQL_RETRIEVAL_NODE,sql_retrieval)
graph.add_conditional_edges(START,pick_retrieval_method, [RULES_RETRIEVAL_NODE,T2SQL_RETRIEVAL_NODE])
graph.add_node(RERANK_NODE,rerank)
graph.add_edge(RULES_RETRIEVAL_NODE,RERANK_NODE)
graph.add_node(GENERATION_NODE,mock_lm)
graph.add_edge(T2SQL_RETRIEVAL_NODE,GENERATION_NODE)
graph.add_edge(RERANK_NODE,GENERATION_NODE)
graph.add_edge(GENERATION_NODE,END)


def get_app():
    return graph.compile()
