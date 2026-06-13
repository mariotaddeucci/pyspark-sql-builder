from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_nullifzero() -> None:
    c = F.nullifzero(F.col("value"))
    assert c._expr == "NULLIF(`value`, 0)"
