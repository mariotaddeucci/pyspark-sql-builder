from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_coalesce() -> None:
    """
    PySpark docstring example:
    >>> c = coalesce(a, b, c)
    Returns the first non-null value among the columns.
    """
    c = F.coalesce(F.col("a"), F.col("b"), F.lit(0))
    assert c._expr == "COALESCE(`a`, `b`, 0)"
