from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_dense_rank() -> None:
    c = F.dense_rank()
    assert isinstance(c._expr, str)
    assert len(c._expr) > 0
