from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_xpath_string() -> None:
    c = F.xpath_string(F.col("xml"), "/path")
    assert c._expr == "XPATH_STRING(`xml`, '/path')"
