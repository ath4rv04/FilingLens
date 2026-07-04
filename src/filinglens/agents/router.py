from __future__ import annotations

from dataclasses import dataclass
import re

TABLE_TERMS = {
    "amount",
    "balance",
    "cash",
    "cost",
    "ebit",
    "ebitda",
    "expense",
    "fy",
    "income",
    "margin",
    "pat",
    "profit",
    "revenue",
    "sales",
    "total",
}
DISCLOSURE_TERMS = {
    "describe",
    "disclosure",
    "explain",
    "management",
    "md&a",
    "outlook",
    "risk",
    "strategy",
}
TOKEN_PATTERN = re.compile(r"[a-zA-Z0-9&]+")


@dataclass(slots=True)
class AgentRoute:
    use_retrieval: bool
    use_tables: bool
    reason: str


class QueryRouter:
    """Routes analyst questions to retrieval and table analysis components."""

    def route(self, question: str) -> AgentRoute:
        tokens = set(TOKEN_PATTERN.findall(question.lower()))
        has_table_signal = bool(tokens & TABLE_TERMS) or any(
            token.startswith("fy20") for token in tokens
        )
        has_disclosure_signal = bool(tokens & DISCLOSURE_TERMS)

        if has_table_signal and has_disclosure_signal:
            return AgentRoute(
                use_retrieval=True,
                use_tables=True,
                reason="question mixes numeric metrics with disclosure language",
            )

        if has_table_signal:
            return AgentRoute(
                use_retrieval=False,
                use_tables=True,
                reason="question asks for financial metrics likely found in tables",
            )

        return AgentRoute(
            use_retrieval=True,
            use_tables=False,
            reason="question is best answered from narrative filing text",
        )
