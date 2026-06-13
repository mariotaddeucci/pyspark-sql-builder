from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_max_column() -> None:
    """
    PySpark docstring Example 1:
    Compute the maximum value of a numeric column.
    >>> df.select(sf.max(df.age)).show()
    """
    c = F.max(F.col("score"))
    assert c._expr == "MAX(`score`)"


def test_max_string_col() -> None:
    """
    PySpark docstring Example 2:
    Compute the maximum value of a string column.
    >>> df.select(sf.max("salary")).show()
    Note: string column names are auto-backtick-quoted.
    """
    c = F.max("salary")
    assert c._expr == "MAX(`salary`)"
