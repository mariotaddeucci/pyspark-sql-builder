from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_xpath_float() -> None:
    c = F.xpath_float(F.col("xml"), "/path")
    assert c._expr == "XPATH_FLOAT(`xml`, '/path')"
