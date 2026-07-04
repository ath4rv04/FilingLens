import fitz
import json
from pathlib import Path


def extract_metadata(pdf_path: str, output_path: str):
    doc = fitz.open(pdf_path)

    metadata = {
        "pages": len(doc),
        "title": doc.metadata.get("title"),
        "author": doc.metadata.get("author"),
        "producer": doc.metadata.get("producer"),
        "creator": doc.metadata.get("creator"),
    }

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4)

    print("Metadata saved.")
