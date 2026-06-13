from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_xpath_boolean() -> None:
    c = F.xpath_boolean(F.col("xml"), "/path")
    assert c._expr == "XPATH_BOOLEAN(`xml`, '/path')"
