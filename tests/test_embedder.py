import numpy as np
from types import SimpleNamespace

from filinglens.embeddings import embedder


class FakeSentenceTransformer:
    def __init__(self, model_name, device):
        self.model_name = model_name
        self.device = device

    def encode(
        self,
        texts,
        normalize_embeddings,
        convert_to_numpy,
        show_progress_bar,
    ):
        assert normalize_embeddings is True
        assert convert_to_numpy is True
        assert show_progress_bar is True
        return np.zeros((len(texts), 1024))


def test_embedding_dimension(monkeypatch):
    monkeypatch.setattr(embedder, "SentenceTransformer", FakeSentenceTransformer)
    monkeypatch.setattr(
        embedder,
        "torch",
        SimpleNamespace(cuda=SimpleNamespace(is_available=lambda: False)),
    )

    service = embedder.EmbeddingService()

    vector = service.embed("hello")

    assert vector.shape == (1, 1024)
    assert service.device == "cpu"


def test_get_embedding_service_is_cached(monkeypatch):
    embedder.get_embedding_service.cache_clear()
    monkeypatch.setattr(embedder, "SentenceTransformer", FakeSentenceTransformer)
    monkeypatch.setattr(
        embedder,
        "torch",
        SimpleNamespace(cuda=SimpleNamespace(is_available=lambda: False)),
    )

    assert embedder.get_embedding_service() is embedder.get_embedding_service()
    embedder.get_embedding_service.cache_clear()
