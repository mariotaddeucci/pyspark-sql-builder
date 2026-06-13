from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_make_dt_interval() -> None:
    c = F.make_dt_interval(days=1)
    assert c._expr == "MAKE_DT_INTERVAL(1, 0, 0, 0)"
