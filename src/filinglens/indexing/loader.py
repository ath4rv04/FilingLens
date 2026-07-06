from __future__ import annotations

import json
from pathlib import Path

from filinglens.models import DocumentChunk


def load_chunks(chunks_dir: Path) -> list[DocumentChunk]:
    """Load DocumentChunk objects from a directory of JSON files."""

    if not chunks_dir.exists():
        raise FileNotFoundError(f"Chunks directory not found: {chunks_dir}")

    chunks: list[DocumentChunk] = []

    for chunk_path in sorted(chunks_dir.glob("*.json")):
        with chunk_path.open(
            encoding="utf-8",
        ) as file:
            chunks.append(DocumentChunk(**json.load(file)))

    if not chunks:
        raise ValueError(f"No chunk JSON files found in: {chunks_dir}")

    return chunks
