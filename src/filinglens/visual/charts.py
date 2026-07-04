from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class ChartCaption:
    image_path: str
    caption: str
    confidence: float


class HeuristicChartCaptioner:
    """Lightweight chart captioner until a vision-language model is wired in."""

    def caption(self, image_path: str | Path) -> ChartCaption:
        image_path = Path(image_path)
        stem = image_path.stem.replace("_", " ")
        return ChartCaption(
            image_path=str(image_path),
            caption=f"Potential filing chart or visual page: {stem}",
            confidence=0.25,
        )
