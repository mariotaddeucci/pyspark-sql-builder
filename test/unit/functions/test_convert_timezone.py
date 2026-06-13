from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_convert_timezone() -> None:
    c = F.convert_timezone("UTC", "PST", F.col("ts"))
    assert c._expr == "CONVERT_TIMEZONE('UTC', 'PST', `ts`)"
