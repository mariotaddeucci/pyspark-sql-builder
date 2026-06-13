from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_hll_union() -> None:
    c = F.hll_union(F.col("a"), F.col("b"))
    assert c._expr == "HLL_UNION(`a`, `b`)"
