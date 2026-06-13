from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_right() -> None:
    c = F.right(F.col("x"), 3)
    assert c._expr == "RIGHT(`x`, 3)"
