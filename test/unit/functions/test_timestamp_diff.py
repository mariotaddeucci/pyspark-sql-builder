from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_timestamp_diff() -> None:
    c = F.timestamp_diff("SECOND", F.col("start"), F.col("end"))
    assert c._expr == "TIMESTAMPDIFF(SECOND, `start`, `end`)"
