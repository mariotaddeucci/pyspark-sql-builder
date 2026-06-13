from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_current_timezone() -> None:
    c = F.current_timezone()
    assert isinstance(c._expr, str)
    assert len(c._expr) > 0
