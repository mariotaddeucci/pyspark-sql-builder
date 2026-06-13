from __future__ import annotations

from typing import TYPE_CHECKING

import polyglot_sql as _polyglot_sql

from pyspark_sql_builder.column import Column, _quote_ident
from pyspark_sql_builder.group import GroupedData

if TYPE_CHECKING:
    from pyspark_sql_builder.session import SparkSession


class DataFrame:
    def __init__(
        self,
        table: str | None = None,
        session: SparkSession | None = None,
    ) -> None:
        self._table = table
        self._session = session
        self._raw_sql: str | None = None
        self._projections: list[Column | str] | None = None
        self._wheres: list[Column] = []
        self._joins: list[dict] = []
        self._group_by: list[Column | str] | None = None
        self._having: Column | None = None
        self._order_by: list[Column | str] | None = None
        self._limit: int | None = None
        self._offset: int | None = None
        self._distinct: bool = False
        self._alias: str | None = None

        if session is None:
            from pyspark_sql_builder.session import SparkSession as _Session

            self._session = _Session()

    @classmethod
    def from_sql(cls, query: str, session: SparkSession | None = None) -> DataFrame:
        df = cls.__new__(cls)
        df._table = None
        df._session = session
        df._raw_sql = query
        df._projections = None
        df._wheres = []
        df._joins = []
        df._group_by = None
        df._having = None
        df._order_by = None
        df._limit = None
        df._offset = None
        df._distinct = False
        df._alias = None
        if session is None:
            from pyspark_sql_builder.session import SparkSession as _Session

            df._session = _Session()
        return df

    @classmethod
    def from_rows(
        cls,
        rows: list[tuple],
        schema: list[str],
        session: SparkSession | None = None,
    ) -> DataFrame:
        values = ", ".join(
            f"({', '.join(repr(v) if isinstance(v, str) else str(v) for v in row)})"
            for row in rows
        )
        cols = ", ".join(schema)
        sql = f"SELECT {cols} FROM (VALUES {values}) AS t({cols})"
        return cls.from_sql(sql, session)

    def select(self, *columns: Column | str) -> DataFrame:
        df = self._clone()
        df._projections = [
            Column(_quote_ident(c)) if isinstance(c, str) else c for c in columns
        ]
        return df

    def selectExpr(self, *exprs: str) -> DataFrame:
        df = self._clone()
        df._projections = list(exprs)
        return df

    def where(self, condition: Column) -> DataFrame:
        df = self._clone()
        df._wheres = [*self._wheres, condition]
        return df

    def filter(self, condition: Column) -> DataFrame:
        return self.where(condition)

    def join(
        self,
        other: DataFrame | str,
        on: Column | str | list[str] | None = None,
        how: str = "inner",
    ) -> DataFrame:
        df = self._clone()
        if isinstance(other, DataFrame):
            table_name = other._table
            table_alias = other._alias
        else:
            table_name = other
            table_alias = None
        using: list[str] | None = None
        if isinstance(on, list):
            using = on
            on = None
        df._joins = [
            *self._joins,
            {
                "table": table_name,
                "alias": table_alias,
                "on": on,
                "how": how,
                "using": using,
            },
        ]
        return df

    def groupBy(self, *columns: Column | str) -> GroupedData:
        cols = [Column(_quote_ident(c)) if isinstance(c, str) else c for c in columns]
        return GroupedData(self, cols)

    def having(self, condition: Column) -> DataFrame:
        df = self._clone()
        df._having = condition
        return df

    def orderBy(self, *columns: Column | str) -> DataFrame:
        df = self._clone()
        df._order_by = [
            Column(_quote_ident(c)) if isinstance(c, str) else c for c in columns
        ]
        return df

    def limit(self, n: int) -> DataFrame:
        df = self._clone()
        df._limit = n
        return df

    def offset(self, n: int) -> DataFrame:
        df = self._clone()
        df._offset = n
        return df

    def distinct(self) -> DataFrame:
        df = self._clone()
        df._distinct = True
        return df

    def alias(self, alias: str) -> DataFrame:
        df = self._clone()
        df._alias = alias
        return df

    def agg(self, *expressions: Column) -> DataFrame:
        df = self._clone()
        df._projections = list(expressions)
        return df

    def drop(self, *columns: Column | str) -> DataFrame:
        projections = self._projections
        if not projections:
            return self.select("*")
        col_names = {c.name if isinstance(c, Column) else c for c in columns}
        remaining: list[Column | str] = [
            c
            for c in projections
            if not (isinstance(c, Column) and c.name in col_names)
            and not (isinstance(c, str) and c in col_names)
        ]
        if not remaining:
            remaining = [Column("*")]
        df = self._clone()
        df._projections = remaining
        return df

    def withColumn(self, col_name: str, col_expr: Column) -> DataFrame:
        df = self._clone()
        if df._projections is not None:
            for i, c in enumerate(df._projections):
                if isinstance(c, Column) and c.name == col_name:
                    df._projections[i] = col_expr
                    return df
                if isinstance(c, str) and c == col_name:
                    df._projections[i] = col_expr
                    return df
            df._projections = [*df._projections, col_expr.alias(col_name)]
        return df

    def withColumnRenamed(self, existing: str, new_name: str) -> DataFrame:
        df = self._clone()
        if df._projections is not None:
            for i, c in enumerate(df._projections):
                if isinstance(c, Column) and c.name == existing:
                    df._projections[i] = Column(f"{c._expr} AS `{new_name}`")
                    return df
                if isinstance(c, str) and c == existing:
                    df._projections[i] = Column(f"{c} AS `{new_name}`")
                    return df
        return df

    def union(self, other: DataFrame) -> DataFrame:
        sql = f"({self.generate_query()}) UNION ({other.generate_query()})"
        return DataFrame.from_sql(sql, self._session)

    def unionAll(self, other: DataFrame) -> DataFrame:
        sql = f"({self.generate_query()}) UNION ALL ({other.generate_query()})"
        return DataFrame.from_sql(sql, self._session)

    def intersect(self, other: DataFrame) -> DataFrame:
        sql = f"({self.generate_query()}) INTERSECT ({other.generate_query()})"
        return DataFrame.from_sql(sql, self._session)

    def exceptAll(self, other: DataFrame) -> DataFrame:
        sql = f"({self.generate_query()}) EXCEPT ({other.generate_query()})"
        return DataFrame.from_sql(sql, self._session)

    def __getitem__(self, item: str | Column) -> Column:
        if isinstance(item, Column):
            return item
        return Column(item)

    def generate_query(self, dialect: str | None = None) -> str:
        sql = self._raw_sql if self._raw_sql else self._build_sql()
        session = self._session
        if session is None:
            from pyspark_sql_builder.session import SparkSession as _Session

            session = _Session()
        target = dialect or session.dialect
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

    def show(self, n: int = 20, truncate: bool = True) -> None:
        print(self.generate_query())

    def explain(self, extended: bool = False) -> None:
        print("== Physical Plan ==")
        print(self.generate_query())

    def copy(self) -> DataFrame:
        return self._clone()

    def _build_sql(self) -> str:
        parts: list[str] = ["SELECT"]

        if self._distinct:
            parts.append("DISTINCT")

        if self._projections:
            cols = ", ".join(
                c._expr if isinstance(c, Column) else str(c) for c in self._projections
            )
            parts.append(cols)
        else:
            parts.append("*")

        if self._table:
            table_ref = self._table
            if self._alias:
                table_ref = f"{table_ref} AS {self._alias}"
            parts.append(f"FROM {table_ref}")

        for join_info in self._joins:
            how = join_info["how"].upper()
            table = join_info["table"]
            alias = join_info.get("alias")
            table_ref = f"{table} AS {alias}" if alias else table
            using = join_info.get("using")
            if using:
                cols = ", ".join(f"`{c}`" for c in using)
                parts.append(f"{how} JOIN {table_ref} USING ({cols})")
                continue
            on_clause = join_info["on"]
            if on_clause:
                on_sql = (
                    on_clause._expr if isinstance(on_clause, Column) else str(on_clause)
                )
                parts.append(f"{how} JOIN {table_ref} ON {on_sql}")
            else:
                parts.append(f"{how} JOIN {table_ref}")

        if self._wheres:
            where = " AND ".join(c._expr for c in self._wheres)
            parts.append(f"WHERE {where}")

        if self._group_by:
            cols = ", ".join(
                c._expr if isinstance(c, Column) else str(c) for c in self._group_by
            )
            parts.append(f"GROUP BY {cols}")

        if self._having:
            parts.append(f"HAVING {self._having._expr}")

        if self._order_by:
            cols = ", ".join(
                c._expr if isinstance(c, Column) else str(c) for c in self._order_by
            )
            parts.append(f"ORDER BY {cols}")

        if self._limit is not None:
            parts.append(f"LIMIT {self._limit}")

        if self._offset is not None:
            parts.append(f"OFFSET {self._offset}")

        return " ".join(parts)

    def _clone(self) -> DataFrame:
        df = DataFrame.__new__(DataFrame)
        df._table = self._table
        df._session = self._session
        df._raw_sql = self._raw_sql
        df._projections = self._projections
        df._wheres = list(self._wheres)
        df._joins = list(self._joins)
        df._group_by = self._group_by
        df._having = self._having
        df._order_by = self._order_by
        df._limit = self._limit
        df._offset = self._offset
        df._distinct = self._distinct
        df._alias = self._alias
        return df
