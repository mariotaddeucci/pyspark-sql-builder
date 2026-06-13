from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_filter() -> None:
    c = F.filter(F.col("a"), "x -> x > 0")
    assert c._expr == "FILTER(`a`, x -> x > 0)"
