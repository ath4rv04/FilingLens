import json
from dataclasses import asdict
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter

from filinglens.models.document_chunk import DocumentChunk
from filinglens.settings import CHUNK_OVERLAP, CHUNK_SIZE
from filinglens.utils.logging import get_logger

logger = get_logger(__name__)


class Chunker:
    """Splits extracted text into overlapping chunks."""

    def __init__(self):

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
        )

    def process_folder(
        self,
        text_folder: str | Path,
        output_folder: str | Path,
        company: str,
        year: str,
    ) -> int:

        text_folder = Path(text_folder)
        output_folder = Path(output_folder)

        output_folder.mkdir(parents=True, exist_ok=True)

        chunk_count = 0

        for txt_file in sorted(text_folder.glob("*.txt")):
            page = int(txt_file.stem.split("_")[1])

            text = txt_file.read_text(
                encoding="utf-8",
            )

            if not text.strip():
                logger.warning(
                    "Skipping empty page: %s",
                    txt_file.name,
                )
                continue

            chunks = self.splitter.split_text(text)

            for i, chunk_text in enumerate(chunks):
                document_chunk = DocumentChunk(
                    id=f"{company}_{year}_page_{page}_chunk_{i}",
                    company=company,
                    year=year,
                    page=page,
                    chunk=i,
                    text=chunk_text,
                )

                output_path = output_folder / f"{document_chunk.id}.json"

                with open(
                    output_path,
                    "w",
                    encoding="utf-8",
                ) as f:
                    json.dump(
                        asdict(document_chunk),
                        f,
                        indent=4,
                        ensure_ascii=False,
                    )

                chunk_count += 1

        logger.info(
            "Created %d chunks.",
            chunk_count,
        )

        return chunk_count
