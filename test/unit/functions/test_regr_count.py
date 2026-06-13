from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_regr_count() -> None:
    c = F.regr_count(F.col("x"), F.col("y"))
    assert c._expr == "REGR_COUNT(`x`, `y`)"
