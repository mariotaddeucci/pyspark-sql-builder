# Test Guide — pyspark-sql-builder

## Conventions

- **Plain functions only** (no classes, no `self`)
- **Fixtures** go in `conftest.py`
- **Each public method** in `DataFrame`, `Column`, and `functions` should have at least one test
- **Every test asserts on `generate_query()`** output — no database connections

## Fixtures

```python
# conftest.py provides:
spark    -> SparkSession(dialect="spark")
duckdb   -> SparkSession(dialect="duckdb")
postgres -> SparkSession(dialect="postgres")
bigquery -> SparkSession(dialect="bigquery")
```

## Test patterns

### Column tests
```python
def test_eq() -> None:
    c = Column("age") == 18
    assert c._expr == "age = 18"
```

### DataFrame tests
```python
def test_select_columns(spark: SparkSession) -> None:
    df = spark.table("users").select("id", "name")
    assert df.generate_query() == "SELECT id, name FROM users"
```

### Function tests
```python
def test_count_column() -> None:
    c = F.count(F.col("id"))
    assert c._expr == "COUNT(id)"
```

### Dialect transpilation tests
```python
@pytest.mark.parametrize("dialect", ["spark", "duckdb", "postgres", "bigquery"])
def test_transpile(dialect: str) -> None:
    session = SparkSession(dialect=dialect)
    df = session.table("users").where(F.col("age") > 18)
    result = df.generate_query()
    assert "SELECT" in result
    assert result
```

### CamelCase API
All methods use PySpark-style camelCase:
- `df.groupBy(...)`, `df.orderBy(...)`, `df.selectExpr(...)`
- `df.withColumn(...)`, `df.withColumnRenamed(...)`
- `df.unionAll(...)`, `df.exceptAll(...)`
- `Column.isNull()`, `Column.isNotNull()`
- `F.sum()`, `F.min()`, `F.max()`, `F.abs()`, `F.round()` (shadow builtins)
- `F.countDistinct()`
- `SparkSession.builder.getOrCreate()`

## Test locations

```
test/
├── unit/               # 96 unit tests, no DB
│   ├── conftest.py     # spark, duckdb, postgres, bigquery fixtures
│   ├── test_column.py
│   ├── test_dataframe.py
│   ├── test_functions.py
│   ├── test_session.py
│   └── test_types.py
└── integration/
    └── sqlite/
        ├── conftest.py               # sqlite_conn fixture (in-memory SQLite)
        └── test_sqlite_integration.py  # 2 tests: monthly agg + window function
```

## Running tests

```bash
uv run pytest -v                     # all tests
uv run pytest test/unit/ -v          # unit tests only
uv run pytest test/integration/ -v   # integration tests only
uv run pytest -k "transpile"         # filter by keyword
```
