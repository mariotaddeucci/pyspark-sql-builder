# Test Guide — pyspark-sql-builder

## Conventions

- **Plain functions only** (no classes, no `self`)
- **Fixtures** go in `test/unit/conftest.py`
- **Each public function/method** in `DataFrame`, `Column`, and `functions` should have at least one test
- **Every test asserts on `generate_query()`** output or `Column._expr` — no database connections
- **Test files are organized by module subdirectory.** Each module (`functions/`, `column/`, `dataframe/`, `session/`, `types/`) has its own directory under `test/unit/`. Test file names reflect the function or method being tested (e.g., `test_col.py`, `test_where.py`, `test_alias.py`).

## Writing tests — docstring-first approach

The recommended approach for writing tests is:

1. **Look up the original PySpark docstring** for the function/method at:  
   <https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/functions.html>  
   (or the class-specific page, e.g. `DataFrame`, `Column`).

2. **Replicate the official docstring examples as test cases.**  
   This ensures the library matches Spark's documented behavior.  
   Each docstring example should become one or more asserts.

3. For functions that raise `NotImplementedError` (no SQL equivalent), verify the exception is raised.

### Example — `col()` function

Official PySpark docstring:
```
col(col: str) -> Column
…
>>> df.select(col("id").cast("int")).show()
>>> df.select(col("id").alias("num")).show()
```

Corresponding test:
```python
def test_col() -> None:
    c = F.col("id")
    assert isinstance(c, Column)
    assert c._expr == "`id`"
```

### Example — `Column.between()` method

Official docstring:
```
between(lowerBound, upperBound)
…
>>> df.filter(df.age.between(18, 65))
```

Test:
```python
def test_between() -> None:
    c = Column("age").between(18, 65)
    assert c._expr == "age BETWEEN 18 AND 65"
```

### Example — `DataFrame.select()` method

Official docstring:
```
select(*cols) -> DataFrame
…
>>> df.select("id", "name").show()
```

Test:
```python
def test_select_columns(spark: SparkSession) -> None:
    df = spark.table("users").select("id", "name")
    assert df.generate_query() == "SELECT `id`, `name` FROM users"
```

### Example — `NotImplementedError`

```python
def test_broadcast_not_implemented() -> None:
    with pytest.raises(NotImplementedError, match="broadcast"):
        F.broadcast(...)
```

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

## Test locations (macro)

```
test/
├── unit/          # ~120 unit tests, no DB
│   ├── conftest.py        # fixtures: spark, duckdb, postgres, bigquery
│   ├── functions/         # tests for pyspark_sql_builder.functions
│   ├── column/            # tests for pyspark_sql_builder.column
│   ├── dataframe/         # tests for pyspark_sql_builder.dataframe
│   ├── session/           # tests for pyspark_sql_builder.session
│   └── types/             # tests for pyspark_sql_builder.types
└── integration/    # runs against SQLite and DuckDB
    └── sqlite/
```

## Running tests

```bash
uv run pytest -v                     # all tests
uv run pytest test/unit/ -v          # unit tests only
uv run pytest test/unit/functions/ -v  # function tests only
uv run pytest test/unit/column/ -v     # column tests only
uv run pytest test/unit/dataframe/ -v  # dataframe tests only
uv run pytest test/unit/session/ -v    # session tests only
uv run pytest test/unit/types/ -v      # types tests only
uv run pytest test/integration/ -v   # integration tests only
uv run pytest -k "transpile"         # filter by keyword
```
