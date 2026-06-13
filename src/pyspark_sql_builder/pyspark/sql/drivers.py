from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Self

import duckdb
import pyarrow as pa


class DatabaseDriver(ABC):
    @classmethod
    @abstractmethod
    def create(cls, connection: str) -> Self: ...

    @abstractmethod
    def execute(self, query: str) -> None: ...

    @abstractmethod
    def query(self, query: str) -> pa.RecordBatchReader: ...


class DuckDBDriver(DatabaseDriver):
    def __init__(self, connection: duckdb.DuckDBPyConnection) -> None:
        self._conn = connection

    @classmethod
    def create(cls, connection: str) -> Self:
        connection = connection.removeprefix("duckdb://")
        conn = duckdb.connect(connection)
        return cls(conn)

    def execute(self, query: str) -> None:
        self._conn.execute(query)

    def query(self, query: str) -> pa.RecordBatchReader:
        cur = self._conn.execute(query)
        return cur.to_arrow_reader()


class ConnectorXDriver(DatabaseDriver):
    def __init__(self, connection: str) -> None:
        self._connection = connection

    @classmethod
    def create(cls, connection: str) -> Self:
        return cls(connection)

    def execute(self, query: str) -> None:
        import connectorx as cx

        cx.read_sql(self._connection, query)

    def query(self, query: str) -> pa.RecordBatchReader:
        import connectorx as cx

        table = cx.read_sql(self._connection, query, return_type="arrow")
        return table.to_reader()


def get_driver(connection: str) -> DatabaseDriver:
    if connection.startswith("duckdb://"):
        return DuckDBDriver.create(connection)
    return ConnectorXDriver.create(connection)
