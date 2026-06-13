from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_to_varchar() -> None:
    c = F.to_varchar(F.col("x"), "999")
    assert c._expr == "TO_VARCHAR(`x`, '999')"
