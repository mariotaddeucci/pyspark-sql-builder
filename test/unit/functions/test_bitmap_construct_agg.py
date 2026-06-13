from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_bitmap_construct_agg() -> None:
    c = F.bitmap_construct_agg(F.col("x"))
    assert isinstance(c._expr, str)
    assert len(c._expr) > 0
