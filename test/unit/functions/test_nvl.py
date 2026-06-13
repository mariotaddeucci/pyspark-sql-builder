from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_nvl() -> None:
    c = F.nvl(F.col("value"), 0)
    assert c._expr == "NVL(`value`, 0)"
