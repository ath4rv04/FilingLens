from __future__ import annotations


from filinglens.embeddings.embedder import EmbeddingService
from filinglens.models import RetrievalResult
from filinglens.vectorstore import QdrantVectorStore
from filinglens.embeddings.embedder import (
    get_embedding_service,
)


class DenseRetriever:
    def __init__(
        self,
        *,
        vector_store: QdrantVectorStore,
        embedder: EmbeddingService | None = None,
    ) -> None:

        self.embedder = embedder or get_embedding_service()
        self.vector_store = vector_store

    def search(self, query: str, *, top_k: int = 5, filters: dict | None = None) -> list[RetrievalResult]:
        query_vector = self.embedder.embed(
            query,
            show_progress_bar=False,
        )[0]
        results = self.vector_store.search(query_vector, top_k=top_k, filters=filters)

        return [
            RetrievalResult(
                chunk=result.chunk,
                score=result.score,
                source="dense",
            )
            for result in results
        ]
