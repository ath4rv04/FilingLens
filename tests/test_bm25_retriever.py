from filinglens.models.document_chunk import DocumentChunk
from filinglens.retrieval import BM25Retriever


def test_bm25_retriever_ranks_matching_chunks_first():
    chunks = [
        DocumentChunk(
            id="chunk-1",
            company="TCS",
            year="FY2024",
            page=1,
            chunk=0,
            text="Revenue from banking clients increased sharply.",
        ),
        DocumentChunk(
            id="chunk-2",
            company="TCS",
            year="FY2024",
            page=2,
            chunk=0,
            text="Employee headcount and hiring plans were discussed.",
        ),
    ]

    retriever = BM25Retriever(chunks)
    results = retriever.search("banking revenue", top_k=1)

    assert len(results) == 1
    assert results[0].chunk_id == "chunk-1"
    assert results[0].source == "bm25"


def test_bm25_retriever_returns_empty_for_non_text_query():
    retriever = BM25Retriever([])

    assert retriever.search("!!!") == []
