import argparse

from filinglens.ingestion.document_processor import DocumentProcessor

parser = argparse.ArgumentParser()

parser.add_argument(
    "--input",
    required=True,
)

args = parser.parse_args()

processor = DocumentProcessor(args.input)

processor.process()

print("Done!")