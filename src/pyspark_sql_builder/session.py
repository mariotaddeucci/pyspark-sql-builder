from __future__ import annotations

from pyspark_sql_builder.dataframe import DataFrame
from pyspark_sql_builder.readwriter import DataFrameReader, DataFrameWriter


class SparkSession:
    def __init__(self, dialect: str = "spark") -> None:
        self._dialect = dialect

    @property
    def dialect(self) -> str:
        return self._dialect

    @property
    def read(self) -> DataFrameReader:
        return DataFrameReader(self)

    @property
    def writer(self) -> DataFrameWriter:
        return DataFrameWriter(self)

    def table(self, table_name: str) -> DataFrame:
        return DataFrame(table_name, session=self)

    def sql(self, query: str) -> DataFrame:
        return DataFrame.from_sql(query, session=self)

    def range(self, start: int, end: int, step: int = 1) -> DataFrame:
        return DataFrame.from_sql(
            f"SELECT id FROM range({start}, {end}, {step})",
            session=self,
        )

    class Builder:
        def __init__(self) -> None:
            self._dialect: str = "spark"

        def app_name(self, name: str) -> SparkSession.Builder:
            return self

        def config(self, key: str, value: str) -> SparkSession.Builder:
            return self

        def getOrCreate(self) -> SparkSession:
            return SparkSession(dialect=self._dialect)

    builder: Builder = Builder()
