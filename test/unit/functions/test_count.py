from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_count_star() -> None:
    """
    PySpark docstring Example 1:
    Count all rows in a DataFrame.
    >>> df.select(sf.count(sf.expr("*"))).show()
    """
    c = F.count()
    assert c._expr == "COUNT(*)"


def test_count_column() -> None:
    """
    PySpark docstring Example 2:
    Count non-null values in a specific column.
    >>> df.select(sf.count(df.alphabets)).show()
    """
    c = F.count(F.col("id"))
    assert c._expr == "COUNT(`id`)"


def test_count_distinct() -> None:
    c = F.countDistinct(F.col("category"))
    assert c._expr == "COUNT(DISTINCT `category`)"


def test_count_multiple() -> None:
    """
    PySpark docstring Example 4:
    Count non-null values in multiple columns.
    >>> df.select(sf.count(df.id), sf.count(df.fruit)).show()
    """
    c1 = F.count(F.col("id"))
    c2 = F.count(F.col("fruit"))
    assert c1._expr == "COUNT(`id`)"
    assert c2._expr == "COUNT(`fruit`)"
