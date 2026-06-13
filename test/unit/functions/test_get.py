from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_get() -> None:
    c = F.get(F.col("a"), 0)
    assert c._expr == "`a`[0]"
