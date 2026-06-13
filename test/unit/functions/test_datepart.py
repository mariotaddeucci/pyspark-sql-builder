from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_datepart() -> None:
    c = F.datepart("YEAR", F.col("d"))
    assert c._expr == "DATE_PART('YEAR', `d`)"
