import sqlite3
from typing import Optional
from pathlib import Path

from filinglens.finance.models import FinancialMetric


class FinanceRepository:
    """Stores financial extractions cleanly targeting standard SQLite implementations avoiding vector complexities."""

    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._init_db()

    def _get_conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._get_conn() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    company TEXT NOT NULL,
                    year TEXT NOT NULL,
                    statement TEXT,
                    metric TEXT NOT NULL,
                    value REAL NOT NULL,
                    unit TEXT,
                    currency TEXT,
                    page INTEGER,
                    source_text TEXT
                )
            """)

    def save(self, metric: FinancialMetric) -> None:
        with self._get_conn() as conn:
            conn.execute(
                """
                INSERT INTO metrics (company, year, statement, metric, value, unit, currency, page, source_text)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    metric.company,
                    metric.year,
                    metric.statement,
                    metric.metric,
                    metric.value,
                    metric.unit,
                    metric.currency,
                    metric.page,
                    metric.source_text,
                ),
            )

    def save_many(self, metrics: list[FinancialMetric]) -> None:
        with self._get_conn() as conn:
            conn.executemany(
                """
                INSERT INTO metrics (company, year, statement, metric, value, unit, currency, page, source_text)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                [
                    (
                        m.company,
                        m.year,
                        m.statement,
                        m.metric,
                        m.value,
                        m.unit,
                        m.currency,
                        m.page,
                        m.source_text,
                    )
                    for m in metrics
                ],
            )

    def find(
        self, company: str, year: str, metric_name: str
    ) -> Optional[FinancialMetric]:
        with self._get_conn() as conn:
            row = conn.execute(
                """
                SELECT * FROM metrics 
                WHERE company = ? AND year = ? AND metric = ?
                LIMIT 1
            """,
                (company, year, metric_name),
            ).fetchone()

            if row:
                return FinancialMetric(
                    company=row["company"],
                    year=row["year"],
                    statement=row["statement"],
                    metric=row["metric"],
                    value=row["value"],
                    unit=row["unit"],
                    currency=row["currency"],
                    page=row["page"],
                    source_text=row["source_text"],
                )
        return None

    def list_metrics(self, company: str, year: str) -> list[FinancialMetric]:
        results = []
        with self._get_conn() as conn:
            rows = conn.execute(
                """
                SELECT * FROM metrics 
                WHERE company = ? AND year = ?
            """,
                (company, year),
            ).fetchall()

            for row in rows:
                results.append(
                    FinancialMetric(
                        company=row["company"],
                        year=row["year"],
                        statement=row["statement"],
                        metric=row["metric"],
                        value=row["value"],
                        unit=row["unit"],
                        currency=row["currency"],
                        page=row["page"],
                        source_text=row["source_text"],
                    )
                )
        return results

    def compare(
        self, metric: str, companies: list[str] = None, years: list[str] = None
    ) -> list[FinancialMetric]:
        query = "SELECT * FROM metrics WHERE metric = ?"
        params = [metric]

        if companies:
            placeholders = ",".join(["?"] * len(companies))
            query += f" AND company IN ({placeholders})"
            params.extend(companies)

        if years:
            placeholders = ",".join(["?"] * len(years))
            query += f" AND year IN ({placeholders})"
            params.extend(years)

        results = []
        with self._get_conn() as conn:
            rows = conn.execute(query, params).fetchall()
            for row in rows:
                results.append(
                    FinancialMetric(
                        company=row["company"],
                        year=row["year"],
                        statement=row["statement"],
                        metric=row["metric"],
                        value=row["value"],
                        unit=row["unit"],
                        currency=row["currency"],
                        page=row["page"],
                        source_text=row["source_text"],
                    )
                )
        return results
