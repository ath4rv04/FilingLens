from __future__ import annotations

from collections import Counter
from math import log
import re
from typing import Any

from filinglens.models.document_chunk import DocumentChunk
from filinglens.models import RetrievalResult

TOKEN_PATTERN = re.compile(r"[a-zA-Z0-9]+")


from filinglens.retrieval.filtering import normalize_filters
from filinglens.utils.logging import get_logger

logger = get_logger(__name__)

class BM25Retriever:
    """In-memory BM25 retriever for filing chunks."""

    def __init__(
        self,
        chunks: list[DocumentChunk | dict[str, Any]],
        *,
        k1: float = 1.5,
        b: float = 0.75,
    ) -> None:
        self.k1 = k1
        self.b = b
        self.chunks = [
            chunk if isinstance(chunk, DocumentChunk) else DocumentChunk(**chunk)
            for chunk in chunks
        ]
        
        if not self.chunks:
            logger.warning("[!] BM25 Corpus initialized with 0 chunks. If data/processed/chunks is empty or non-existent, generating empty retrival pipelines. Consider running `scripts/build_company.py` to regenerate chunks!")
        else:
            logger.info("BM25 Corpus mapping loaded successfully supporting %d DocumentChunks.", len(self.chunks))
            
        self.documents = [self._tokenize(chunk.text) for chunk in self.chunks]
        self.term_frequencies = [Counter(document) for document in self.documents]
        self.document_frequencies = self._document_frequencies()
        self.average_document_length = self._average_document_length()

    def search(
        self, query: str, *, top_k: int = 5, filters: dict | None = None
    ) -> list[RetrievalResult]:
        filters = normalize_filters(filters)
        logger.info("BM25 Search | Query: '%s' | Filters: %s", query, filters)
        query_terms = self._tokenize(query)
        if not query_terms:
            logger.warning("BM25 Query rejected: Tokenizer emitted 0 tokens for query '%s'!", query)
            return []

        scored = []
        for index, chunk in enumerate(self.chunks):
            if filters:
                if any(getattr(chunk, k, None) != v for k, v in filters.items()):
                    continue

            score = self._score(query_terms, index)
            scored.append((score, chunk))
            
        scored = [(score, chunk) for score, chunk in scored if score > 0]
        scored.sort(key=lambda item: item[0], reverse=True)
        
        if not scored:
            logger.warning("BM25 Retrieval missed all chunks returning 0 candidates! Ensure filters %s match dataset geometries.", filters)

        return [
            RetrievalResult(
                chunk=chunk,
                score=score,
                source="bm25",
            )
            for score, chunk in scored[:top_k]
        ]

    def _score(self, query_terms: list[str], document_index: int) -> float:
        score = 0.0
        term_frequency = self.term_frequencies[document_index]
        document_length = len(self.documents[document_index])

        for term in query_terms:
            frequency = term_frequency.get(term, 0)
            if frequency == 0:
                continue

            idf = self._inverse_document_frequency(term)
            numerator = frequency * (self.k1 + 1)
            denominator = frequency + self.k1 * (
                1 - self.b + self.b * document_length / self.average_document_length
            )
            score += idf * numerator / denominator

        return score

    def _inverse_document_frequency(self, term: str) -> float:
        document_count = len(self.documents)
        frequency = self.document_frequencies.get(term, 0)
        return log(1 + (document_count - frequency + 0.5) / (frequency + 0.5))

    def _document_frequencies(self) -> Counter[str]:
        frequencies: Counter[str] = Counter()
        for document in self.documents:
            frequencies.update(set(document))
        return frequencies

    def _average_document_length(self) -> float:
        if not self.documents:
            return 1.0

        total_length = sum(len(document) for document in self.documents)
        return max(total_length / len(self.documents), 1.0)

    @staticmethod
    def _tokenize(text: str) -> list[str]:
        return TOKEN_PATTERN.findall(text.lower())
