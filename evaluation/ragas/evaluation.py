import re

import pandas as pd

from domain.reranker.reranker import Reranker
from infra.databases.vector_database import VectorStore


def _words(text: str) -> list[str]:
    return re.findall(r"\w+", text.lower())

def _matches(chunk, reference) -> bool:
    chunk_text = chunk.get('text', '')
    ref_w = set(_words(reference))
    chunk_w = set(_words(chunk_text))
    
    if not ref_w or not chunk_w:
        return False
        
    common_words = len(ref_w & chunk_w)
    recall_ratio = common_words / len(ref_w)
    precision_ratio = common_words / len(chunk_w)

    return recall_ratio >= 0.3 or precision_ratio >= 0.3


def evaluate_chunks(retrieved, references, k=5) -> dict[str, float]:
    hits, recalls, mrrs, aps = [], [], [], []

    for chunks, refs in zip(retrieved, references):

        if isinstance(refs, str):
            refs = refs.split('--- passage suivant ---')
        top = chunks[:k]

        relevant = [any(_matches(c, r) for r in refs) for c in top]

        hits.append(float(any(relevant)))
        recalls.append(sum(any(_matches(c, r) for c in top) for r in refs) / len(refs))
        mrrs.append(next((1 / rank for rank, ok in enumerate(relevant, 1) if ok), 0.0))

        found, total = 0, 0.0
        for rank, ok in enumerate(relevant, 1):
            if ok:
                found += 1
                total += found / rank
        aps.append(total / found if found else 0.0)

    mean = lambda values: sum(values) / len(values)
    scores = {f"hit@{k}": mean(hits), f"recall@{k}": mean(recalls),
              f"mrr@{k}": mean(mrrs), f"map@{k}": mean(aps)}
    print("  ".join(f"{name}={value:.3f}" for name, value in scores.items()))
    return scores


def evaluation(k:int = 5, chunk_size: int = 500) -> dict[str, float]:
    vector_store = VectorStore()
    vector_store.index_markdown(chunk_size)
    reranker = Reranker()
    data = pd.read_csv('evaluation/data/processed/testset_v1.csv')
    data.drop(columns=['decision', 'section', 'comment'], inplace=True)
    data.dropna(inplace=True)
 
    retrieved = []
    for _, row in data.iterrows():
        retrieved.append(reranker.rerank(row['question'], vector_store.search(row['question']), k))
    
    return evaluate_chunks(retrieved, data['reference_contexts'])

