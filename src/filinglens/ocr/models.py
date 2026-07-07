from dataclasses import dataclass

@dataclass(slots=True)
class OCRWord:
    text: str
    confidence: float
    bbox: tuple[float, float, float, float]

@dataclass(slots=True)
class OCRLine:
    words: list[OCRWord]
    bbox: tuple[float, float, float, float]

@dataclass(slots=True)
class OCRBlock:
    lines: list[OCRLine]
    bbox: tuple[float, float, float, float]

@dataclass(slots=True)
class OCRPage:
    page_number: int
    blocks: list[OCRBlock]
    confidence: float

@dataclass(slots=True)
class OCRResult:
    pages: list[OCRPage]
    success: bool
    error: str | None = None
