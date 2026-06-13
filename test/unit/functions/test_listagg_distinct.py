from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_listagg_distinct() -> None:
    c = F.listagg_distinct(F.col("x"), ",")
    assert c._expr == "LISTAGG(DISTINCT `x`, ',')"
