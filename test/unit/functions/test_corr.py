from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_corr() -> None:
    c = F.corr(F.col("x"), F.col("y"))
    assert c._expr == "CORR(`x`, `y`)"
