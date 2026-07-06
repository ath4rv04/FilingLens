from functools import lru_cache
from typing import Annotated
from fastapi import Depends

from filinglens.embeddings.embedder import get_embedding_service, EmbeddingService
from filinglens.vectorstore.qdrant_store import QdrantVectorStore
from filinglens.retrieval.dense import DenseRetriever
from filinglens.retrieval.bm25 import BM25Retriever
from filinglens.retrieval.hybrid import HybridRetriever
from filinglens.llm.base import BaseLLMProvider
from filinglens.llm.factory import get_llm
from filinglens.llm.qa_service import QAService
from filinglens.services.indexing_service import IndexingService
from filinglens.indexing.loader import load_chunks
from filinglens.settings import PROCESSED_DATA_DIR


@lru_cache
def get_embedder() -> EmbeddingService:
    return get_embedding_service()


@lru_cache
def get_qdrant_store() -> QdrantVectorStore:
    return QdrantVectorStore()


@lru_cache
def get_hybrid_retriever(
    embedder: Annotated[EmbeddingService, Depends(get_embedder)],
    vector_store: Annotated[QdrantVectorStore, Depends(get_qdrant_store)],
) -> HybridRetriever:
    dense_retriever = DenseRetriever(embedder=embedder, vector_store=vector_store)

    chunks = []
    if PROCESSED_DATA_DIR.exists():
        for chunk_dir in PROCESSED_DATA_DIR.rglob("chunks"):
            if chunk_dir.is_dir():
                try:
                    loaded = load_chunks(chunk_dir)
                    chunks.extend(loaded)
                except (FileNotFoundError, ValueError):
                    pass

    bm25_retriever = BM25Retriever(chunks=chunks)

    return HybridRetriever(
        dense_retriever=dense_retriever,
        bm25_retriever=bm25_retriever,
    )


@lru_cache
def get_llm_provider() -> BaseLLMProvider:
    return get_llm()


def get_qa_service(
    retriever: Annotated[HybridRetriever, Depends(get_hybrid_retriever)],
    llm: Annotated[BaseLLMProvider, Depends(get_llm_provider)],
) -> QAService:
    return QAService(retriever=retriever, llm=llm)


def get_indexing_service(
    embedder: Annotated[EmbeddingService, Depends(get_embedder)],
    vector_store: Annotated[QdrantVectorStore, Depends(get_qdrant_store)],
) -> IndexingService:
    return IndexingService(embedder=embedder, vector_store=vector_store)
