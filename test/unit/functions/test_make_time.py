from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_make_time() -> None:
    c = F.make_time(10, 30, 45)
    assert c._expr == "MAKE_TIME(10, 30, 45)"
