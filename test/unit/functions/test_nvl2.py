from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_nvl2() -> None:
    c = F.nvl2(F.col("value"), "not null", "null")
    assert c._expr == "CASE WHEN `value` IS NOT NULL THEN 'not null' ELSE 'null' END"
