import argparse
from filinglens.downloader.downloader import DownloadManager
from filinglens.ingestion.document_processor import DocumentProcessor
from filinglens.indexing.loader import load_chunks
from filinglens.finance.extractor import FinancialMetricExtractor
from filinglens.finance.repository import FinanceRepository
from filinglens.services.indexing_service import IndexingService
from filinglens.settings import FINANCE_DB_PATH, PROCESSED_DATA_DIR
from filinglens.api.dependencies import get_embedder, get_qdrant_store


def main():
    parser = argparse.ArgumentParser(description="Full E2E Engine Initialization")
    parser.add_argument("--company", required=True)
    parser.add_argument("--year", required=True)
    args = parser.parse_args()

    print(f"1. Downloading {args.company} {args.year}")
    manager = DownloadManager()
    res = manager.download(args.company, args.year)
    if not res.success:
        print(f"Fatal Download Collision: {res.error}")
        return

    print("2. Processing PDF natively...")
    pdf_path = res.path
    if not pdf_path:
        pdf_path = manager.storage.get_filing_path(res.filing)

    processor = DocumentProcessor(str(pdf_path))
    proc_res = processor.process()

    print("3. Extracting deterministic Finance analytics...")
    chunk_dir = PROCESSED_DATA_DIR / args.company / args.year / "chunks"
    chunks = load_chunks(chunk_dir)
    extractor = FinancialMetricExtractor()
    repo = FinanceRepository(db_path=FINANCE_DB_PATH)

    total = []
    for chunk in chunks:
        metrics = extractor.extract_from_chunk(chunk)
        total.extend(metrics)
    repo.save_many(total)

    print("4. Generating Vector Indexes natively...")
    embedder = get_embedder()
    store = get_qdrant_store()
    indexer = IndexingService(embedder, store)
    count, _ = indexer.index_company_year(args.company, args.year)

    print(
        f"\nIntegration Complete: Extracted {len(total)} analytical tuples, Indexed {count} semantic chunks seamlessly."
    )


if __name__ == "__main__":
    main()
