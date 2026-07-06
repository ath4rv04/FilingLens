from filinglens.embeddings.embedder import EmbeddingService
from filinglens.vectorstore.qdrant_store import QdrantVectorStore
from filinglens.indexing.loader import load_chunks
from filinglens.settings import PROCESSED_DATA_DIR, QDRANT_COLLECTION


class IndexingService:
    def __init__(self, embedder: EmbeddingService, vector_store: QdrantVectorStore):
        self.embedder = embedder
        self.vector_store = vector_store

    def index_company_year(self, company: str, year: str) -> tuple[int, str]:
        path = PROCESSED_DATA_DIR / company / year / "chunks"
        if not path.exists():
            raise FileNotFoundError(f"Chunks directory not found for {company} {year}")

        chunks = load_chunks(path)
        texts = [chunk.text for chunk in chunks]

        embeddings = self.embedder.embed(texts)

        if not self.vector_store.client.collection_exists(QDRANT_COLLECTION):
            self.vector_store.create_collection()

        self.vector_store.upload_chunks(chunks, embeddings)

        return len(chunks), self.vector_store.collection_name
