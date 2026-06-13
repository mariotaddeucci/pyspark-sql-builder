from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_upper() -> None:
    """
    PySpark docstring example:
    >>> df.select(upper(col("name"))).show()
    Converts a string column to upper case.
    """
    c = F.upper(F.col("name"))
    assert c._expr == "UPPER(`name`)"
