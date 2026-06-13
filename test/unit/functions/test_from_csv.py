from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_from_csv() -> None:
    c = F.from_csv(F.col("val"), "a INT")
    assert c._expr == "FROM_CSV(`val`, 'a INT')"
