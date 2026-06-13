from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_xpath_number() -> None:
    c = F.xpath_number(F.col("xml"), "/path")
    assert c._expr == "XPATH_NUMBER(`xml`, '/path')"
