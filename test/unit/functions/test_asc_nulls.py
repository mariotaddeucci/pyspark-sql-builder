from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_asc_nulls_first() -> None:
    c = F.asc_nulls_first(F.col("value"))
    assert c._expr == "`value` ASC NULLS FIRST"


def test_asc_nulls_last() -> None:
    c = F.asc_nulls_last(F.col("value"))
    assert c._expr == "`value` ASC NULLS LAST"


def test_desc_nulls_first() -> None:
    c = F.desc_nulls_first(F.col("value"))
    assert c._expr == "`value` DESC NULLS FIRST"


def test_desc_nulls_last() -> None:
    c = F.desc_nulls_last(F.col("value"))
    assert c._expr == "`value` DESC NULLS LAST"
