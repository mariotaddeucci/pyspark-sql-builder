from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_try_to_number() -> None:
    c = F.try_to_number(F.col("x"), "999")
    assert c._expr == "TRY_TO_NUMBER(`x`, '999')"
