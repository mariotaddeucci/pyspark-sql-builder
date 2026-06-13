from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_schema_of_variant_agg() -> None:
    c = F.schema_of_variant_agg(F.col("x"))
    assert isinstance(c._expr, str)
    assert len(c._expr) > 0
