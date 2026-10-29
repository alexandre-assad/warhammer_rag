from domain.reranker.reranker import Reranker

MOCK_CHUNKS = [
    "Le RAG c'est trop cool",
    "A keyword counter on a permanent or on a card in a zone other than the battlefield causes that object to gain that keyword.",
    "Each activated ability of a planeswalker has a loyalty symbol in its cost. Positive loyalty symbols point upward and feature a plus sign followed by a number",
    "Some effects put tokens onto the battlefield. A token is a marker used to represent any permanent that isn't represented by a card"
]


MOCK_QUERIES  = [
    "Que penses tu du RAG?",
    "How does a keyword counter act when a permanent changes zone?",
    "How are planeswalker abilities displayed?",
    "What is a token?"
]

MOCK_CHUNKS_DICT = [{"text":chunk} for chunk in MOCK_CHUNKS]

reranker = Reranker()


def test_rerank():
    top_k = 5
    ranked = reranker.rerank(MOCK_QUERIES[0],MOCK_CHUNKS_DICT,top_k= top_k)
    assert len(ranked) == min(top_k,len(MOCK_CHUNKS_DICT))
    assert ranked[0]["text"] == MOCK_CHUNKS[0]



