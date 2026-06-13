from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_cume_dist() -> None:
    c = F.cume_dist()
    assert isinstance(c._expr, str)
    assert len(c._expr) > 0
