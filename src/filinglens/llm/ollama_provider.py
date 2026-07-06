from ollama import Client

from filinglens.llm.base import BaseLLMProvider
from filinglens.llm.response import LLMResponse
from filinglens.settings import (
    OLLAMA_HOST,
    OLLAMA_MODEL,
)
from filinglens.utils.logging import get_logger

logger = get_logger(__name__)


class OllamaProvider(BaseLLMProvider):
    """Local Ollama-backed LLM."""

    def __init__(self):

        self.client = Client(host=OLLAMA_HOST)

        self.model = OLLAMA_MODEL

        logger.info(
            "Using Ollama model: %s",
            self.model,
        )

    def generate(
        self,
        *,
        system: str,
        user: str,
    ) -> LLMResponse:

        response = self.client.chat(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": system,
                },
                {
                    "role": "user",
                    "content": user,
                },
            ],
        )

        return LLMResponse(
            answer=response["message"]["content"],
            model=self.model,
        )
