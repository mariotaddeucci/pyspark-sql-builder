from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_date_sub() -> None:
    c = F.date_sub(F.col("d"), 2)
    assert c._expr == "DATE_SUB(`d`, 2)"
