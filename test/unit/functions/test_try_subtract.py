from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_try_subtract() -> None:
    c = F.try_subtract(F.col("a"), F.col("b"))
    assert c._expr == "`a` - `b`"
