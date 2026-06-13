from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_try_make_timestamp() -> None:
    c = F.try_make_timestamp(2024, 3, 15, 10, 30, 45)
    assert c._expr == "TRY_MAKE_TIMESTAMP(2024, 3, 15, 10, 30, 45)"
