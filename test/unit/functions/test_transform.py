from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_transform() -> None:
    c = F.transform(F.col("a"), "x -> x + 1")
    assert c._expr == "TRANSFORM(`a`, x -> x + 1)"
