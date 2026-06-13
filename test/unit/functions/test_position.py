from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_position() -> None:
    c = F.position("sub", F.col("x"))
    assert c._expr == "POSITION('sub' IN `x`)"
