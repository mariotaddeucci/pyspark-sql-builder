from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_try_add() -> None:
    c = F.try_add(F.col("a"), F.col("b"))
    assert c._expr == "`a` + `b`"
