from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_extract() -> None:
    c = F.extract("year", F.col("d"))
    assert c._expr == "EXTRACT(YEAR FROM `d`)"
