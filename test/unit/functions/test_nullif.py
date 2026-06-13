from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_nullif() -> None:
    c = F.nullif(F.col("value"), 0)
    assert c._expr == "NULLIF(`value`, 0)"


def test_nullif_with_string() -> None:
    c = F.nullif(F.col("name"), "unknown")
    assert c._expr == "NULLIF(`name`, 'unknown')"
