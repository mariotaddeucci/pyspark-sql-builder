from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_least() -> None:
    c = F.least(F.col("a"), F.col("b"))
    assert c._expr == "LEAST(`a`, `b`)"
