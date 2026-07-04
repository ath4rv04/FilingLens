from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from filinglens.retrieval import RetrievalResult


@dataclass(slots=True)
class Citation:
    company: str
    year: str
    page: int | None
    chunk: int | None
    chunk_id: str

    def label(self) -> str:
        location = []
        if self.page is not None:
            location.append(f"p. {self.page}")
        if self.chunk is not None:
            location.append(f"chunk {self.chunk}")

        suffix = ", ".join(location) if location else self.chunk_id
        return f"{self.company} {self.year}, {suffix}"


@dataclass(slots=True)
class ContextBlock:
    citation: Citation
    text: str
    score: float
    source: str

    def render(self, index: int) -> str:
        return f"[{index}] {self.citation.label()}\n{self.text}"


class ContextAssembler:
    """Builds compact, citation-ready context from retrieval results."""

    def __init__(self, *, max_characters: int = 6000) -> None:
        if max_characters < 1:
            raise ValueError("max_characters must be at least 1")

        self.max_characters = max_characters

    def assemble(self, results: list[RetrievalResult]) -> list[ContextBlock]:
        blocks: list[ContextBlock] = []
        used_characters = 0

        for result in results:
            text = self._clean_text(result.text)
            if not text:
                continue

            remaining = self.max_characters - used_characters
            if remaining <= 0:
                break

            text = text[:remaining].rstrip()
            if not text:
                break

            blocks.append(
                ContextBlock(
                    citation=self._citation(result.payload, result.chunk_id),
                    text=text,
                    score=result.score,
                    source=result.source,
                )
            )
            used_characters += len(text)

        return blocks

    def render(self, results: list[RetrievalResult]) -> str:
        blocks = self.assemble(results)
        return "\n\n".join(
            block.render(index) for index, block in enumerate(blocks, start=1)
        )

    @staticmethod
    def _citation(payload: dict[str, Any], chunk_id: str) -> Citation:
        return Citation(
            company=str(payload.get("company", "Unknown")),
            year=str(payload.get("year", "Unknown")),
            page=ContextAssembler._optional_int(payload.get("page")),
            chunk=ContextAssembler._optional_int(payload.get("chunk")),
            chunk_id=chunk_id,
        )

    @staticmethod
    def _optional_int(value: Any) -> int | None:
        if value is None:
            return None

        return int(value)

    @staticmethod
    def _clean_text(text: str) -> str:
        return " ".join(text.split())
