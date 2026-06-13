from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_min_column() -> None:
    """
    PySpark docstring Example 1:
    Compute the minimum value of a numeric column.
    >>> df.select(sf.min(df.id)).show()
    """
    c = F.min(F.col("date"))
    assert c._expr == "MIN(`date`)"


def test_min_string_col() -> None:
    """
    PySpark docstring Example 2:
    Compute the minimum value of a string column.
    >>> df.select(sf.min("name")).show()
    Note: string column names are auto-backtick-quoted.
    """
    c = F.min("name")
    assert c._expr == "MIN(`name`)"
