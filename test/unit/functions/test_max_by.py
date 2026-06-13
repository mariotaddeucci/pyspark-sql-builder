from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_max_by() -> None:
    c = F.max_by(F.col("x"), F.col("y"))
    assert c._expr == "MAX_BY(`x`, `y`)"
