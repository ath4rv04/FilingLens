import json
from pathlib import Path

import fitz

from filinglens.utils.logging import get_logger

logger = get_logger(__name__)


def extract_metadata(
    pdf_path: str | Path,
    output_path: str | Path,
) -> dict:
    """
    Extract metadata from a PDF.

    Returns
    -------
    dict
        Metadata dictionary.
    """

    output_path = Path(output_path)
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with fitz.open(pdf_path) as pdf:

        metadata = {
            "page_count": len(pdf),
            "title": pdf.metadata.get("title"),
            "author": pdf.metadata.get("author"),
            "producer": pdf.metadata.get("producer"),
            "creator": pdf.metadata.get("creator"),
            "subject": pdf.metadata.get("subject"),
            "keywords": pdf.metadata.get("keywords"),
            "creation_date": pdf.metadata.get("creationDate"),
            "modification_date": pdf.metadata.get("modDate"),
            "is_encrypted": pdf.is_encrypted,
        }

    with open(
        output_path,
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            metadata,
            f,
            indent=4,
            ensure_ascii=False,
        )

    logger.info("Metadata saved.")

    return metadata