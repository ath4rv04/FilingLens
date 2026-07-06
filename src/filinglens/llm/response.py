from dataclasses import dataclass


@dataclass(slots=True)
class LLMResponse:
    """Canonical model for LLM generation responses."""

    answer: str
    model: str
    latency_ms: float
    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    total_tokens: int | None = None
