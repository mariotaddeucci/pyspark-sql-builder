from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_isnan() -> None:
    c = F.isnan(F.col("value"))
    assert c._expr == "ISNAN(`value`)"
