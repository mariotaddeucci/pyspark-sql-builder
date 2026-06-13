from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_json_tuple() -> None:
    c = F.json_tuple(F.col("j"), "f1", "f2")
    assert c._expr == "JSON_TUPLE(`j`, 'f1', 'f2')"
