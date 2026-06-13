from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_abs() -> None:
    """
    PySpark docstring example:
    >>> df.select(abs(col("value"))).show()
    Computes the absolute value of a numeric column.
    """
    c = F.abs(F.col("value"))
    assert c._expr == "ABS(`value`)"
