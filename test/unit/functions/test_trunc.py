from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_trunc() -> None:
    c = F.trunc(F.col("d"), "MONTH")
    assert c._expr == "TRUNC(`d`, 'MONTH')"
