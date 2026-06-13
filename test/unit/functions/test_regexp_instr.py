from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_regexp_instr() -> None:
    c = F.regexp_instr(F.col("x"), "\\d+")
    assert c._expr == "REGEXP_INSTR(`x`, '\\d+')"
