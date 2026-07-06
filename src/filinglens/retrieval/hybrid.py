from __future__ import annotations

from filinglens.retrieval.bm25 import BM25Retriever
from filinglens.retrieval.dense import DenseRetriever
from filinglens.models import RetrievalResult
from filinglens.retrieval.rrf import reciprocal_rank_fusion


class HybridRetriever:
    """Combines dense semantic retrieval with sparse BM25 retrieval."""

    def __init__(
        self,
        *,
        dense_retriever: DenseRetriever,
        bm25_retriever: BM25Retriever,
        fusion_k: int = 60,
    ) -> None:
        self.dense_retriever = dense_retriever
        self.bm25_retriever = bm25_retriever
        self.fusion_k = fusion_k

    def search(
        self,
        query: str,
        *,
        top_k: int = 5,
        candidate_k: int | None = None,
    ) -> list[RetrievalResult]:
        candidate_k = candidate_k or max(top_k * 4, top_k)
        dense_results = self.dense_retriever.search(query, top_k=candidate_k)
        bm25_results = self.bm25_retriever.search(query, top_k=candidate_k)

        return reciprocal_rank_fusion(
            [dense_results, bm25_results],
            top_k=top_k,
            k=self.fusion_k,
        )
