from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_xpath_short() -> None:
    c = F.xpath_short(F.col("xml"), "/path")
    assert c._expr == "XPATH_SHORT(`xml`, '/path')"
