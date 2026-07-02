from ingestion.pdf_renderer import render_pdf
from ingestion.metadata import extract_metadata
from ingestion.text_extractor import extract_text


PDF = "data/raw/TCS/FY2024/annual_report.pdf"
BASE = "data/processed/TCS/FY2024"

render_pdf(PDF, f"{BASE}/pages")
extract_text(PDF, f"{BASE}/text")
extract_metadata(PDF, f"{BASE}/metadata.json")

print("Pipeline completed successfully!")