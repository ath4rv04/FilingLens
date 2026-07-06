import re

from filinglens.models.document_chunk import DocumentChunk
from filinglens.finance.models import FinancialMetric
from filinglens.finance.normalizer import normalize_metric_name
from filinglens.finance.parser import parse_financial_value
from filinglens.finance.constants import METRIC_ALIASES


class FinancialMetricExtractor:
    """Extracts scalar properties directly matching label bounds locally via heuristics."""

    def __init__(self):
        # Establish regex patterns scanning labels alongside adjacent values elegantly.
        # E.g. "Net Sales of ₹ 2453" -> Match "Net Sales", Match "₹ 2453"
        aliases = sorted(METRIC_ALIASES.keys(), key=len, reverse=True)
        self.metric_pattern = re.compile(
            r"\b("
            + "|".join(aliases)
            + r")\b[:\s]*(?:of|stood at|was|is)?\s*([$₹]?[\s\d,\.]+(?:crore|lakh|million|mn|bn|billion)?)",
            re.IGNORECASE,
        )

    def extract_from_chunk(self, chunk: DocumentChunk) -> list[FinancialMetric]:
        extracted = []
        text = chunk.text

        matches = self.metric_pattern.finditer(text)
        for match in matches:
            raw_metric_label = match.group(1)
            raw_value_span = match.group(2)

            val, unit, currency = parse_financial_value(raw_value_span)

            if val is not None:
                metric = FinancialMetric(
                    company=chunk.company,
                    year=chunk.year,
                    statement="Unknown",
                    metric=normalize_metric_name(raw_metric_label),
                    value=val,
                    unit=unit if unit else "",
                    currency=currency if currency else "",
                    page=chunk.page,
                    source_text=match.group(0),
                )
                extracted.append(metric)

        return extracted
