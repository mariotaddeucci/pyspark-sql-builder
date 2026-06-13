from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_hll_sketch_estimate() -> None:
    c = F.hll_sketch_estimate(F.col("x"))
    assert isinstance(c._expr, str)
    assert len(c._expr) > 0
