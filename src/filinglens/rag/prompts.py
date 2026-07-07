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
You are FilingLens-IN, an expert multimodal financial filing assistant.

Rules:

1. Answer ONLY using the supplied multimodal context.
2. Never invent facts.
3. Every factual statement must cite one or more sources like [1] along with the modality.
4. If the answer cannot be determined from the context, explicitly say so.
5. If numbers conflict, mention the conflict and cite both sources.
6. Prefer deterministic financial metrics and tabular values when available.
7. Preserve financial terminology exactly.
""".strip()

    def build(
        self,
        question: str,
        context_blocks: list[ContextBlock],
    ) -> RagPrompt:

        from collections import defaultdict
        
        grouped_blocks = defaultdict(list)
        for i, block in enumerate(context_blocks, start=1):
            source_tag = block.source.upper() if block.source else "TEXT"
            grouped_blocks[source_tag].append(block.render(i))
            
        context_parts = []
        for modality, b_list in grouped_blocks.items():
            context_parts.append(f"==== {modality} ====")
            context_parts.extend(b_list)
            
        context = "\n\n".join(context_parts)

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
