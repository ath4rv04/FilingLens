from dataclasses import dataclass


@dataclass(slots=True)
class FinancialMetric:
    company: str
    year: str
    statement: str
    metric: str
    value: float
    unit: str
    currency: str
    page: int
    source_text: str


@dataclass(slots=True)
class BalanceSheetItem(FinancialMetric):
    pass


@dataclass(slots=True)
class IncomeStatementItem(FinancialMetric):
    pass


@dataclass(slots=True)
class CashFlowItem(FinancialMetric):
    pass


@dataclass(slots=True)
class FinancialRatio(FinancialMetric):
    pass


@dataclass(slots=True)
class SegmentRevenue(FinancialMetric):
    segment: str
