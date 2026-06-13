from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_make_timestamp_ntz() -> None:
    c = F.make_timestamp_ntz(2024, 3, 15, 10, 30, 45)
    assert c._expr == "MAKE_TIMESTAMP_NTZ(2024, 3, 15, 10, 30, 45)"
