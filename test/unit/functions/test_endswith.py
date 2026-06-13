from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_endswith() -> None:
    c = F.endswith(F.col("x"), "suffix")
    assert c._expr == "`x` LIKE '%' || 'suffix'"
