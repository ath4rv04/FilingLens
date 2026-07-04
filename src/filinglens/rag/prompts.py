from __future__ import annotations

from dataclasses import dataclass

from filinglens.rag.context import ContextBlock


@dataclass(slots=True)
class RagPrompt:
    system: str
    user: str


class RagPromptBuilder:
    """Builds source-grounded analyst QA prompts."""

    system_prompt = (
        "You are FilingLens-IN, an analyst-grade financial filing assistant. "
        "Answer only from the supplied context. Cite sources with bracketed "
        "numbers like [1]. If the context is insufficient, say what is missing."
    )

    def build(self, question: str, context_blocks: list[ContextBlock]) -> RagPrompt:
        context = "\n\n".join(
            block.render(index) for index, block in enumerate(context_blocks, start=1)
        )
        if not context:
            context = "No retrieved context was available."

        return RagPrompt(
            system=self.system_prompt,
            user=(
                f"Question:\n{question.strip()}\n\n"
                f"Context:\n{context}\n\n"
                "Answer with concise reasoning and citations."
            ),
        )
