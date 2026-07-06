import json

import pytest

from filinglens.indexing import load_chunks


def test_load_chunks_reads_document_chunk_json(tmp_path):
    chunk_path = tmp_path / "chunk.json"
    chunk_path.write_text(
        json.dumps(
            {
                "id": "TCS_FY2024_page_1_chunk_0",
                "company": "TCS",
                "year": "FY2024",
                "page": 1,
                "chunk": 0,
                "text": "Revenue increased.",
            }
        ),
        encoding="utf-8",
    )

    chunks = load_chunks(tmp_path)

    assert len(chunks) == 1
    assert chunks[0].company == "TCS"
    assert chunks[0].text == "Revenue increased."


def test_load_chunks_rejects_missing_directory(tmp_path):
    with pytest.raises(FileNotFoundError, match="Chunks directory"):
        load_chunks(tmp_path / "missing")


def test_load_chunks_rejects_empty_directory(tmp_path):
    with pytest.raises(ValueError, match="No chunk JSON"):
        load_chunks(tmp_path)
