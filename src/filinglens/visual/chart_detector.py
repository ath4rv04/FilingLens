from dataclasses import dataclass

@dataclass(slots=True)
class ChartSummary:
    page: int
    bbox: tuple[float, float, float, float]
    chart_type: str  # Bar, Line, Pie, Area, Waterfall
    confidence: float
    caption: str | None = None
    summary_text: str | None = None

class ChartDetector:
    """Evaluates graphical regions extracting numerical statistics implicitly bypassing text dependencies."""
    
    def detect_charts(self, image_path: str, page_number: int) -> list[ChartSummary]:
        # Implement layout detection bindings mapping bounding blocks directly 
        # (LayoutLMv3 embeddings / YOLO hooks mapped here in production)
        return []
