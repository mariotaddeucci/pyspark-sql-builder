from __future__ import annotations

from typing import TYPE_CHECKING

import polyglot_sql as _polyglot_sql
import pyarrow as pa

from pyspark_sql_builder.column import Column, _quote_ident
from pyspark_sql_builder.group import GroupedData

if TYPE_CHECKING:
    from pyspark_sql_builder.readwriter import DataFrameWriter
    from pyspark_sql_builder.session import SparkSession


class DataFrame:
    def __init__(
        self,
        query: str,
        session: SparkSession,
    ) -> None:
        self._query = query
        self._session = session

    @classmethod
    def from_rows(
        cls,
        rows: list[tuple],
        schema: list[str],
        session: SparkSession,
    ) -> DataFrame:
        values = ", ".join(
            f"({', '.join(repr(v) if isinstance(v, str) else str(v) for v in row)})"
            for row in rows
        )
        cols = ", ".join(schema)
        sql = f"SELECT {cols} FROM (VALUES {values}) AS t({cols})"
        return cls(sql, session)

    def _wrap(self, sql: str) -> DataFrame:
        return DataFrame(sql, self._session)

    def _replace_select(self, cols: str) -> DataFrame:
        upper = self._query.upper().lstrip()
        if upper.startswith("SELECT "):
            from_idx = self._query.upper().find(" FROM ")
            if from_idx != -1:
                new_query = f"SELECT {cols}{self._query[from_idx:]}"
                return DataFrame(new_query, self._session)
        return self._wrap(f"SELECT {cols} FROM ({self._query}) AS _t")

    def select(self, *columns: Column | str) -> DataFrame:
        cols = ", ".join(
            Column(_quote_ident(c))._expr if isinstance(c, str) else c._expr
            for c in columns
        )
        return self._replace_select(cols)

    def selectExpr(self, *exprs: str) -> DataFrame:
        return self._replace_select(", ".join(exprs))

    def where(self, condition: Column) -> DataFrame:
        return self._wrap(
            f"SELECT * FROM ({self._query}) AS _t WHERE {condition._expr}"
        )

    def filter(self, condition: Column) -> DataFrame:
        return self.where(condition)

    def join(
        self,
        other: DataFrame | str,
        on: Column | str | list[str] | None = None,
        how: str = "inner",
    ) -> DataFrame:
        if isinstance(other, DataFrame):
            table_ref = f"({other._query}) AS _t"
        else:
            table_ref = other
        using: list[str] | None = None
        if isinstance(on, list):
            using = on
            on = None
        if using:
            cols = ", ".join(_quote_ident(c) for c in using)
            return self._wrap(
                f"{self._query} {how.upper()} JOIN {table_ref} USING ({cols})"
            )
        if on is not None:
            on_sql = on._expr if isinstance(on, Column) else str(on)
            return self._wrap(
                f"{self._query} {how.upper()} JOIN {table_ref} ON {on_sql}"
            )
        return self._wrap(f"{self._query} {how.upper()} JOIN {table_ref}")

    def groupBy(self, *columns: Column | str) -> GroupedData:
        cols = [Column(_quote_ident(c)) if isinstance(c, str) else c for c in columns]
        return GroupedData(self, cols)

    def having(self, condition: Column) -> DataFrame:
        return self._wrap(
            f"SELECT * FROM ({self._query}) AS _t HAVING {condition._expr}"
        )

    def orderBy(self, *columns: Column | str) -> DataFrame:
        cols = ", ".join(
            Column(_quote_ident(c))._expr if isinstance(c, str) else c._expr
            for c in columns
        )
        return self._wrap(f"SELECT * FROM ({self._query}) AS _t ORDER BY {cols}")

    def limit(self, n: int) -> DataFrame:
        return self._wrap(f"SELECT * FROM ({self._query}) AS _t LIMIT {n}")

    def distinct(self) -> DataFrame:
        return self._wrap(f"SELECT DISTINCT * FROM ({self._query}) AS _t")

    def alias(self, alias: str) -> DataFrame:
        return self._wrap(f"SELECT * FROM ({self._query}) AS {alias}")

    def agg(self, *expressions: Column) -> DataFrame:
        cols = ", ".join(e._expr for e in expressions)
        return self._wrap(f"SELECT {cols} FROM ({self._query}) AS _t")

    def drop(self, *columns: Column | str) -> DataFrame:
        col_names = ", ".join(
            _quote_ident(c.name) if isinstance(c, Column) else _quote_ident(c)
            for c in columns
        )
        return self._wrap(f"SELECT * EXCLUDE ({col_names}) FROM ({self._query}) AS _t")

    def withColumn(self, col_name: str, col_expr: Column) -> DataFrame:
        return self._wrap(
            f"SELECT *, {col_expr._expr} AS {_quote_ident(col_name)}"
            f" FROM ({self._query}) AS _t"
        )

    def withColumnRenamed(self, existing: str, new_name: str) -> DataFrame:
        return self._wrap(
            f"SELECT * REPLACE ({_quote_ident(existing)} AS {_quote_ident(new_name)})"
            f" FROM ({self._query}) AS _t"
        )

    def union(self, other: DataFrame) -> DataFrame:
        sql = f"({self._query}) UNION ({other._query})"
        return DataFrame(sql, self._session)

    def unionAll(self, other: DataFrame) -> DataFrame:
        sql = f"({self._query}) UNION ALL ({other._query})"
        return DataFrame(sql, self._session)

    def intersect(self, other: DataFrame) -> DataFrame:
        sql = f"({self._query}) INTERSECT ({other._query})"
        return DataFrame(sql, self._session)

    def exceptAll(self, other: DataFrame) -> DataFrame:
        sql = f"({self._query}) EXCEPT ({other._query})"
        return DataFrame(sql, self._session)

    def __getitem__(self, item: str | Column) -> Column:
        if isinstance(item, Column):
            return item
        return Column(item)

    def generate_query(self, dialect: str | None = None) -> str:
        sql = self._query
        session = self._session
        target = dialect or session.target_dialect
        if target == "spark":
            return sql
        try:
            ast = _polyglot_sql.parse_one(sql)
            return ast.sql(dialect=target)  # type: ignore[no-any-return]
        except Exception:
            try:
                result = _polyglot_sql.transpile(sql, read="spark", write=target)
                return result[0] if result else sql
            except Exception:
                return sql

    def toArrow(self) -> pa.Table:
        query = self.generate_query()
        session = self._session
        return session._get_driver().toArrow(query)

    def toPandas(self):
        return self.toArrow().to_pandas()

    def show(self, n: int = 20, truncate: bool = True) -> None:
        print(self.generate_query())

    def explain(self, extended: bool = False) -> None:
        print("== Physical Plan ==")
        print(self.generate_query())

    @property
    def write(self) -> DataFrameWriter:
        from pyspark_sql_builder.readwriter import DataFrameWriter

        return DataFrameWriter(self._session, self)

    def copy(self) -> DataFrame:
        return DataFrame(self._query, self._session)
