from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_date_diff() -> None:
    c = F.date_diff(F.col("end"), F.col("start"))
    assert c._expr == "DATEDIFF(`end`, `start`)"
