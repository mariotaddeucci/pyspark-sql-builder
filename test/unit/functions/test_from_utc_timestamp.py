from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_from_utc_timestamp() -> None:
    c = F.from_utc_timestamp(F.col("ts"), "PST")
    assert c._expr == "FROM_UTC_TIMESTAMP(`ts`, 'PST')"
