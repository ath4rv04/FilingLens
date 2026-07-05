from pathlib import Path

import fitz
from tqdm import tqdm

from filinglens.settings import IMAGE_SCALE
from filinglens.utils.logging import get_logger

logger = get_logger(__name__)


def render_pdf(pdf_path: str | Path, output_dir: str | Path):

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    with fitz.open(pdf_path) as pdf:

        page_count = len(pdf)

        for page_num in tqdm(
            range(page_count),
            desc="Rendering Pages",
        ):

            page = pdf.load_page(page_num)

            pix = page.get_pixmap(
                matrix=fitz.Matrix(
                    IMAGE_SCALE,
                    IMAGE_SCALE,
                )
            )

            image_path = (
                output_dir
                / f"page_{page_num + 1:03d}.png"
            )

            pix.save(image_path)

    logger.info("Rendered %d pages.", page_count)