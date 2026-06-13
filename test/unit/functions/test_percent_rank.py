from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_percent_rank() -> None:
    c = F.percent_rank()
    assert isinstance(c._expr, str)
    assert len(c._expr) > 0
