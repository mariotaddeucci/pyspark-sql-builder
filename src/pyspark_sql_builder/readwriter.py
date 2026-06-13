from __future__ import annotations

from typing import TYPE_CHECKING, Any

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
            return DataFrameCls(path, session=self._session)
        return DataFrameCls(session=self._session)


class DataFrameWriter:
    def __init__(self, session: SparkSession) -> None:
        self._session = session

    def csv(self, path: str, **options: Any) -> None:
        pass

    def parquet(self, path: str) -> None:
        pass

    def json(self, path: str) -> None:
        pass

    def save(self, path: str | None = None) -> None:
        pass

    def format(self, source: str) -> DataFrameWriter:
        return self

    def option(self, key: str, value: Any) -> DataFrameWriter:
        return self

    def options(self, **options: Any) -> DataFrameWriter:
        return self

    def mode(self, save_mode: str) -> DataFrameWriter:
        return self
