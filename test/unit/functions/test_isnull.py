from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_isnull() -> None:
    c = F.isnull(F.col("value"))
    assert c._expr == "`value` IS NULL"
