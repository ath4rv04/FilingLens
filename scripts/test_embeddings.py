from filinglens.embeddings.embedder import EmbeddingService
from sklearn.metrics.pairwise import cosine_similarity

embedder = EmbeddingService()

texts = [
    "Revenue increased",
    "Sales grew",
    "The weather is sunny",
]

vectors = embedder.embed(texts)

print(cosine_similarity(vectors))
