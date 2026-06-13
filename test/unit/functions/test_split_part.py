from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_split_part() -> None:
    c = F.split_part(F.col("x"), ",", 2)
    assert c._expr == "SPLIT_PART(`x`, ',', 2)"
