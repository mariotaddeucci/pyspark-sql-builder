from __future__ import annotations

import pytest

from pyspark_sql_builder.pyspark.sql import functions as F


def test_session_window_not_implemented() -> None:
    with pytest.raises(NotImplementedError):
        F.session_window(F.col("x"), "1 hour")
