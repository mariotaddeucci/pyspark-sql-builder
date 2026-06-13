from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_dateadd() -> None:
    c = F.dateadd(F.col("d"), 5)
    assert c._expr == "DATE_ADD(`d`, 5)"
