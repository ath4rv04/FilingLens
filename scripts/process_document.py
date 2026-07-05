import argparse

from filinglens.ingestion.document_processor import DocumentProcessor

parser = argparse.ArgumentParser(
    description="Process a financial filing PDF."
)

parser.add_argument(
    "--input",
    required=True,
    help="Path to the PDF file",
)

args = parser.parse_args()

processor = DocumentProcessor(args.input)

result = processor.process()

print("\nProcessing Summary")
print("-" * 30)
print(f"Company        : {result.company}")
print(f"Year           : {result.year}")
print(f"Pages          : {result.page_count}")
print(f"Chunk Count    : {result.chunk_count}")
print(f"Scanned Pages  : {len(result.scanned_pages)}")

if result.scanned_pages:
    print(f"Page Numbers   : {result.scanned_pages}")