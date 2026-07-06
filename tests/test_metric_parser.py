from filinglens.finance.parser import parse_financial_value


def test_parse_financial_value_extracts_cr():
    val, unit, currency = parse_financial_value("₹245,315 crore")
    assert val == 245315.0
    assert unit == "crore"
    assert currency == "INR"


def test_parse_financial_value_extracts_million():
    val, unit, currency = parse_financial_value("2,453 million")
    assert val == 2453.0
    assert unit == "million"
    assert currency is None


def test_parse_financial_value_extracts_bn():
    val, unit, currency = parse_financial_value("245.3 bn")
    assert val == 245.3
    assert unit == "billion"
    assert currency is None


def test_parse_financial_value_extracts_decimals():
    val, unit, currency = parse_financial_value("₹2.45 lakh crore")
    assert val == 2.45
    assert unit == "crore"  # Note: simple rule matcher takes first match.
    assert currency == "INR"
