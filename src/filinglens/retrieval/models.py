from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class RetrievalResult:
    """Normalized result returned by dense, sparse, and hybrid retrievers."""

    id: str
    score: float
    payload: dict[str, Any]
    source: str

    @property
    def text(self) -> str:
        return str(self.payload.get("text", ""))

    @property
    def chunk_id(self) -> str:
        return str(self.payload.get("chunk_id", self.id))
