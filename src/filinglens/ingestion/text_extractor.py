from pathlib import Path
import fitz


def extract_text(pdf_path: str, output_dir: str):
    doc = fitz.open(pdf_path)

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for page_no, page in enumerate(doc):
        text = page.get_text()

        with open(
            output_dir / f"page_{page_no + 1:03d}.txt",
            "w",
            encoding="utf-8",
        ) as f:
            f.write(text)

    print("Text extraction complete.")
