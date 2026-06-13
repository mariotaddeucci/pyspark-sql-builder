from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_asc_nulls_last() -> None:
    c = F.asc_nulls_last(F.col("x"))
    assert isinstance(c._expr, str)
    assert len(c._expr) > 0
