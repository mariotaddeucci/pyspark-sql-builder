from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_split() -> None:
    c = F.split(F.col("x"), ",")
    assert c._expr == "SPLIT(`x`, ',')"
