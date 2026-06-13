from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import BaseModel, ConfigDict, Field, SecretStr

from pyspark_sql_builder.dataframe import DataFrame
from pyspark_sql_builder.readwriter import DataFrameReader, DataFrameWriter

if TYPE_CHECKING:
    from pyspark_sql_builder.drivers import DatabaseDriver


class InternalSettings(BaseModel):
    model_config = ConfigDict(extra="forbid")

    dialect: str = Field(
        default="spark",
        description=(
            "The SQL dialect for session operations"
            " (Session.sql, functions.expr, DataFrame.from_sql, etc)"
        ),
    )
    connection: SecretStr | None = Field(
        default=None,
        description="The database URL. Required for certain dialects.",
    )

    @property
    def target_dialect(self) -> str:
        if self.connection is None:
            return self.dialect
        driver = self.connection.get_secret_value().split(":")[0]
        return driver


class SessionSettings(BaseModel):
    app_name: str = Field(
        default="pyspark-sql-builder", description="The name of the application."
    )
    internal: InternalSettings = Field(
        default_factory=InternalSettings,
        description="Internal settings for the SparkSession.",
    )


class SparkSession:
    def __init__(
        self,
        settings: SessionSettings | None = None,
        **kwargs: Any,
    ) -> None:
        self._driver: DatabaseDriver | None = None
        if settings is not None:
            self._settings = settings
        else:
            internal_kwargs: dict[str, Any] = {}
            if "dialect" in kwargs:
                internal_kwargs["dialect"] = kwargs.pop("dialect")
            if "connection" in kwargs:
                internal_kwargs["connection"] = kwargs.pop("connection")
            if internal_kwargs:
                kwargs["internal"] = internal_kwargs
            self._settings = SessionSettings.model_validate(kwargs)

    def _get_driver(self) -> DatabaseDriver:
        if self._driver is None:
            from pyspark_sql_builder.drivers import get_driver

            conn = self._settings.internal.connection
            if conn is None:
                raise RuntimeError("No connection string configured on SparkSession")
            self._driver = get_driver(conn.get_secret_value())
        return self._driver

    @property
    def dialect(self) -> str:
        return self._settings.internal.dialect

    @property
    def target_dialect(self) -> str:
        return self._settings.internal.target_dialect

    @property
    def read(self) -> DataFrameReader:
        return DataFrameReader(self)

    @property
    def writer(self) -> DataFrameWriter:
        return DataFrameWriter(self)

    def table(self, table_name: str) -> DataFrame:
        return DataFrame(f"SELECT * FROM {table_name}", session=self)

    def sql(self, query: str) -> DataFrame:
        return DataFrame(query, session=self)

    def range(self, start: int, end: int, step: int = 1) -> DataFrame:
        return DataFrame(
            f"SELECT id FROM range({start}, {end}, {step})",
            session=self,
        )

    def to_arrow_reader(self, query: str) -> Any:
        return self._get_driver().query(query)

    class Builder:
        _internal_settings_prefix = "internal"

        def __init__(self) -> None:
            self._settings_map: dict[str, Any] = {"internal": {}}

        def app_name(self, name: str) -> SparkSession.Builder:
            self._settings_map["app_name"] = name
            return self

        def config(self, key: str, value: str) -> SparkSession.Builder:
            if key.startswith(self._internal_settings_prefix + "."):
                internal_key = key[len(self._internal_settings_prefix) + 1 :]
                self._settings_map["internal"][internal_key] = value
            else:
                self._settings_map[key] = value

            return self

        def getOrCreate(self) -> SparkSession:
            settings = SessionSettings.model_validate(self._settings_map)
            return SparkSession(settings=settings)

    builder: Builder = Builder()
