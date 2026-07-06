import pytest

from filinglens.llm.factory import get_llm
from filinglens.llm.ollama_provider import OllamaProvider


def test_get_llm_returns_ollama_provider(monkeypatch):
    import filinglens.llm.factory as factory

    monkeypatch.setattr(factory, "LLM_PROVIDER", "ollama")

    llm = get_llm()
    assert isinstance(llm, OllamaProvider)


def test_get_llm_raises_value_error_for_unknown_provider(monkeypatch):
    import filinglens.llm.factory as factory

    monkeypatch.setattr(factory, "LLM_PROVIDER", "unknown")

    with pytest.raises(ValueError, match="Unknown provider"):
        get_llm()
