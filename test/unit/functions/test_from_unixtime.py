from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_from_unixtime() -> None:
    c = F.from_unixtime(F.col("x"))
    assert c._expr == "FROM_UNIXTIME(`x`, 'yyyy-MM-dd HH:mm:ss')"
