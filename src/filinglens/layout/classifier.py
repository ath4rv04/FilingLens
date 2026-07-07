from enum import Enum
from dataclasses import dataclass
from filinglens.utils.logging import get_logger

logger = get_logger(__name__)

class DocumentSection(str, Enum):
    COVER = "Cover"
    CHAIRMANS_LETTER = "Chairman's Letter"
    CEO_MESSAGE = "CEO Message"
    MDA = "Management Discussion & Analysis"
    CORPORATE_GOVERNANCE = "Corporate Governance"
    FINANCIAL_STATEMENTS = "Financial Statements"
    NOTES_TO_ACCOUNTS = "Notes to Accounts"
    RISK_FACTORS = "Risk Factors"
    ESG = "ESG"
    SHAREHOLDER_INFO = "Shareholder Information"
    APPENDIX = "Appendix"
    UNKNOWN = "Unknown"

@dataclass(slots=True)
class SectionClassification:
    page: int
    section: DocumentSection
    confidence: float

class LayoutClassifier:
    """Classifies document pages into explicit repeating sections natively."""
    def classify_page(self, page_number: int, text_content: str, image_path: str | None = None) -> SectionClassification:
        content_lower = text_content.lower()
        
        if page_number == 1 or "annual report" in content_lower[:100]:
            return SectionClassification(page_number, DocumentSection.COVER, 0.9)
            
        if "management discussion" in content_lower and "analysis" in content_lower:
            return SectionClassification(page_number, DocumentSection.MDA, 0.8)
            
        if "financial statements" in content_lower and "balance sheet" in content_lower:
            return SectionClassification(page_number, DocumentSection.FINANCIAL_STATEMENTS, 0.85)
            
        if "corporate governance" in content_lower:
            return SectionClassification(page_number, DocumentSection.CORPORATE_GOVERNANCE, 0.75)
            
        return SectionClassification(page_number, DocumentSection.UNKNOWN, 0.5)
