from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_xpath() -> None:
    c = F.xpath(F.col("xml"), "/path")
    assert c._expr == "XPATH(`xml`, '/path')"
