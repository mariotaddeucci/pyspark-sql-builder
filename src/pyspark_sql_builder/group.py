from __future__ import annotations

from typing import TYPE_CHECKING

from pyspark_sql_builder.column import Column, _to_expr

if TYPE_CHECKING:
    from pyspark_sql_builder.dataframe import DataFrame


def _strip_alias(expr: str) -> str:
    idx = expr.rfind(" AS `")
    if idx != -1 and expr.endswith("`"):
        return expr[:idx]
    return expr


class GroupedData:
    def __init__(self, df: DataFrame, group_by_columns: list[Column]) -> None:
        self._df = df
        self._group_by_columns = group_by_columns

    def agg(self, *expressions: Column) -> DataFrame:
        from pyspark_sql_builder.dataframe import DataFrame as _DataFrame

        group_cols = ", ".join(c._expr for c in self._group_by_columns)
        group_by = ", ".join(_strip_alias(c._expr) for c in self._group_by_columns)
        agg_cols = ", ".join(e._expr for e in expressions)
        if self._group_by_columns:
            sql = (
                f"SELECT {group_cols}, {agg_cols}"
                f" FROM ({self._df._query}) AS _t GROUP BY {group_by}"
            )
        else:
            sql = f"SELECT {agg_cols} FROM ({self._df._query}) AS _t"
        return _DataFrame(sql, self._df._session)

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
