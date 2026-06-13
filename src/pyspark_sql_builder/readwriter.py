from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pyarrow as pa
import pyarrow.csv as pa_csv
import pyarrow.parquet as pa_parquet

from pyspark_sql_builder.column import _quote_ident

if TYPE_CHECKING:
    from pyspark_sql_builder.dataframe import DataFrame
    from pyspark_sql_builder.session import SparkSession


class DataFrameReader:
    def __init__(self, session: SparkSession) -> None:
        self._session = session

    def table(self, table_name: str) -> DataFrame:
        return self._session.table(table_name)

    def csv(self, path: str, **options: Any) -> DataFrame:
        schema = options.get("schema", ["*"])
        cols = ", ".join(schema) if isinstance(schema, list) else "*"
        return self._session.table(f"read_csv_auto('{path}')").select(cols)

    def parquet(self, path: str) -> DataFrame:
        return self._session.table(f"parquet_scan('{path}')")

    def json(self, path: str) -> DataFrame:
        return self._session.table(f"read_json_auto('{path}')")

    def format(self, source: str) -> DataFrameReader:
        return self

    def option(self, key: str, value: Any) -> DataFrameReader:
        return self

    def options(self, **options: Any) -> DataFrameReader:
        return self

    def load(self, path: str | None = None) -> DataFrame:
        from pyspark_sql_builder.dataframe import DataFrame as DataFrameCls

        if path:
            sql = f"SELECT * FROM {_quote_ident(path)}"
            return DataFrameCls(sql, session=self._session)
        return DataFrameCls("SELECT 1", session=self._session)


class DataFrameWriter:
    def __init__(
        self,
        session: SparkSession,
        df: DataFrame | None = None,
    ) -> None:
        self._session = session
        self._df = df
        self._options: dict[str, Any] = {}
        self._format: str = ""

    def _get_reader(self) -> pa.RecordBatchReader:
        assert self._df is not None
        query = self._df.generate_query()
        return self._session.to_arrow_reader(query)

    def _get_compression(self) -> str | None:
        raw = self._options.get("compression", "none")
        if raw in ("none", "uncompressed", None):
            return None
        return str(raw)

    @staticmethod
    def _open_csv(path: str, compression: str | None) -> Any:
        if compression is None:
            return open(path, "wb")
        import bz2
        import gzip

        if compression in ("gzip", "deflate"):
            return gzip.open(path, "wb")
        if compression == "bzip2":
            return bz2.open(path, "wb")
        msg = f"Unsupported compression codec for CSV: '{compression}'"
        raise ValueError(msg)

    def csv(self, path: str, **options: Any) -> None:
        self._options.update(options)
        if self._df is None:
            return
        reader = self._get_reader()
        has_header = str(self._options.get("header", True)).lower() == "true"
        compression = self._get_compression()
        f = self._open_csv(path, compression)
        try:
            first = True
            for batch in reader:
                include = has_header and first
                opts = pa_csv.WriteOptions(include_header=include)
                pa_csv.write_csv(batch, f, write_options=opts)
                first = False
        finally:
            f.close()

    def parquet(self, path: str) -> None:
        if self._df is None:
            return
        reader = self._get_reader()
        compression = self._get_compression()
        cmp_map: dict[str | None, str | None] = {
            None: "snappy",
            "none": None,
            "uncompressed": None,
            "snappy": "snappy",
            "gzip": "gzip",
            "deflate": "gzip",
            "lz4": "lz4",
            "zstd": "zstd",
            "brotli": "brotli",
        }
        if compression not in cmp_map:
            msg = f"Unsupported compression codec for Parquet: '{compression}'"
            raise ValueError(msg)
        pq_compression = cmp_map[compression]
        writer: pa_parquet.ParquetWriter | None = None
        try:
            for batch in reader:
                if writer is None:
                    writer = pa_parquet.ParquetWriter(
                        path, batch.schema, compression=pq_compression
                    )
                writer.write_batch(batch)
        finally:
            if writer is not None:
                writer.close()

    def json(self, path: str) -> None:
        if self._df is None:
            return
        reader = self._get_reader()
        import duckdb

        con = duckdb.connect()
        con.register("_pyspark_json_tmp", reader)
        compression = self._get_compression()
        _json_codecs = {"gzip", "zstd"}
        if compression is not None and compression not in _json_codecs:
            msg = f"Unsupported compression codec for JSON: '{compression}'"
            raise ValueError(msg)
        copy_opts = ""
        if compression == "gzip":
            copy_opts = " (COMPRESSION gzip)"
        elif compression == "zstd":
            copy_opts = " (COMPRESSION zstd)"
        try:
            con.execute(f"COPY _pyspark_json_tmp TO '{path}'{copy_opts}")
        finally:
            con.close()

    def save(self, path: str | None = None) -> None:
        if self._df is None or path is None:
            return
        if self._format in ("csv",):
            self.csv(path)
        elif self._format in ("parquet",):
            self.parquet(path)
        elif self._format in ("json",):
            self.json(path)
        else:
            self.parquet(path)

    def format(self, source: str) -> DataFrameWriter:
        self._format = source
        return self

    def option(self, key: str, value: Any) -> DataFrameWriter:
        self._options[key] = value
        return self

    def options(self, **options: Any) -> DataFrameWriter:
        self._options.update(options)
        return self

    def mode(self, save_mode: str) -> DataFrameWriter:
        return self
