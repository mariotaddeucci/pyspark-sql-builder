from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_date_from_unix_date() -> None:
    c = F.date_from_unix_date(F.col("x"))
    assert isinstance(c._expr, str)
    assert len(c._expr) > 0
