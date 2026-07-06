import argparse
from filinglens.settings import PROCESSED_DATA_DIR, FINANCE_DB_PATH
from filinglens.indexing.loader import load_chunks
from filinglens.finance.extractor import FinancialMetricExtractor
from filinglens.finance.repository import FinanceRepository


def main():
    parser = argparse.ArgumentParser(
        description="Extract deterministic analytics skipping semantic flows."
    )
    parser.add_argument("--company", required=True)
    parser.add_argument("--year", required=True)
    args = parser.parse_args()

    chunk_dir = PROCESSED_DATA_DIR / args.company / args.year / "chunks"
    if not chunk_dir.exists():
        print("Error: No chunks found for extraction.")
        return

    chunks = load_chunks(chunk_dir)
    extractor = FinancialMetricExtractor()
    repo = FinanceRepository(db_path=FINANCE_DB_PATH)

    total = []
    for chunk in chunks:
        metrics = extractor.extract_from_chunk(chunk)
        total.extend(metrics)

    repo.save_many(total)
    print(
        f"Extraction successful: Mapped {len(total)} individual scalars directly bypassing LLMs."
    )


if __name__ == "__main__":
    main()
