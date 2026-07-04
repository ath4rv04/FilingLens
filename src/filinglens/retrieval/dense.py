from __future__ import annotations

from typing import Any

from filinglens.embeddings.embedder import EmbeddingService
from filinglens.retrieval.models import RetrievalResult
from filinglens.vectorstore import QdrantVectorStore


class DenseRetriever:
    """Dense retriever backed by Qdrant."""

    def __init__(
        self,
        *,
        embedder: EmbeddingService,
        vector_store: QdrantVectorStore,
    ) -> None:
        self.embedder = embedder
        self.vector_store = vector_store

    def search(self, query: str, *, top_k: int = 5) -> list[RetrievalResult]:
        query_vector = self.embedder.embed(query)
        results = self.vector_store.search(query_vector, top_k=top_k)

        return [
            RetrievalResult(
                id=result.id,
                score=result.score,
                payload=self._payload(result.payload, result.id),
                source="dense",
            )
            for result in results
        ]

    @staticmethod
    def _payload(payload: dict[str, Any], fallback_id: str) -> dict[str, Any]:
        normalized = dict(payload)
        normalized.setdefault("chunk_id", normalized.get("id", fallback_id))
        return normalized
