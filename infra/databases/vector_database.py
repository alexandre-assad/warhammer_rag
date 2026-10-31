from pathlib import Path
import sys
import chromadb
from chromadb.utils import embedding_functions
from domain.text_processing.chunking import get_chunks_from_text, mardown_file_read

DB_PATH = "data/processed/vector_db"  # folder where Chroma persists its data
COLLECTION_NAME = "WARHAMMER_RULES"
MD_FILE = "data/processed/pdf/Core Rules.md"
# MODEL_NAME = "intfloat/multilingual-e5-small"
MODEL_NAME = "./model_e5_local"


class VectorStore:
    def __init__(
        self,
        db_path: str = DB_PATH,
        collection_name: str = COLLECTION_NAME,
        model_name: str = MODEL_NAME,
        embedding_function=None,
    ):
        # Persistent client: data is written to disk and survives restarts.
        self.client = chromadb.PersistentClient(path=db_path)

        # Chroma calls this function to embed documents on add/upsert and
        # queries on search, so both always use the same model.
        self.embedding_function = embedding_function or (
            embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name=model_name
            )
        )

        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedding_function,
            # Sentence-BERT models are trained for cosine similarity.
            metadata={"hnsw:space": "cosine"},
        )

    def add_chunks(self, chunks: list[str], source: str, batch_size: int = 256) -> int:
        """Embed and store chunks. Re-indexing the same source overwrites it."""
        # Remove old chunks of this source so a shorter re-parse leaves no leftovers.
        self.collection.delete(where={"source": source})

        for start in range(0, len(chunks), batch_size):
            batch = chunks[start : start + batch_size]
            self.collection.upsert(
                ids=[f"{source}::{start + i}" for i in range(len(batch))],
                documents=batch,
                metadatas=[
                    {"source": source, "chunk_index": start + i}
                    for i in range(len(batch))
                ],
            )
        return len(chunks)

    def index_markdown(self, chunk_size:int = 500, file_path: Path = Path(MD_FILE)) -> int:
        text = mardown_file_read(file_path)
        chunks = get_chunks_from_text(text, chunk_size)
        return self.add_chunks(chunks, source=Path(file_path).name)

    def search(self, query: str, k: int = 5, source: str | None = None) -> list[dict]:
        result = self.collection.query(
            query_texts=[query],
            n_results=k,
            where={"source": source} if source else None,
        )
        return [
            {"text": doc, "distance": dist, **meta}
            for doc, dist, meta in zip(
                result.get("documents", [None])[0],
                result.get("distances", [None])[0],
                result.get("metadatas", [None])[0],
            )
        ]

    def count(self) -> int:
        return self.collection.count()


if __name__ == "__main__":
    
    if not Path(DB_PATH).exists():
        print("Creating the vector_db folder")
        Path(DB_PATH).mkdir()

    store = VectorStore()
    n = store.index_markdown()
    print("okay")
    print(f"Indexed {n} chunks, collection size: {store.count()}")