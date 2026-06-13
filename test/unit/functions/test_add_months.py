from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_add_months() -> None:
    c = F.add_months(F.col("d"), 3)
    assert c._expr == "ADD_MONTHS(`d`, 3)"
