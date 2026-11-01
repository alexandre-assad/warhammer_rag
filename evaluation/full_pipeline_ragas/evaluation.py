import json
import os
import time
import uuid
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from google import genai
from ragas import EvaluationDataset, RunConfig, SingleTurnSample, evaluate
from ragas.llms import llm_factory
from ragas.metrics import (
    FactualCorrectness,
    Faithfulness,
    LLMContextPrecisionWithReference,
    LLMContextRecall,
)

from app.graph import get_app

load_dotenv()

TESTSET = Path("evaluation/data/processed/testset_full_v1.csv")
CHECKPOINT = Path("evaluation/results/agent_runs.jsonl")
OUTPUT_FILE = Path("evaluation/results/full_pipeline_eval_results.csv")
JUDGE_MODEL = "gemini-3.5-flash"
N_ROWS = None  # None = all the testset

ANSWER_KEY, DOCUMENTS_KEY, SQL_KEY = "answer", "chunks", "sql_rows"


def build_judge_llm():
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
    return llm_factory(JUDGE_MODEL, provider="google", client=client)


def run_rag(app, question: str) -> tuple[str, list[str]]:
    config = {"configurable": {"thread_id": str(uuid.uuid4())}}
    state = app.invoke(
        {"query": question, "messages": [{"role": "user", "content": question}]},
        config,
    )
    contexts = [
        c["text"] if isinstance(c, dict) else str(c)
        for c in state.get(DOCUMENTS_KEY, [])
    ]
    if state.get(SQL_KEY):
        contexts.append(str(state[SQL_KEY]))
    return state[ANSWER_KEY], contexts


def collect_runs(app, test_set: pd.DataFrame) -> list[dict]:
    """Query the agent once per question; resumable thanks to the JSONL checkpoint."""
    CHECKPOINT.parent.mkdir(parents=True, exist_ok=True)
    done = {}
    if CHECKPOINT.exists():
        with CHECKPOINT.open(encoding="utf-8") as f:
            done = {r["question"]: r for r in map(json.loads, f)}
    with CHECKPOINT.open("a", encoding="utf-8") as f:
        for _, ex in test_set.iterrows():
            q = ex["question"]
            if q not in done:
                t0 = time.perf_counter()
                response, contexts = run_rag(app, q)
                done[q] = {
                    "question": q,
                    "reference": ex["reference_answer"],
                    "category": ex["category"],
                    "response": response,
                    "contexts": contexts,
                    "latency_s": round(time.perf_counter() - t0, 2),
                }
                f.write(json.dumps(done[q], ensure_ascii=False) + "\n")
                f.flush()
    return [done[q] for q in test_set["question"]]


def full_evaluation() -> None:
    test_set = pd.read_csv(TESTSET).dropna(subset=["question"])
    test_set.drop(columns=["decision", "comment"], inplace=True)

    if N_ROWS:
        test_set = test_set.sample(N_ROWS, random_state=0)

    records = collect_runs(get_app(), test_set)

    scored = [r for r in records if r["category"] != "out_of_scope"]
    samples = [
        SingleTurnSample(
            user_input=r["question"],
            response=r["response"],
            retrieved_contexts=r["contexts"],
            reference=r["reference"],
        )
        for r in scored
    ]

    judge = build_judge_llm()
    metrics = [
        Faithfulness(llm=judge),
        FactualCorrectness(llm=judge),
        LLMContextPrecisionWithReference(llm=judge),
        LLMContextRecall(llm=judge),
    ]
    result = evaluate(
        dataset=EvaluationDataset(samples=samples),
        metrics=metrics,
        run_config=RunConfig(max_workers=2, timeout=300),
    )

    df = result.to_pandas()
    df["category"] = [r["category"] for r in scored]
    df["latency_s"] = [r["latency_s"] for r in scored]
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)

    print(df.groupby("category").mean(numeric_only=True))
    print(f"Per-question scores saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    full_evaluation()
