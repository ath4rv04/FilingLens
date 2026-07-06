import argparse
import sys

if sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

from filinglens.indexing.loader import load_chunks
from filinglens.llm.factory import get_llm
from filinglens.llm.qa_service import QAService
from filinglens.retrieval.bm25 import BM25Retriever
from filinglens.retrieval.dense import DenseRetriever
from filinglens.retrieval.hybrid import HybridRetriever
from filinglens.vectorstore.qdrant_store import QdrantVectorStore
from filinglens.settings import PROCESSED_DATA_DIR


def main():
    parser = argparse.ArgumentParser(
        description="Ask a question about financial filings."
    )
    parser.add_argument("--question", required=True, help="Question to ask.")
    parser.add_argument("--company", help="Filter by company name.")
    parser.add_argument("--year", help="Filter by year.")
    parser.add_argument("--debug", action="store_true", help="Enable developer debug mode.")
    args = parser.parse_args()

    print("Loading indices...")
    try:
        chunks = []
        if PROCESSED_DATA_DIR.exists():
            for chunk_dir in PROCESSED_DATA_DIR.rglob("chunks"):
                if chunk_dir.is_dir():
                    chunks.extend(load_chunks(chunk_dir))
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

    response, context_blocks, metrics = qa.answer(
        question=args.question,
        company=args.company,
        year=args.year,
    )

    if args.debug:
        filters = {}
        if args.company: filters["company"] = args.company
        if args.year: filters["year"] = args.year
        
        print("\n--- DEBUG OUTPUT ---")
        dense_results = dense_retriever.search(args.question, filters=filters)
        print("Dense Results:", [r.chunk.id for r in dense_results])
        
        bm25_results = bm25_retriever.search(args.question, filters=filters)
        print("BM25 Results:", [r.chunk.id for r in bm25_results])
        
        hybrid_results = hybrid_retriever.search(args.question, filters=filters)
        print("Hybrid Ranking:", [r.chunk.id for r in hybrid_results])
        
        print("Context Blocks:", [block.citation.chunk_id for block in context_blocks])
        print("Prompt Preview:\n", metrics.get("prompt_preview", ""))
        print("LLM Response RAW:\n", response.answer)
        print("--------------------\n")

    print(f"Answer\n------\n{response.answer}\n")

    print("Sources\n-------")
    for block in context_blocks:
        print(block.citation.label())


if __name__ == "__main__":
    main()
