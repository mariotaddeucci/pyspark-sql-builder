from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_make_timestamp() -> None:
    c = F.make_timestamp(2024, 3, 15, 10, 30, 45)
    assert c._expr == "MAKE_TIMESTAMP(2024, 3, 15, 10, 30, 45)"
