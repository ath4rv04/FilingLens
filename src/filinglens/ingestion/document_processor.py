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

        image_output_dir = PROCESSED_DATA_DIR / "images" / self.company / self.year
        render_pdf(
            self.pdf_path,
            image_output_dir,
        )

        metadata = extract_metadata(
            self.pdf_path,
            self.output / "metadata.json",
        )

        from filinglens.visual.repository import VisualRepository
        visual_repo = VisualRepository()
        for page_num in range(1, metadata["page_count"] + 1):
            img_path = image_output_dir / f"page_{page_num:03d}.png"
            visual_repo.store_page(self.company, self.year, page_num, str(img_path))

        scanned_pages = extract_text(
            self.pdf_path,
            self.output / "text",
        )

        if scanned_pages:
            logger.info("Triggering OCR on %d scanned pages...", len(scanned_pages))
            from filinglens.ocr.service import get_ocr_service
            
            ocr_service = get_ocr_service().get_provider()
            
            for page_num in scanned_pages:
                image_path = visual_repo.get_image_path(self.company, self.year, page_num)
                
                if image_path:
                    ocr_page = ocr_service.process_page(image_path, page_num)
                    
                    text_parts = []
                    for block in ocr_page.blocks:
                        for line in block.lines:
                            line_str = " ".join([w.text for w in line.words])
                            text_parts.append(line_str)
                            
                    merged_text = "\n".join(text_parts)
                    
                    if merged_text:
                        text_file = self.output / "text" / f"page_{page_num:03d}.txt"
                        text_file.write_text(merged_text, encoding="utf-8")

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
