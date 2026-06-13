from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_nanvl() -> None:
    c = F.nanvl(F.col("value"), F.lit(0))
    assert c._expr == "IF(ISNAN(`value`), 0, `value`)"


def test_nanvl_with_literal() -> None:
    c = F.nanvl(F.col("x"), -1)
    assert c._expr == "IF(ISNAN(`x`), -1, `x`)"
