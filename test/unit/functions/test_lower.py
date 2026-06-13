from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_lower() -> None:
    """
    PySpark docstring example:
    >>> df.select(lower(col("name"))).show()
    Converts a string column to lower case.
    """
    c = F.lower(F.col("name"))
    assert c._expr == "LOWER(`name`)"
