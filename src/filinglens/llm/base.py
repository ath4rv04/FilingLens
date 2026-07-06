from abc import ABC, abstractmethod

from filinglens.llm.response import LLMResponse


class BaseLLMProvider(ABC):
    """Abstract base class for LLM providers."""

    @abstractmethod
    def generate(
        self,
        *,
        system: str,
        user: str,
    ) -> LLMResponse:
        raise NotImplementedError

    @abstractmethod
    def generate_stream(
        self,
        *,
        system: str,
        user: str,
    ):
        raise NotImplementedError
