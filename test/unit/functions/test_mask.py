from __future__ import annotations

import pytest

from pyspark_sql_builder import functions as F


def test_mask_not_implemented() -> None:
    with pytest.raises(NotImplementedError):
        F.mask(F.col("x"))
