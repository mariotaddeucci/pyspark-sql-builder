from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_current_timestamp() -> None:
    """
    PySpark docstring example:
    >>> df.select(current_timestamp())
    Returns the current timestamp as a timestamp column.
    """
    c = F.current_timestamp()
    assert c._expr == "CURRENT_TIMESTAMP"
