from filinglens.embeddings.embedder import get_embedding_service

embedder = get_embedding_service()

print(f"Device: {embedder.device}")
print(f"Dimension: {embedder.embedding_dimension}")

texts = [
    "Revenue increased by 15%",
    "Sales grew by 15%",
    "The weather is sunny today",
]

embeddings = embedder.embed(
    texts,
    show_progress_bar=True,
)

print("Embedding shape:", embeddings.shape)