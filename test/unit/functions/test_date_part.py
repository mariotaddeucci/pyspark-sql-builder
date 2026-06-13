from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_date_part() -> None:
    c = F.date_part("YEAR", F.col("d"))
    assert c._expr == "DATE_PART('YEAR', `d`)"
