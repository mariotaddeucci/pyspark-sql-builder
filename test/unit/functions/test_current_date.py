from __future__ import annotations

from pyspark_sql_builder.pyspark.sql import functions as F


def test_current_date() -> None:
    """
    PySpark docstring example:
    >>> df.select(current_date())
    Returns the current date as a date column.
    """
    c = F.current_date()
    assert c._expr == "CURRENT_DATE"
