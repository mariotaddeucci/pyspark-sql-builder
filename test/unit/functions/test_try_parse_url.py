from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_try_parse_url() -> None:
    c = F.try_parse_url(F.col("url"), "HOST")
    assert c._expr == "TRY_PARSE_URL(`url`, 'HOST')"
