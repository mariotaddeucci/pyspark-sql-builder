from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_try_variant_get() -> None:
    c = F.try_variant_get(F.col("x"), "$.key", "INT")
    assert c._expr == "TRY_VARIANT_GET(`x`, '$.key', 'INT')"
