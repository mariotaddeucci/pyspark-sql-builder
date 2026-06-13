from __future__ import annotations

from pathlib import Path

import pyarrow.csv as pa_csv
import pyarrow.json as pa_json
import pyarrow.parquet as pa_parquet
import pytest

from pyspark_sql_builder.session import SparkSession


def test_write_csv(spark: SparkSession, tmp_path: Path) -> None:
    df = spark.table("users").select("name", "email").orderBy("name")
    path = str(tmp_path / "users.csv")
    df.write.csv(path, header=True)
    table = pa_csv.read_csv(path)
    assert table.column_names == ["name", "email"]
    assert table.num_rows == 3
    assert table.column("name").to_pylist() == ["Joao", "Maria", "Pedro"]


def test_write_csv_without_header(spark: SparkSession, tmp_path: Path) -> None:
    df = spark.table("users").select("name", "email").orderBy("name")
    path = str(tmp_path / "users_no_header.csv")
    df.write.option("header", False).csv(path)
    table = pa_csv.read_csv(
        path,
        read_options=pa_csv.ReadOptions(column_names=["name", "email"]),
    )
    assert table.num_rows == 3


def test_write_csv_gzip_compression(spark: SparkSession, tmp_path: Path) -> None:
    df = spark.table("users").select("name", "email").orderBy("name")
    path = str(tmp_path / "users.csv.gz")
    df.write.option("compression", "gzip").csv(path, header=True)
    import gzip

    with gzip.open(path, "rb") as f:
        content = f.read()
    assert b"Joao" in content
    assert b"Maria" in content
    assert b"Pedro" in content


def test_write_csv_bzip2_compression(spark: SparkSession, tmp_path: Path) -> None:
    df = spark.table("users").select("name", "email").orderBy("name")
    path = str(tmp_path / "users.csv.bz2")
    df.write.option("compression", "bzip2").csv(path, header=True)
    import bz2

    with bz2.open(path, "rb") as f:
        content = f.read()
    assert b"Joao" in content


def test_write_json(spark: SparkSession, tmp_path: Path) -> None:
    df = spark.table("users").select("name", "email").orderBy("name")
    path = str(tmp_path / "users.json")
    df.write.json(path)
    table = pa_json.read_json(path)
    assert table.num_rows == 3
    assert table.column("name").to_pylist() == ["Joao", "Maria", "Pedro"]


def test_write_json_gzip_compression(spark: SparkSession, tmp_path: Path) -> None:
    df = spark.table("users").select("name", "email").orderBy("name")
    path = str(tmp_path / "users.json.gz")
    df.write.option("compression", "gzip").json(path)
    import gzip

    with gzip.open(path, "rb") as f:
        content = f.read()
    assert b"Joao" in content


def test_write_json_zstd_compression(spark: SparkSession, tmp_path: Path) -> None:
    df = spark.table("users").select("name", "email").orderBy("name")
    path = str(tmp_path / "users.json.zst")
    df.write.option("compression", "zstd").json(path)
    import duckdb

    con = duckdb.connect()
    table = con.execute(
        f"SELECT * FROM read_json_auto('{path}'::TEXT)"
    ).to_arrow_table()
    con.close()
    assert table.num_rows == 3


def test_write_parquet(spark: SparkSession, tmp_path: Path) -> None:
    df = spark.table("users").select("name", "email").orderBy("name")
    path = str(tmp_path / "users.parquet")
    df.write.parquet(path)
    table = pa_parquet.read_table(path)
    assert table.num_rows == 3
    assert table.column("name").to_pylist() == ["Joao", "Maria", "Pedro"]


def test_write_parquet_uncompressed(spark: SparkSession, tmp_path: Path) -> None:
    df = spark.table("users").select("name", "email").orderBy("name")
    path = str(tmp_path / "users_uncompressed.parquet")
    df.write.option("compression", "none").parquet(path)
    table = pa_parquet.read_table(path)
    assert table.num_rows == 3


def test_write_parquet_gzip_compression(spark: SparkSession, tmp_path: Path) -> None:
    df = spark.table("users").select("name", "email").orderBy("name")
    path = str(tmp_path / "users_gzip.parquet")
    df.write.option("compression", "gzip").parquet(path)
    table = pa_parquet.read_table(path)
    assert table.num_rows == 3


def test_write_parquet_zstd_compression(spark: SparkSession, tmp_path: Path) -> None:
    df = spark.table("users").select("name", "email").orderBy("name")
    path = str(tmp_path / "users_zstd.parquet")
    df.write.option("compression", "zstd").parquet(path)
    table = pa_parquet.read_table(path)
    assert table.num_rows == 3


def test_write_csv_unsupported_compression(spark: SparkSession, tmp_path: Path) -> None:
    df = spark.table("users").select("name")
    path = str(tmp_path / "bad.csv")
    with pytest.raises(
        ValueError, match="Unsupported compression codec for CSV: 'snappy'"
    ):
        df.write.option("compression", "snappy").csv(path)


def test_write_parquet_unsupported_compression(
    spark: SparkSession, tmp_path: Path
) -> None:
    df = spark.table("users").select("name")
    path = str(tmp_path / "bad.parquet")
    with pytest.raises(
        ValueError, match="Unsupported compression codec for Parquet: 'bzip2'"
    ):
        df.write.option("compression", "bzip2").parquet(path)


def test_write_json_unsupported_compression(
    spark: SparkSession, tmp_path: Path
) -> None:
    df = spark.table("users").select("name")
    path = str(tmp_path / "bad.json")
    with pytest.raises(
        ValueError, match="Unsupported compression codec for JSON: 'snappy'"
    ):
        df.write.option("compression", "snappy").json(path)


def test_write_format_csv_save(spark: SparkSession, tmp_path: Path) -> None:
    df = spark.table("users").select("name", "email").orderBy("name")
    path = str(tmp_path / "users_format.csv")
    df.write.format("csv").option("header", True).save(path)
    table = pa_csv.read_csv(path)
    assert table.num_rows == 3


def test_write_format_parquet_save(spark: SparkSession, tmp_path: Path) -> None:
    df = spark.table("users").select("name", "email").orderBy("name")
    path = str(tmp_path / "users_format.parquet")
    df.write.format("parquet").save(path)
    table = pa_parquet.read_table(path)
    assert table.num_rows == 3
