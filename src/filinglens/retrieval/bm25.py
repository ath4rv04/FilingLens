from __future__ import annotations

from collections import Counter
from dataclasses import asdict, is_dataclass
from math import log
import re
from typing import Any

from filinglens.models.document_chunk import DocumentChunk
from filinglens.retrieval.models import RetrievalResult

TOKEN_PATTERN = re.compile(r"[a-zA-Z0-9]+")


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
        self.payloads = [self._payload(chunk) for chunk in chunks]
        self.documents = [self._tokenize(payload["text"]) for payload in self.payloads]
        self.term_frequencies = [Counter(document) for document in self.documents]
        self.document_frequencies = self._document_frequencies()
        self.average_document_length = self._average_document_length()

    def search(self, query: str, *, top_k: int = 5) -> list[RetrievalResult]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []

        scored = [
            (
                self._score(query_terms, index),
                self.payloads[index],
            )
            for index in range(len(self.payloads))
        ]
        scored = [(score, payload) for score, payload in scored if score > 0]
        scored.sort(key=lambda item: item[0], reverse=True)

        return [
            RetrievalResult(
                id=str(payload["chunk_id"]),
                score=score,
                payload=payload,
                source="bm25",
            )
            for score, payload in scored[:top_k]
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

    @staticmethod
    def _payload(chunk: DocumentChunk | dict[str, Any]) -> dict[str, Any]:
        payload = asdict(chunk) if is_dataclass(chunk) else dict(chunk)
        payload["chunk_id"] = payload.pop("id", payload.get("chunk_id"))
        return payload
