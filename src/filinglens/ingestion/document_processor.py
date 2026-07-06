from pathlib import Path

from filinglens.settings import PROCESSED_DATA_DIR
from filinglens.utils.logging import get_logger

from filinglens.embeddings.chunker import Chunker
from filinglens.ingestion.metadata import extract_metadata
from filinglens.ingestion.pdf_renderer import render_pdf
from filinglens.ingestion.text_extractor import extract_text
from filinglens.models.processing_result import ProcessingResult

logger = get_logger(__name__)


class DocumentProcessor:
    """Coordinates the complete document processing pipeline."""

    def __init__(self, pdf_path: str):

        self.pdf_path = Path(pdf_path)

        if not self.pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {self.pdf_path}")

        # Expected:
        # data/raw/TCS/FY2024/annual_report.pdf
        self.company = self.pdf_path.parent.parent.name
        self.year = self.pdf_path.parent.name

        self.output = PROCESSED_DATA_DIR / self.company / self.year

    def process(self) -> ProcessingResult:

        logger.info(
            "Processing document: %s",
            self.pdf_path.name,
        )

        render_pdf(
            self.pdf_path,
            self.output / "pages",
        )

        scanned_pages = extract_text(
            self.pdf_path,
            self.output / "text",
        )

        metadata = extract_metadata(
            self.pdf_path,
            self.output / "metadata.json",
        )

        chunker = Chunker()

        chunk_count = chunker.process_folder(
            self.output / "text",
            self.output / "chunks",
            self.company,
            self.year,
        )

        logger.info(
            "Finished processing %s",
            self.pdf_path.name,
        )

        return ProcessingResult(
            company=self.company,
            year=self.year,
            page_count=metadata["page_count"],
            scanned_pages=scanned_pages,
            chunk_count=chunk_count,
        )
