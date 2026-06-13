from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_parse_url() -> None:
    c = F.parse_url(F.col("url"), "HOST")
    assert c._expr == "PARSE_URL(`url`, 'HOST')"
