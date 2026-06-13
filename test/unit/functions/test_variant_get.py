from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_variant_get() -> None:
    c = F.variant_get(F.col("x"), "$.key", "INT")
    assert c._expr == "VARIANT_GET(`x`, '$.key', 'INT')"
