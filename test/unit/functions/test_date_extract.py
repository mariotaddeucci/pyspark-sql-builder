from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_year() -> None:
    """
    PySpark docstring example:
    >>> df.select(year(col("d")))
    Extracts the year from a date/timestamp column.
    """
    assert F.year(F.col("d"))._expr == "YEAR(`d`)"


def test_month() -> None:
    """
    PySpark docstring example:
    >>> df.select(month(col("d")))
    Extracts the month from a date/timestamp column.
    """
    assert F.month(F.col("d"))._expr == "MONTH(`d`)"


def test_day() -> None:
    """
    PySpark docstring example:
    >>> df.select(day(col("d")))
    Extracts the day of the month from a date/timestamp column.
    """
    assert F.day(F.col("d"))._expr == "DAY(`d`)"
