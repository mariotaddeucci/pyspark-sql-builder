from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_schema_of_variant() -> None:
    c = F.schema_of_variant(F.col("x"))
    assert isinstance(c._expr, str)
    assert len(c._expr) > 0
