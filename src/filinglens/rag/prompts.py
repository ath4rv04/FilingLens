from __future__ import annotations

from dataclasses import dataclass

from filinglens.rag.context import ContextBlock


@dataclass(slots=True)
class RagPrompt:
    """Container for chat prompts."""

    system: str
    user: str


class RagPromptBuilder:
    """Build analyst-grade prompts for FilingLens."""

    SYSTEM_PROMPT = """
You are FilingLens-IN, an expert financial filing analysis assistant.

Rules:

1. Answer ONLY using the supplied context.
2. Never invent facts.
3. Every factual statement must cite one or more sources like [1].
4. If the answer cannot be determined from the context,
   explicitly say so.
5. Prefer concise analyst-style writing.
6. Preserve financial terminology exactly.
7. If numbers conflict, mention the conflict and cite both.
""".strip()

    def build(
        self,
        question: str,
        context_blocks: list[ContextBlock],
    ) -> RagPrompt:

        context = "\n\n".join(
            block.render(i)
            for i, block in enumerate(
                context_blocks,
                start=1,
            )
        )

        if not context:
            context = "No context available."

        user_prompt = f"""
Question

{question.strip()}

Context

{context}

Instructions

• Answer the question.
• Use citations like [1].
• If information is missing, explain what is missing.
• Do not use outside knowledge.
""".strip()

        return RagPrompt(
            system=self.SYSTEM_PROMPT,
            user=user_prompt,
        )