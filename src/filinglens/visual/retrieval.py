from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class VisualPageResult:
    page: int
    image_path: str
    score: float


class VisualRetriever:
    """File-backed visual page retriever placeholder for ColPali/ColQwen2."""

    def __init__(self, pages_dir: str | Path) -> None:
        self.pages_dir = Path(pages_dir)

    def search(self, query: str, *, top_k: int = 5) -> list[VisualPageResult]:
        if not self.pages_dir.exists():
            raise FileNotFoundError(f"Pages directory not found: {self.pages_dir}")

        query_terms = set(query.lower().split())
        results: list[VisualPageResult] = []

        for image_path in sorted(self.pages_dir.glob("page_*.png")):
            page = int(image_path.stem.split("_")[1])
            filename_terms = set(image_path.stem.lower().split("_"))
            score = 1.0 + len(query_terms & filename_terms) * 0.1
            results.append(
                VisualPageResult(
                    page=page,
                    image_path=str(image_path),
                    score=score,
                )
            )

        return results[:top_k]
