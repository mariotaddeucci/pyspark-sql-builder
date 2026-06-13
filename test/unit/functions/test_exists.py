from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_exists() -> None:
    c = F.exists(F.col("a"), "x -> x > 0")
    assert c._expr == "EXISTS(`a`, x -> x > 0)"
