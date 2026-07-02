from pathlib import Path
import fitz


def render_pdf(pdf_path: str, output_dir: str):
    pdf = fitz.open(pdf_path)

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for page_num in range(len(pdf)):
        page = pdf.load_page(page_num)

        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))

        image_path = output_dir / f"page_{page_num+1:03d}.png"

        pix.save(image_path)

    print(f"Rendered {len(pdf)} pages.")