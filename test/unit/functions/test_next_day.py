from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_next_day() -> None:
    c = F.next_day(F.col("d"), "Mon")
    assert c._expr == "NEXT_DAY(`d`, 'Mon')"
