
from infra.databases.vector_database import VectorStore

TEST_DB = "tests/infra/databases/vector_db/mock_db"



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
store = VectorStore(TEST_DB,collection_name="test")


def test_add_chunks():
    assert store.add_chunks(MOCK_CHUNKS,source="test_chunks") == 4


def test_query():
    for query, doc in zip(MOCK_QUERIES,MOCK_CHUNKS):
        assert store.search(query,k=1,source="test_chunks")[0]["text"] == doc

def mock_test():
    assert True