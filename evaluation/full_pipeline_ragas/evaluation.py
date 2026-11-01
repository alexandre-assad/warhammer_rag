import uuid
from pathlib import Path
from dotenv import load_dotenv

import pandas as pd 

from app.graph import get_app

from ragas import EvaluationDataset, SingleTurnSample, evaluate
from ragas.llms import LangchainLLMWrapper
from ragas.metrics import (
    FactualCorrectness,
    Faithfulness,
    LLMContextPrecisionWithoutReference,
    LLMContextPrecisionWithReference,
    LLMContextRecall,
)

import google.generativeai as genai

load_dotenv()

test_set = pd.read_csv("evaluation/data/processed/testset_v1.csv")
OUTPUT_FILE = Path("evaluation/results/full_pipeline_eval_results.csv")

# Keys of the final state returned by app.invoke(...). Adapt to your graph.
ANSWER_KEY = "answer"
DOCUMENTS_KEY = "chunks"  
SQL_KEY = "sql_rows"  





def build_judge_llm():
    raise NotImplementedError("return a LangchainLLMWrapper(chat_model) here")


def run_rag(app, question: str) -> tuple[str, list[str]]:
    """One independent conversation round: fresh thread, no memory between questions."""
    config = {"configurable": {"thread_id": str(uuid.uuid4())}}
    state = app.invoke({"query": question}, config)

    contexts = [chunk for chunk in state.get(DOCUMENTS_KEY,[])]
    if state.get(SQL_KEY):
        contexts.append(str(state[SQL_KEY]))
    return state[ANSWER_KEY], contexts


def main() -> None:
    app = get_app()
    judge = build_judge_llm()

    samples = []
    for _, example  in test_set.iterrows():
        query = example["question"]
        response, contexts = run_rag(app, query)
        samples.append(
            SingleTurnSample(
                user_input=query,
                response=response,
                retrieved_contexts=contexts,
                reference=example["reference_answer"],
            )
        )

    

    metrics = [
                Faithfulness(llm=judge),
                FactualCorrectness(llm=judge),
                LLMContextPrecisionWithReference(llm=judge),
                LLMContextRecall(llm=judge),
            ]

    result = evaluate(dataset=EvaluationDataset(samples=samples), metrics=metrics)

    df = result.to_pandas()
    df.to_csv(OUTPUT_FILE, index=False)
    print(result)  # mean score per metric
    print(f"Per-question scores saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()