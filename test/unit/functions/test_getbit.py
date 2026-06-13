from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_getbit() -> None:
    c = F.getbit(F.col("x"), 3)
    assert c._expr == "GETBIT(`x`, 3)"
