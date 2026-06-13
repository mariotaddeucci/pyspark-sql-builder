from __future__ import annotations

from pyspark_sql_builder.column import Column, _quote_ident


class Window:
    def __init__(self) -> None:
        self._partition_by: list[Column] | None = None
        self._order_by: list[Column] | None = None

    @staticmethod
    def partitionBy(*cols: Column | str) -> Window:
        w = Window()
        w._partition_by = [
            Column(_quote_ident(c)) if isinstance(c, str) else c for c in cols
        ]
        return w

    def orderBy(self, *cols: Column | str) -> Window:
        self._order_by = [
            Column(_quote_ident(c)) if isinstance(c, str) else c for c in cols
        ]
        return self

    def _spec_sql(self) -> str:
        parts: list[str] = []
        if self._partition_by:
            cols = ", ".join(c._expr for c in self._partition_by)
            parts.append(f"PARTITION BY {cols}")
        if self._order_by:
            cols = ", ".join(c._expr for c in self._order_by)
            parts.append(f"ORDER BY {cols}")
        return " ".join(parts)
