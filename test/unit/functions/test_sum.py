from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_sum() -> None:
    """
    PySpark docstring Example 1:
    Calculating the sum of values in a column.
    >>> df.select(sf.sum(df["id"])).show()
    """
    c = F.sum(F.col("amount"))
    assert c._expr == "SUM(`amount`)"


def test_sum_string_col() -> None:
    """
    PySpark docstring Example 3:
    >>> df.select(sf.sum("age")).show()
    Note: string column names are auto-backtick-quoted.
    """
    c = F.sum("age")
    assert c._expr == "SUM(`age`)"
