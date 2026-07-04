import argparse
from pathlib import Path

from scripts.build_index import load_chunks

from filinglens.embeddings.embedder import get_embedding_service
from filinglens.retrieval import BM25Retriever, DenseRetriever, HybridRetriever
from filinglens.vectorstore import QdrantVectorStore


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--question", required=True)
    parser.add_argument("--chunks", required=True)
    parser.add_argument("--collection", default=None)
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--candidate-k", type=int, default=None)
    parser.add_argument("--qdrant-url", default=None)
    args = parser.parse_args()

    chunks = load_chunks(Path(args.chunks))
    bm25_retriever = BM25Retriever(chunks)

    vector_store = QdrantVectorStore(
        **({"collection_name": args.collection} if args.collection else {}),
        **({"url": args.qdrant_url} if args.qdrant_url else {}),
    )
    dense_retriever = DenseRetriever(
        embedder=get_embedding_service(),
        vector_store=vector_store,
    )
    hybrid_retriever = HybridRetriever(
        dense_retriever=dense_retriever,
        bm25_retriever=bm25_retriever,
    )

    results = hybrid_retriever.search(
        args.question,
        top_k=args.top_k,
        candidate_k=args.candidate_k,
    )

    if not results:
        print("No results found.")
        return

    for result in results:
        payload = result.payload
        sources = ", ".join(payload.get("retrieval_sources", []))
        print(
            f"[{result.score:.4f}] {payload.get('company')} {payload.get('year')} "
            f"page {payload.get('page')} chunk {payload.get('chunk')} ({sources})"
        )
        print(result.text[:600].strip())
        print()


if __name__ == "__main__":
    main()
