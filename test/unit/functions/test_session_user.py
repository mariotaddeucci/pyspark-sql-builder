from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_session_user() -> None:
    c = F.session_user()
    assert isinstance(c._expr, str)
    assert len(c._expr) > 0
