from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_make_ym_interval() -> None:
    c = F.make_ym_interval(years=1)
    assert c._expr == "MAKE_YM_INTERVAL(1, 0)"
