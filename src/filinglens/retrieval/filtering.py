import re
from filinglens.utils.logging import get_logger

logger = get_logger(__name__)

def normalize_company(company: str) -> str:
    """Normalize company targeting unified mapping strings."""
    if not company:
        return ""
        
    normalized = company.strip()
    logger.debug("Normalized company '%s' -> '%s'", company, normalized)
    return normalized

def normalize_year(year: str) -> str:
    """
    Supported year formats: FY2024, FY24, 2024, 2023-24, 2023/24
    Canonical -> 2024
    """
    if not year:
        return ""
        
    year = str(year).strip()
    match = re.search(r'(20\d{2}|\d{2})$', year)
    
    normalized = year
    if match:
        val = match.group(1)
        if len(val) == 4:
            normalized = val
        else:
            normalized = f"20{val}"
            
    logger.debug("Normalized year '%s' -> '%s'", year, normalized)
    return normalized

def normalize_filters(filters: dict | None) -> dict | None:
    if not filters:
        return None
    normalized = {}
    for k, v in filters.items():
        if k == "company":
            v = normalize_company(v)
        elif k == "year":
            v = normalize_year(v)
        normalized[k] = v
    return normalized

def build_qdrant_filter(filters: dict, models) -> 'Filter | None':
    """Build standardized Qdrant Filters seamlessly."""
    filters = normalize_filters(filters)
    if not filters:
        return None
        
    must_conditions = []
    
    for k, v in filters.items():
        if k == "company":
            v = normalize_company(v)
        elif k == "year":
            v = normalize_year(v)
            
        must_conditions.append(
            models.FieldCondition(
                key=k,
                match=models.MatchValue(value=v),
            )
        )
        
    if not must_conditions:
        return None
        
    return models.Filter(must=must_conditions)
