from filinglens.llm.ollama_provider import OllamaProvider


class FakeResponse:
    def __init__(self, data):
        self._data = data

    def raise_for_status(self):
        pass

    def json(self):
        return self._data

    def iter_lines(self):
        import json

        for msg in self._data.get("chunks", []):
            yield json.dumps({"message": {"content": msg}}).encode("utf-8")


def test_ollama_provider_generates_response(monkeypatch):
    def fake_post(*args, **kwargs):
        return FakeResponse(
            {
                "message": {"content": "Revenue grew."},
                "model": "qwen2.5:3b",
                "prompt_eval_count": 10,
                "eval_count": 5,
            }
        )

    import requests

    monkeypatch.setattr(requests, "post", fake_post)

    provider = OllamaProvider()
    response = provider.generate(system="Sys", user="Usr")

    assert response.answer == "Revenue grew."
    assert response.model == "qwen2.5:3b"
    assert response.total_tokens == 15
    assert response.latency_ms >= 0


def test_ollama_provider_generates_stream(monkeypatch):
    def fake_post(*args, **kwargs):
        return FakeResponse({"chunks": ["Rev", "enue ", "grew."]})

    import requests

    monkeypatch.setattr(requests, "post", fake_post)

    provider = OllamaProvider()
    stream = provider.generate_stream(system="Sys", user="Usr")

    results = list(stream)
    assert results == ["Rev", "enue ", "grew."]
