from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_str_to_map() -> None:
    c = F.str_to_map(F.col("x"))
    assert isinstance(c._expr, str)
    assert len(c._expr) > 0
