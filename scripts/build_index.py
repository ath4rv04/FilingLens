import argparse
import json
from pathlib import Path

from filinglens.embeddings.embedder import get_embedding_service
from filinglens.models.document_chunk import DocumentChunk
from filinglens.vectorstore import QdrantVectorStore


def load_chunks(chunks_dir: Path) -> list[DocumentChunk]:
    if not chunks_dir.exists():
        raise FileNotFoundError(f"Chunks directory not found: {chunks_dir}")

    chunks: list[DocumentChunk] = []

    for chunk_path in sorted(chunks_dir.glob("*.json")):
        with chunk_path.open(encoding="utf-8") as file:
            chunks.append(DocumentChunk(**json.load(file)))

    if not chunks:
        raise ValueError(f"No chunk JSON files found in: {chunks_dir}")

    return chunks


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--chunks", required=True, help="Directory containing chunk JSON files"
    )
    parser.add_argument("--collection", default=None)
    parser.add_argument("--recreate", action="store_true")
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--qdrant-url", default=None)
    args = parser.parse_args()

    chunks = load_chunks(Path(args.chunks))
    texts = [chunk.text for chunk in chunks]

    embedder = get_embedding_service()
    embeddings = embedder.embed(texts)

    store = QdrantVectorStore(
        **({"collection_name": args.collection} if args.collection else {}),
        **({"url": args.qdrant_url} if args.qdrant_url else {}),
    )
    store.create_collection(recreate=args.recreate)
    store.upload_chunks(chunks, embeddings, batch_size=args.batch_size)

    stats = store.collection_stats()
    print(
        "Indexed "
        f"{stats.get('points_count', len(chunks))} chunks into "
        f"{stats['collection_name']}"
    )


if __name__ == "__main__":
    main()
