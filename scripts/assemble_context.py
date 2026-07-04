import argparse
from pathlib import Path

from scripts.build_index import load_chunks

from filinglens.embeddings.embedder import get_embedding_service
from filinglens.rag import ContextAssembler
from filinglens.retrieval import BM25Retriever, DenseRetriever, HybridRetriever
from filinglens.vectorstore import QdrantVectorStore


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--question", required=True)
    parser.add_argument("--chunks", required=True)
    parser.add_argument("--collection", default=None)
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--max-characters", type=int, default=6000)
    parser.add_argument("--qdrant-url", default=None)
    args = parser.parse_args()

    chunks = load_chunks(Path(args.chunks))
    vector_store = QdrantVectorStore(
        **({"collection_name": args.collection} if args.collection else {}),
        **({"url": args.qdrant_url} if args.qdrant_url else {}),
    )
    retriever = HybridRetriever(
        dense_retriever=DenseRetriever(
            embedder=get_embedding_service(),
            vector_store=vector_store,
        ),
        bm25_retriever=BM25Retriever(chunks),
    )
    results = retriever.search(args.question, top_k=args.top_k)
    context = ContextAssembler(max_characters=args.max_characters).render(results)

    print(context if context else "No context assembled.")


if __name__ == "__main__":
    main()
