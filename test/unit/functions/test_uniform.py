from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_uniform() -> None:
    c = F.uniform(0.0, 1.0)
    assert c._expr == "UNIFORM(0.0, 1.0)"
