from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_radians() -> None:
    c = F.radians(F.col("x"))
    assert isinstance(c._expr, str)
    assert len(c._expr) > 0
