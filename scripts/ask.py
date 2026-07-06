import argparse

from filinglens.indexing.loader import load_chunks
from filinglens.llm.factory import get_llm
from filinglens.llm.qa_service import QAService
from filinglens.retrieval.bm25 import BM25Retriever
from filinglens.retrieval.dense import DenseRetriever
from filinglens.retrieval.hybrid import HybridRetriever
from filinglens.vectorstore.qdrant_store import QdrantVectorStore
from filinglens.settings import PROCESSED_DATA_DIR


def main():
    parser = argparse.ArgumentParser(description="Ask a question about financial filings.")
    parser.add_argument("--question", required=True, help="Question to ask.")
    parser.add_argument("--company", help="Filter by company name.")
    parser.add_argument("--year", help="Filter by year.")
    args = parser.parse_args()

    print("Loading indices...")
    try:
        chunks = load_chunks(PROCESSED_DATA_DIR / "chunks")
    except Exception as e:
        print(f"Error loading chunks for BM25: {e}")
        print("Falling back to empty BM25 chunk state.")
        chunks = []

    vector_store = QdrantVectorStore()
    dense_retriever = DenseRetriever(vector_store=vector_store)
    bm25_retriever = BM25Retriever(chunks=chunks)
    hybrid_retriever = HybridRetriever(
        dense_retriever=dense_retriever, bm25_retriever=bm25_retriever
    )

    llm = get_llm()
    qa = QAService(retriever=hybrid_retriever, llm=llm)

    print(f"\nQuestion\n--------\n{args.question}\n")

    response, context_blocks = qa.answer(
        question=args.question,
        company=args.company,
        year=args.year,
    )

    print(f"Answer\n------\n{response.answer}\n")

    print("Sources\n-------")
    for block in context_blocks:
        print(block.citation.label())


if __name__ == "__main__":
    main()
