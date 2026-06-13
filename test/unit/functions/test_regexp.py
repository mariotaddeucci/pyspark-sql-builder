from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_regexp() -> None:
    c = F.regexp(F.col("name"), "^foo.*")
    assert c._expr == "`name` RLIKE '^foo.*'"


def test_regexp_like() -> None:
    c = F.regexp_like(F.col("name"), "^foo.*")
    assert c._expr == "`name` RLIKE '^foo.*'"


def test_rlike() -> None:
    c = F.rlike(F.col("name"), "^foo.*")
    assert c._expr == "`name` RLIKE '^foo.*'"
