from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_concat() -> None:
    """
    PySpark docstring example:
    >>> concat(col("first"), lit(" "), col("last"))
    Concatenates multiple columns together.
    """
    c = F.concat(F.col("first"), F.lit(" "), F.col("last"))
    assert c._expr == "CONCAT(`first`, ' ', `last`)"
