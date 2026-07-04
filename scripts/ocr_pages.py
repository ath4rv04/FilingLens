import argparse
from pathlib import Path

from filinglens.ocr import PaddleOCRService


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--pages", required=True, help="Directory of rendered page PNGs"
    )
    parser.add_argument("--output", required=True, help="Directory for OCR text files")
    args = parser.parse_args()

    pages_dir = Path(args.pages)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    service = PaddleOCRService()

    count = 0
    for image_path in sorted(pages_dir.glob("page_*.png")):
        result = service.extract_image(image_path)
        (output_dir / f"{image_path.stem}.txt").write_text(
            result.text,
            encoding="utf-8",
        )
        count += 1

    print(f"OCR complete for {count} pages into {output_dir}")


if __name__ == "__main__":
    main()
