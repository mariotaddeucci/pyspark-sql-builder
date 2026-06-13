from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_window() -> None:
    c = F.window(F.col("ts"), "1 hour")
    assert c._expr == "WINDOW(`ts`, '1 hour')"
