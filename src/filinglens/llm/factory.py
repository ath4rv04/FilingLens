from filinglens.llm.base import BaseLLMProvider
from filinglens.llm.ollama_provider import OllamaProvider
from filinglens.settings import LLM_PROVIDER


def get_llm() -> BaseLLMProvider:

    if LLM_PROVIDER == "ollama":
        return OllamaProvider()

    raise ValueError(f"Unknown provider: {LLM_PROVIDER}")
