from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_grouping_id() -> None:
    c = F.grouping_id(F.col("a"), F.col("b"))
    assert c._expr == "GROUPING_ID(`a`, `b`)"
