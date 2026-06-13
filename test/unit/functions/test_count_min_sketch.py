from __future__ import annotations

import pytest

from pyspark_sql_builder import functions as F


def test_count_min_sketch_not_implemented() -> None:
    with pytest.raises(NotImplementedError):
        F.count_min_sketch(F.col("x"), 0.1, 0.95, 42)
