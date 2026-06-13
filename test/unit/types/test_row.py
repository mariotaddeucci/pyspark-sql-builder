"""Tests for pyspark_sql_builder.pyspark.sql.types.Row class."""

from __future__ import annotations

import pytest

from pyspark_sql_builder.pyspark.sql.types import Row


class TestRowCreation:
    """Test Row creation and initialization."""

    def test_row_from_kwargs(self) -> None:
        """Test creating a Row from keyword arguments."""
        row = Row(name="Alice", age=30)
        assert row["name"] == "Alice"
        assert row["age"] == 30

    def test_row_from_args(self) -> None:
        """Test creating a Row from positional arguments."""
        row = Row("Alice", 30)
        assert row[0] == "Alice"
        assert row[1] == 30

    def test_row_mixed_args_kwargs_error(self) -> None:
        """Test that mixing positional and keyword arguments raises an error."""
        with pytest.raises(ValueError, match="Cannot specify both"):
            Row("Alice", age=30)

    def test_row_empty(self) -> None:
        """Test creating an empty Row."""
        row = Row()
        assert len(row) == 0
        assert list(row) == []


class TestRowAccess:
    """Test Row value access."""

    def test_getitem_by_name(self) -> None:
        """Test accessing Row values by column name using __getitem__."""
        row = Row(name="Alice", age=30)
        assert row["name"] == "Alice"
        assert row["age"] == 30

    def test_getitem_by_index(self) -> None:
        """Test accessing Row values by index using __getitem__."""
        row = Row(name="Alice", age=30)
        # kwargs are sorted alphabetically, so age comes before name
        assert row[0] == 30  # age
        assert row[1] == "Alice"  # name

    def test_getattr_by_name(self) -> None:
        """Test accessing Row values by attribute name using __getattr__."""
        row = Row(name="Alice", age=30)
        assert row.name == "Alice"
        assert row.age == 30

    def test_getitem_invalid_column(self) -> None:
        """Test that accessing invalid column raises KeyError."""
        row = Row(name="Alice", age=30)
        with pytest.raises(KeyError, match="Column 'invalid' not found"):
            _ = row["invalid"]

    def test_getattr_invalid_column(self) -> None:
        """Test that accessing invalid attribute raises AttributeError."""
        row = Row(name="Alice", age=30)
        with pytest.raises(AttributeError, match="object has no attribute 'invalid'"):
            _ = row.invalid

    def test_getitem_invalid_type(self) -> None:
        """Test that accessing with invalid index type raises TypeError."""
        row = Row(name="Alice", age=30)
        with pytest.raises(TypeError):
            _ = row[1.5]  # type: ignore


class TestRowIteration:
    """Test Row iteration and length."""

    def test_len(self) -> None:
        """Test Row length."""
        row = Row(name="Alice", age=30, city="NYC")
        assert len(row) == 3

    def test_iter(self) -> None:
        """Test iterating over Row values."""
        row = Row(name="Alice", age=30)
        # kwargs are sorted alphabetically, so age comes before name
        values = list(row)
        assert values == [30, "Alice"]  # age first, then name

    def test_iter_from_args(self) -> None:
        """Test iterating over Row created from positional arguments."""
        row = Row("Alice", 30, "NYC")
        values = list(row)
        assert values == ["Alice", 30, "NYC"]


class TestRowComparison:
    """Test Row equality and hashing."""

    def test_eq_same_values(self) -> None:
        """Test that Rows with same values are equal."""
        row1 = Row(name="Alice", age=30)
        row2 = Row(name="Alice", age=30)
        assert row1 == row2

    def test_eq_different_values(self) -> None:
        """Test that Rows with different values are not equal."""
        row1 = Row(name="Alice", age=30)
        row2 = Row(name="Bob", age=25)
        assert row1 != row2

    def test_eq_different_fields(self) -> None:
        """Test that Rows with different field order are not equal."""
        row1 = Row(name="Alice", age=30)
        row2 = Row(age=30, name="Alice")
        # They have same values but potentially different field order
        # Rows created from kwargs are sorted, so they should be equal
        assert row1 == row2

    def test_eq_with_non_row(self) -> None:
        """Test that comparing Row with non-Row returns False."""
        row = Row(name="Alice", age=30)
        assert row != {"name": "Alice", "age": 30}
        assert row != "Alice"

    def test_hash(self) -> None:
        """Test that Row is hashable."""
        row1 = Row(name="Alice", age=30)
        row2 = Row(name="Alice", age=30)
        assert hash(row1) == hash(row2)

    def test_hash_in_set(self) -> None:
        """Test that Rows can be used in sets."""
        row1 = Row(name="Alice", age=30)
        row2 = Row(name="Alice", age=30)
        row3 = Row(name="Bob", age=25)
        row_set = {row1, row2, row3}
        assert len(row_set) == 2


class TestRowRepr:
    """Test Row string representation."""

    def test_repr_kwargs(self) -> None:
        """Test Row repr with named fields."""
        row = Row(name="Alice", age=30)
        assert "Row(" in repr(row)
        assert "name='Alice'" in repr(row)
        assert "age=30" in repr(row)

    def test_repr_args(self) -> None:
        """Test Row repr with positional arguments."""
        row = Row("Alice", 30)
        assert "Row(" in repr(row)
        assert "'Alice'" in repr(row)
        assert "30" in repr(row)


class TestRowAsDict:
    """Test Row.asDict() method."""

    def test_as_dict_basic(self) -> None:
        """Test converting Row to dictionary."""
        row = Row(name="Alice", age=30, city="NYC")
        d = row.asDict()
        assert d == {"name": "Alice", "age": 30, "city": "NYC"}

    def test_as_dict_with_none(self) -> None:
        """Test converting Row with None values to dictionary."""
        row = Row(name="Alice", age=None)
        d = row.asDict()
        assert d == {"name": "Alice", "age": None}

    def test_as_dict_nested_rows(self) -> None:
        """Test converting Row with nested Rows to dictionary (recursive=True)."""
        inner_row = Row(street="123 Main St", city="NYC")
        outer_row = Row(name="Alice", address=inner_row)
        d = outer_row.asDict(recursive=True)
        expected = {
            "address": {"city": "NYC", "street": "123 Main St"},
            "name": "Alice",
        }
        assert d == expected

    def test_as_dict_nested_rows_non_recursive(self) -> None:
        """Test converting Row with nested Rows (recursive=False)."""
        inner_row = Row(street="123 Main St", city="NYC")
        outer_row = Row(name="Alice", address=inner_row)
        d = outer_row.asDict(recursive=False)
        assert d["name"] == "Alice"
        assert isinstance(d["address"], Row)

    def test_as_dict_list_of_rows(self) -> None:
        """Test converting Row with list of Rows (recursive=True)."""
        row1 = Row(name="Item1", price=10)
        row2 = Row(name="Item2", price=20)
        outer_row = Row(order_id=123, items=[row1, row2])
        d = outer_row.asDict(recursive=True)
        assert d == {
            "order_id": 123,
            "items": [
                {"name": "Item1", "price": 10},
                {"name": "Item2", "price": 20},
            ],
        }
