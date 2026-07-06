from filinglens.finance.models import FinancialMetric


def test_financial_metric_instantiation():
    metric = FinancialMetric(
        company="TCS",
        year="FY2024",
        statement="Income Statement",
        metric="Revenue",
        value=245315.0,
        unit="crore",
        currency="INR",
        page=117,
        source_text="Revenue was ₹245,315 crore",
    )
    assert metric.company == "TCS"
    assert metric.value == 245315.0
