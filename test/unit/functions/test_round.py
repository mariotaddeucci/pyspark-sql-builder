from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_round() -> None:
    """
    PySpark docstring example:
    >>> df.select(round(col("price"), 2)).show()
    Rounds a numeric column to the specified number of decimal places.
    """
    c = F.round(F.col("price"), 2)
    assert c._expr == "ROUND(`price`, 2)"
