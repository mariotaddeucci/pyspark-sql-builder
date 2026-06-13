from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_make_date() -> None:
    c = F.make_date(2024, 3, 15)
    assert c._expr == "MAKE_DATE(2024, 3, 15)"
