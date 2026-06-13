from __future__ import annotations

from pyspark_sql_builder import functions as F


def test_aes_decrypt() -> None:
    c = F.aes_decrypt(F.col("x"), "key")
    assert c._expr == "AES_DECRYPT(`x`, 'key')"
