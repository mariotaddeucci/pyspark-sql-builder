from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_length() -> None:
    """
    PySpark docstring example:
    >>> df.select(length(col("text")).alias("len")).show()
    Computes the length of a string column.
    """
    c = F.length(F.col("text"))
    assert c._expr == "LENGTH(`text`)"
