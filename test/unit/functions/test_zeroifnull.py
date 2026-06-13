from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_zeroifnull() -> None:
    c = F.zeroifnull(F.col("value"))
    assert c._expr == "COALESCE(`value`, 0)"
