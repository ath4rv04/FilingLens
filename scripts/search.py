import argparse

from filinglens.embeddings.embedder import get_embedding_service
from filinglens.vectorstore import QdrantVectorStore


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--question", required=True)
    parser.add_argument("--collection", default=None)
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--qdrant-url", default=None)
    args = parser.parse_args()

    embedder = get_embedding_service()
    query_vector = embedder.embed([args.question])

    store = QdrantVectorStore(
        **({"collection_name": args.collection} if args.collection else {}),
        **({"url": args.qdrant_url} if args.qdrant_url else {}),
    )

    results = store.search(query_vector, top_k=args.top_k)

    if not results:
        print("No results found.")
        return

    for result in results:
        payload = result.payload
        print(
            f"[{result.score:.4f}] "
            f"{payload.get('company')} {payload.get('year')} "
            f"page {payload.get('page')} chunk {payload.get('chunk')}"
        )
        print(result.text[:600].strip())
        print()


if __name__ == "__main__":
    main()
