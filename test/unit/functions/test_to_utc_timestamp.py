from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_to_utc_timestamp() -> None:
    c = F.to_utc_timestamp(F.col("ts"), "PST")
    assert c._expr == "TO_UTC_TIMESTAMP(`ts`, 'PST')"
