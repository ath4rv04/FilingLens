from filinglens.vectorstore.qdrant_store import QdrantVectorStore

class VisualQdrantStore(QdrantVectorStore):
    """Overrides Qdrant integrations targeting dedicated visual partitions natively."""
    def __init__(self, collection_name: str = "filinglens_visual", url: str = "local_qdrant"):
        super().__init__(
            collection_name=collection_name, 
            url=url, 
            vector_size=2048
        )
