from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_transform_keys() -> None:
    c = F.transform_keys(F.col("m"), "(k, v) -> k")
    assert c._expr == "TRANSFORM_KEYS(`m`, (k, v) -> k)"
