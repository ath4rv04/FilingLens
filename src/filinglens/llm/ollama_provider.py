import requests
from typing import Iterator

from filinglens.llm.base import BaseLLMProvider
from filinglens.llm.response import LLMResponse
from filinglens.settings import (
    OLLAMA_URL,
    OLLAMA_MODEL,
    TEMPERATURE,
    TOP_K,
    REQUEST_TIMEOUT,
)
from filinglens.utils.timer import Timer
from filinglens.utils.logging import get_logger

logger = get_logger(__name__)


class OllamaProvider(BaseLLMProvider):
    """Local Ollama-backed LLM avoiding third-party clients."""

    def __init__(self):
        self.url = OLLAMA_URL
        self.model = OLLAMA_MODEL
        self.timeout = REQUEST_TIMEOUT
        self.temperature = TEMPERATURE
        self.top_k = TOP_K

        logger.info(
            "Configured OllamaProvider (model: %s, url: %s)",
            self.model,
            self.url,
        )

    def generate(
        self,
        *,
        system: str,
        user: str,
    ) -> LLMResponse:

        payload = self._build_payload(system, user, stream=False)

        with Timer() as timer:
            res = requests.post(
                f"{self.url}/api/chat", json=payload, timeout=self.timeout
            )
            res.raise_for_status()
            data = res.json()

        logger.info("Ollama generation completed in %.2f ms", timer.elapsed_ms)

        return LLMResponse(
            answer=data.get("message", {}).get("content", ""),
            model=data.get("model", self.model),
            latency_ms=timer.elapsed_ms,
            prompt_tokens=data.get("prompt_eval_count"),
            completion_tokens=data.get("eval_count"),
            total_tokens=data.get("prompt_eval_count", 0) + data.get("eval_count", 0),
        )

    def generate_stream(
        self,
        *,
        system: str,
        user: str,
    ) -> Iterator[str]:

        payload = self._build_payload(system, user, stream=True)

        res = requests.post(
            f"{self.url}/api/chat",
            json=payload,
            timeout=self.timeout,
            stream=True,
        )
        res.raise_for_status()

        import json

        for line in res.iter_lines():
            if line:
                chunk = json.loads(line)
                content = chunk.get("message", {}).get("content")
                if content:
                    yield content

    def _build_payload(self, system: str, user: str, stream: bool) -> dict:
        return {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "options": {
                "temperature": self.temperature,
                "top_k": self.top_k,
            },
            "stream": stream,
        }
