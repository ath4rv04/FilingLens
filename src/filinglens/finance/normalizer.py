def normalize_metric_name(raw_name: str) -> str:
    """Normalize equivalent financial labels into unified semantic descriptors."""
    from filinglens.finance.constants import METRIC_ALIASES

    cleaned = raw_name.lower().strip()
    return METRIC_ALIASES.get(cleaned, raw_name.title())
