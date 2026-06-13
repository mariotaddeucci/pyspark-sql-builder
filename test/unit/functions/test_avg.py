from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_avg_column() -> None:
    """
    PySpark docstring Example 1:
    Calculating the average age.
    >>> df.select(sf.avg("age")).show()
    """
    c = F.avg(F.col("price"))
    assert c._expr == "AVG(`price`)"


def test_avg_string_col() -> None:
    """
    PySpark docstring Example 2:
    Calculating the average age with None.
    >>> df.select(sf.avg("age")).show()
    Note: string column names are auto-backtick-quoted.
    """
    c = F.avg("age")
    assert c._expr == "AVG(`age`)"
