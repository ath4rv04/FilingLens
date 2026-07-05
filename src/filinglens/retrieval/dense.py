from __future__ import annotations

from typing import Any

from filinglens.embeddings.embedder import EmbeddingService
from filinglens.retrieval.models import RetrievalResult
from filinglens.vectorstore import QdrantVectorStore
from filinglens.embeddings.embedder import (
    EmbeddingService,
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

    def search(self, query: str, *, top_k: int = 5) -> list[RetrievalResult]:
        query_vector = self.embedder.embed(
            query,
            show_progress_bar=False,
        )[0]
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
