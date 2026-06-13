from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_from_xml() -> None:
    c = F.from_xml(F.col("val"), "a INT")
    assert c._expr == "FROM_XML(`val`, 'a INT')"
