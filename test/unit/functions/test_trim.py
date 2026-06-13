from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_trim() -> None:
    """
    PySpark docstring example:
    >>> df.select(trim(col("name"))).show()
    Trims leading and trailing spaces from a string column.
    """
    c = F.trim(F.col("name"))
    assert c._expr == "TRIM(`name`)"


def test_ltrim() -> None:
    """
    PySpark docstring example:
    >>> df.select(ltrim(col("name"))).show()
    Trims leading spaces from a string column.
    """
    c = F.ltrim(F.col("name"))
    assert c._expr == "LTRIM(`name`)"


def test_rtrim() -> None:
    """
    PySpark docstring example:
    >>> df.select(rtrim(col("name"))).show()
    Trims trailing spaces from a string column.
    """
    c = F.rtrim(F.col("name"))
    assert c._expr == "RTRIM(`name`)"
