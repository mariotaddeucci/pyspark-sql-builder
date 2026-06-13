from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_monotonically_increasing_id() -> None:
    c = F.monotonically_increasing_id()
    assert isinstance(c._expr, str)
    assert len(c._expr) > 0
