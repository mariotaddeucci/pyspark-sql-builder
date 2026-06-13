from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_instr() -> None:
    c = F.instr(F.col("x"), "sub")
    assert c._expr == "INSTR(`x`, 'sub')"
