from pathlib import Path
import fitz
from tqdm import tqdm
from filinglens.utils.logging import get_logger



def render_pdf(pdf_path: str, output_dir: str):
    pdf = fitz.open(pdf_path)

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for page_num in tqdm(range(len(pdf)), desc="Rendering Pages"):
        page = pdf.load_page(page_num)

        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))

        image_path = output_dir / f"page_{page_num + 1:03d}.png"

        pix.save(image_path)

    logger = get_logger(__name__)

    logger.info("Rendered %d pages", len(pdf))