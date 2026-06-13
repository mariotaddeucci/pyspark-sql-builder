from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_approx_count_distinct() -> None:
    c = F.approx_count_distinct(F.col("x"))
    assert isinstance(c._expr, str)
    assert len(c._expr) > 0
