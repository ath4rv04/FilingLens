from dataclasses import dataclass


@dataclass(slots=True)
class LLMResponse:
    """Structured LLM response."""

    answer: str

    model: str

    prompt_tokens: int | None = None

    completion_tokens: int | None = None

    total_tokens: int | None = None