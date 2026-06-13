from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_spark_partition_id() -> None:
    c = F.spark_partition_id()
    assert isinstance(c._expr, str)
    assert len(c._expr) > 0
