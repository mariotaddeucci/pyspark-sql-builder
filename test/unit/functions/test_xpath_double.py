from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_xpath_double() -> None:
    c = F.xpath_double(F.col("xml"), "/path")
    assert c._expr == "XPATH_DOUBLE(`xml`, '/path')"
