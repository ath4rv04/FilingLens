from pathlib import Path

import fitz

from filinglens.settings import SCANNED_PAGE_THRESHOLD
from filinglens.utils.logging import get_logger

logger = get_logger(__name__)


def extract_text(
    pdf_path: str | Path,
    output_dir: str | Path,
):

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    scanned_pages = []

    with fitz.open(pdf_path) as pdf:

        page_count = len(pdf)

        for page_no, page in enumerate(pdf):

            text = page.get_text()

            if len(text.strip()) < SCANNED_PAGE_THRESHOLD:
                scanned_pages.append(page_no + 1)

            output_file = (
                output_dir
                / f"page_{page_no + 1:03d}.txt"
            )

            output_file.write_text(
                text,
                encoding="utf-8",
            )

    logger.info(
        "Extracted text from %d pages.",
        page_count,
    )

    if scanned_pages:
        logger.warning(
            "Detected %d likely scanned pages: %s",
            len(scanned_pages),
            scanned_pages,
        )

    return scanned_pages