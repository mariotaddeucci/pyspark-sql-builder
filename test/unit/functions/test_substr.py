from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_substr() -> None:
    c = F.substr(F.col("x"), 2)
    assert c._expr == "SUBSTRING(`x`, 2)"
