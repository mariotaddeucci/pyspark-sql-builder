from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_hypot() -> None:
    c = F.hypot(F.col("a"), F.col("b"))
    assert c._expr == "SQRT(`a`*`a` + `b`*`b`)"
