import argparse
from pathlib import Path

from filinglens.tables import PdfPlumberTableExtractor


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input", required=True, help="PDF file to extract tables from"
    )
    parser.add_argument("--output", required=True, help="Directory for table CSV files")
    args = parser.parse_args()

    extractor = PdfPlumberTableExtractor()
    tables = extractor.extract(Path(args.input))
    written_paths = extractor.write_csvs(tables, Path(args.output))

    print(f"Extracted {len(written_paths)} tables into {args.output}")


if __name__ == "__main__":
    main()
