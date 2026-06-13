from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_listagg() -> None:
    c = F.listagg(F.col("x"), ",")
    assert c._expr == "LISTAGG(`x`, ',')"
