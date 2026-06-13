from __future__ import annotations

from typing import TYPE_CHECKING

from pyspark_sql_builder.column import Column, _to_expr

if TYPE_CHECKING:
    from pyspark_sql_builder.dataframe import DataFrame


class GroupedData:
    def __init__(self, df: DataFrame, group_by_columns: list[Column]) -> None:
        self._df = df
        self._group_by_columns = group_by_columns

    def agg(self, *expressions: Column) -> DataFrame:
        from pyspark_sql_builder.dataframe import DataFrame as _DataFrame

        df = self._df.select(*group_by_exprs(self._group_by_columns), *expressions)
        result = _DataFrame.__new__(_DataFrame)
        result._table = df._table
        result._session = df._session
        result._raw_sql = df._raw_sql
        result._projections = list(self._group_by_columns) + list(expressions)  # type: ignore[bad-assignment]  # noqa: E501
        result._wheres = list(df._wheres)
        result._joins = list(df._joins)
        result._group_by = list(self._group_by_columns)
        result._having = None
        result._order_by = None
        result._limit = None
        result._offset = None
        result._distinct = False
        result._alias = None
        return result

    def count(self) -> DataFrame:
        return self.agg(Column("COUNT(*)"))

    def sum(self, column: Column | str) -> DataFrame:
        return self.agg(Column(f"SUM({_to_expr(column)})"))

    def avg(self, column: Column | str) -> DataFrame:
        return self.agg(Column(f"AVG({_to_expr(column)})"))

    def min(self, column: Column | str) -> DataFrame:
        return self.agg(Column(f"MIN({_to_expr(column)})"))

    def max(self, column: Column | str) -> DataFrame:
        return self.agg(Column(f"MAX({_to_expr(column)})"))


def group_by_exprs(columns: list[Column]) -> list[Column]:
    return [Column(_to_expr(c)) for c in columns]
