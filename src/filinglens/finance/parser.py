import re
from typing import Optional


def parse_financial_value(
    raw_text: str,
) -> tuple[Optional[float], Optional[str], Optional[str]]:
    """
    Parses structural strings resolving numerical scalar, unit, and currency boundaries seamlessly.
    Example: '₹245,315 crore' -> 245315.0, 'crore', 'INR'
    """
    raw_lower = raw_text.lower().strip()

    currency = None
    if (
        "₹" in raw_text
        or "rs." in raw_lower
        or "inr" in raw_lower
        or "rupees" in raw_lower
    ):
        currency = "INR"
    elif "$" in raw_text or "usd" in raw_lower or "dollars" in raw_lower:
        currency = "USD"

    unit = None
    if "crore" in raw_lower or "cr." in raw_lower:
        unit = "crore"
    elif "lakh" in raw_lower:
        unit = "lakh"
    elif "billion" in raw_lower or "bn" in raw_lower:
        unit = "billion"
    elif "million" in raw_lower or "mn" in raw_lower:
        unit = "million"
    elif "thousand" in raw_lower:
        unit = "thousand"

    # Isolate number explicitly filtering out all alphanumeric units
    try:
        # Regex extracts numerals and decimal bounds avoiding textual characters
        match = re.search(
            r"[-+]?\d{1,3}(?:,\d{3})+(?:\.\d+)?|[-+]?\d+(?:\.\d+)?", raw_text
        )
        if match:
            clean_num_str = match.group().replace(",", "").replace(" ", "")
            return float(clean_num_str), unit, currency
    except Exception:
        pass

    return None, unit, currency
