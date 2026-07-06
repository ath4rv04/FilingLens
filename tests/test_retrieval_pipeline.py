import pytest
from filinglens.models.document_chunk import DocumentChunk
from filinglens.vectorstore.qdrant_store import QdrantVectorStore
from filinglens.retrieval.dense import DenseRetriever
from filinglens.rag.context import ContextAssembler

def test_retrieval_pipeline_mock_free():
    # Setup mock-free local embeddings
    from filinglens.embeddings.embedder import get_embedding_service
    embedder = get_embedding_service()
    
    store = QdrantVectorStore()
    
    chunk = DocumentChunk(
        id="testpipe_2024_page_1_chunk_0",
        company="testpipe",
        year="2024",
        page=1,
        chunk=0,
        text="This is a financial test chunk containing important revenue metrics for 2024 pipeline."
    )
    
    embeddings = embedder.embed([chunk.text], show_progress_bar=False)
    
    store.upload_chunks([chunk], embeddings)
    
    retriever = DenseRetriever(vector_store=store, embedder=embedder)
    
    # Must retrieve
    results = retriever.search("revenue metrics pipeline", filters={"company": "testpipe", "year": "2024"})
    assert len(results) > 0, "Retrieval returned 0 hits!"
    
    assembler = ContextAssembler()
    blocks = assembler.assemble(results)
    
    assert len(blocks) > 0, "Context blocks dropped unexpectedly!"
    assert blocks[0].citation.company == "testpipe"
    assert "revenue metrics for 2024" in blocks[0].text
