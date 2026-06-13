from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_date_format() -> None:
    c = F.date_format(F.col("d"), "yyyy-MM-dd")
    assert c._expr == "DATE_FORMAT(`d`, 'yyyy-MM-dd')"
