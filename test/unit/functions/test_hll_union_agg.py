from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_hll_union_agg() -> None:
    c = F.hll_union_agg(F.col("x"))
    assert isinstance(c._expr, str)
    assert len(c._expr) > 0
