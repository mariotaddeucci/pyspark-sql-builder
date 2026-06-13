from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_elt() -> None:
    c = F.elt(1, F.col("a"), F.col("b"))
    assert c._expr == "ELT(1, `a`, `b`)"
