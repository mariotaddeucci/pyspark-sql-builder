from __future__ import annotations

from typing import TYPE_CHECKING

import polyglot_sql as _polyglot_sql
import pyarrow as pa

from pyspark_sql_builder.pyspark.sql.column import Column, _quote_ident
from pyspark_sql_builder.pyspark.sql.group import GroupedData
from pyspark_sql_builder.pyspark.sql.types import (
    Row,
    StructType,
    _arrow_schema_to_struct_type,
    _arrow_to_dtype_string,
    _print_schema_field,
)

if TYPE_CHECKING:
    from pyspark_sql_builder.pyspark.sql.readwriter import DataFrameWriter
    from pyspark_sql_builder.pyspark.sql.session import SparkSession


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
        ast = _polyglot_sql.parse_one(sql)
        return ast.sql(dialect=target)

    def _get_arrow_schema(self) -> pa.Schema:
        query = f"SELECT * FROM ({self.generate_query()}) AS _t LIMIT 0"
        reader = self._session.to_arrow_reader(query)
        return reader.schema

    @property
    def columns(self) -> list[str]:
        return self._get_arrow_schema().names

    @property
    def dtypes(self) -> list[tuple[str, str]]:
        return [
            (f.name, _arrow_to_dtype_string(f.type)) for f in self._get_arrow_schema()
        ]

    @property
    def schema(self) -> StructType:
        return _arrow_schema_to_struct_type(self._get_arrow_schema())

    def printSchema(self) -> None:
        print("root")
        for field in self._get_arrow_schema():
            _print_schema_field(field, indent=2)

    def toArrow(self) -> pa.Table:
        query = self.generate_query()
        session = self._session
        # Verify that all tables referenced in the query exist
        # This will raise AnalysisException if a table is not found
        session.catalog.verify_tables_exist(query)
        reader = session._get_driver().query(query)
        return reader.read_all()

    def toPandas(self):
        return self.toArrow().to_pandas()

    def show(self, n: int = 20, truncate: bool = True) -> None:
        print(self.generate_query())

    def explain(self, extended: bool = False) -> None:
        print("== Physical Plan ==")
        print(self.generate_query())

    @property
    def write(self) -> DataFrameWriter:
        from pyspark_sql_builder.pyspark.sql.readwriter import DataFrameWriter

        return DataFrameWriter(self._session, self)

    def copy(self) -> DataFrame:
        return DataFrame(self._query, self._session)

    def collect(self) -> list[Row]:
        """Collect all rows of the DataFrame and return them as a list of Row objects.

        Processes data in chunks (record batches) to minimize memory usage and avoid
        materializing the entire dataset at once.

        Returns:
            List of Row objects, one for each row in the DataFrame.

        Example:
            >>> df = spark.range(10).select("id")
            >>> rows = df.collect()
            >>> rows[0]["id"]
            0
        """
        query = self.generate_query()
        session = self._session
        # Verify that all tables referenced in the query exist
        session.catalog.verify_tables_exist(query)
        reader = session._get_driver().query(query)

        rows = []
        # Process each record batch without materializing the full table
        for record_batch in reader:
            schema_names = record_batch.schema.names
            for i in range(record_batch.num_rows):
                row_data = {}
                for col_name, col_data in zip(schema_names, record_batch.columns):
                    value = col_data[i].as_py()
                    row_data[col_name] = value
                rows.append(Row(**row_data))
        return rows
