from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class OCRResult:
    image_path: str
    text: str
    confidence: float


class PaddleOCRService:
    """Optional PaddleOCR wrapper for scanned filing pages."""

    def __init__(self, ocr_engine: Any | None = None, *, language: str = "en") -> None:
        self.ocr_engine = ocr_engine
        self.language = language

    def extract_image(self, image_path: str | Path) -> OCRResult:
        image_path = Path(image_path)
        engine = self._engine()
        raw_result = engine.ocr(str(image_path), cls=True)
        text_parts: list[str] = []
        confidences: list[float] = []

        for page_result in raw_result or []:
            for line in page_result or []:
                if len(line) < 2:
                    continue
                text, confidence = line[1]
                text_parts.append(str(text))
                confidences.append(float(confidence))

        confidence = sum(confidences) / len(confidences) if confidences else 0.0
        return OCRResult(
            image_path=str(image_path),
            text=" ".join(text_parts).strip(),
            confidence=confidence,
        )

    def _engine(self) -> Any:
        if self.ocr_engine is not None:
            return self.ocr_engine

        from paddleocr import PaddleOCR

        self.ocr_engine = PaddleOCR(use_angle_cls=True, lang=self.language)
        return self.ocr_engine
