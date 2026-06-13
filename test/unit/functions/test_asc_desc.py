from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_asc() -> None:
    """
    PySpark docstring example:
    >>> df.sort(asc("name"))
    Returns a sort expression for ascending order.
    """
    assert F.asc(F.col("name"))._expr == "`name` ASC"


def test_desc() -> None:
    """
    PySpark docstring example:
    >>> df.orderBy(desc("id"))
    Returns a sort expression for descending order.
    """
    assert F.desc(F.col("name"))._expr == "`name` DESC"
