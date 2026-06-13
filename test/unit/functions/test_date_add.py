from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_date_add() -> None:
    c = F.date_add(F.col("d"), 2)
    assert c._expr == "DATE_ADD(`d`, 2)"
