from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from filinglens.retrieval import RetrievalResult
from filinglens.utils.logging import get_logger

logger = get_logger(__name__)


@dataclass(slots=True)
class Citation:
    """Represents a source citation."""

    company: str
    year: str
    page: int | None
    chunk: int |None
    chunk_id: str

    def label(self) -> str:
        """Return a human-readable citation label."""

        location = []

        if self.page is not None:
            location.append(f"p. {self.page}")

        if self.chunk is not None:
            location.append(f"chunk {self.chunk}")

        suffix = ", ".join(location) if location else self.chunk_id

        return f"{self.company} {self.year}, {suffix}"


@dataclass(slots=True)
class ContextBlock:
    """Single retrieved context block."""

    citation: Citation
    text: str
    score: float
    source: str

    def render(self, index: int) -> str:
        return (
            f"[{index}] {self.citation.label()}\n"
            f"{self.text}"
        )


class ContextAssembler:
    """
    Builds an LLM-ready context from retrieval results.

    Responsibilities:
    - Remove duplicate chunks.
    - Sort by retrieval score.
    - Respect context length limits.
    - Preserve citations.
    """

    def __init__(
        self,
        *,
        max_characters: int = 6000,
    ) -> None:

        if max_characters < 1:
            raise ValueError(
                "max_characters must be at least 1."
            )

        self.max_characters = max_characters

    def assemble(
        self,
        results: list[RetrievalResult],
    ) -> list[ContextBlock]:

        if not results:
            logger.warning("No retrieval results supplied.")
            return []

        blocks: list[ContextBlock] = []

        used_characters = 0

        seen_chunks: set[str] = set()

        sorted_results = sorted(
            results,
            key=lambda result: result.score,
            reverse=True,
        )

        for result in sorted_results:

            if result.chunk_id in seen_chunks:
                continue

            seen_chunks.add(result.chunk_id)

            text = self._clean_text(result.text)

            if not text:
                continue

            remaining = self.max_characters - used_characters

            if remaining <= 0:
                break

            if len(text) > remaining:
                text = text[:remaining].rstrip()

            block = ContextBlock(
                citation=self._citation(
                    result.payload,
                    result.chunk_id,
                ),
                text=text,
                score=result.score,
                source=result.source,
            )

            blocks.append(block)

            used_characters += len(text)

        logger.info(
            "Built %d context blocks (%d chars).",
            len(blocks),
            used_characters,
        )

        return blocks

    def render(
        self,
        results: list[RetrievalResult],
    ) -> str:

        blocks = self.assemble(results)

        return "\n\n".join(
            block.render(i)
            for i, block in enumerate(
                blocks,
                start=1,
            )
        )

    @staticmethod
    def _citation(
        payload: dict[str, Any],
        chunk_id: str,
    ) -> Citation:

        return Citation(
            company=str(payload.get("company", "Unknown")),
            year=str(payload.get("year", "Unknown")),
            page=ContextAssembler._optional_int(
                payload.get("page")
            ),
            chunk=ContextAssembler._optional_int(
                payload.get("chunk")
            ),
            chunk_id=chunk_id,
        )

    @staticmethod
    def _optional_int(
        value: Any,
    ) -> int | None:

        if value is None:
            return None

        try:
            return int(value)

        except (TypeError, ValueError):
            return None

    @staticmethod
    def _clean_text(
        text: str,
    ) -> str:

        return " ".join(text.split())