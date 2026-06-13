from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_translate() -> None:
    c = F.translate(F.col("x"), "abc", "xyz")
    assert c._expr == "TRANSLATE(`x`, 'abc', 'xyz')"
