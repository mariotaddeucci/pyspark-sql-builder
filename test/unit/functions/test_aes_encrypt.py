from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_aes_encrypt() -> None:
    c = F.aes_encrypt(F.col("x"), "key")
    assert c._expr == "AES_ENCRYPT(`x`, 'key')"
