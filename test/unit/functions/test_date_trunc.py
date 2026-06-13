from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_date_trunc() -> None:
    c = F.date_trunc("MONTH", F.col("d"))
    assert c._expr == "DATE_TRUNC('MONTH', `d`)"
