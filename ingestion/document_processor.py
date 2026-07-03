from pathlib import Path

from ingestion.metadata import extract_metadata
from ingestion.pdf_renderer import render_pdf
from ingestion.text_extractor import extract_text


class DocumentProcessor:
    def __init__(self, pdf_path: str):
        self.pdf_path = Path(pdf_path)

        if not self.pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {self.pdf_path}")

        # Expected:
        # data/raw/TCS/FY2024/annual_report.pdf
        self.company = self.pdf_path.parent.parent.name
        self.year = self.pdf_path.parent.name

        self.output = (
            Path("data")
            / "processed"
            / self.company
            / self.year
        )

    def process(self):
        print(f"Processing: {self.pdf_path.name}")
        print(f"Company : {self.company}")
        print(f"Year    : {self.year}")

        render_pdf(
            self.pdf_path,
            self.output / "pages",
        )

        extract_text(
            self.pdf_path,
            self.output / "text",
        )

        extract_metadata(
            self.pdf_path,
            self.output / "metadata.json",
        )

        print("Processing complete!")