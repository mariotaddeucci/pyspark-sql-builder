# PySpark SQL Functions — Implementation TODO Checklist

> **Orientation:** Cada função deve ser **totalmente funcional** e seguir o **mesmo comportamento do PySpark** (mesmo nome, mesmos parâmetros, mesmo retorno `Column`).  
> Caso não exista combinação de chamadas SQL equivalentes via `sqlglot`, deve-se lançar `NotImplementedError` com mensagem clara.  
> **Toda função `NotImplementedError` deve ter pelo menos um teste** que verifique que a exceção é levantada.  
> Usar `_to_expr()` para literais e `_quote_ident()` para identificadores.  
> Seguir padrões de teste em `test/unit/test_functions.py` e `test/AGENTS.md`.

**Legenda:**
- `✅` — Pendente (SQL direto possível via sqlglot)
- `✅` — Pendente (deve lançar `NotImplementedError` — sem equivalente SQL)
- `✅` — Já implementado

---

## 1. Core / Column Construction

- [x] `col(name)` — ✅
- [x] `column(name)` — alias para `col`
- [x] `lit(value)` — ✅
- [x] `expr(str)` — `Column(str)` direto
- [x] `broadcast(df)` — ✅ hint de broadcast, sem equivalente SQL puro
- [x] `call_function(name, *args)` — `name(args)`

---

## 2. Conditional / Null Handling

- [x] `coalesce(*cols)` — ✅
- [x] `ifnull(col, alt)` — `IFNULL(col, alt)`
- [x] `nanvl(col, alt)` — `IF(ISNAN(col), alt, col)`
- [x] `nullif(col, val)` — `NULLIF(col, val)`
- [x] `nullifzero(col)` — `NULLIF(col, 0)`
- [x] `nvl(col, alt)` — `NVL(col, alt)` (alias `IFNULL`)
- [x] `nvl2(col, v1, v2)` — `CASE WHEN col IS NOT NULL THEN v1 ELSE v2 END`
- [x] `when(cond, val)` — ✅ (com `WhenBuilder`)
- [x] `zeroifnull(col)` — `COALESCE(col, 0)`
- [x] `equal_null(col1, col2)` — `col1 <=> col2` (null-safe equal)

---

## 3. Predicate / Match Functions

- [x] `ilike(col, pattern)` — `col ILIKE pattern`
- [x] `isnan(col)` — `ISNAN(col)`
- [x] `isnotnull(col)` — `col IS NOT NULL`
- [x] `isnull(col)` — `col IS NULL`
- [x] `like(col, pattern)` — `col LIKE pattern`
- [x] `regexp(col, regex)` — `col RLIKE regex` (alias)
- [x] `regexp_like(col, regex)` — `col RLIKE regex`
- [x] `rlike(col, regex)` — `col RLIKE regex`

---

## 4. Sort Direction (Module-level)

- [x] `asc(col)` — ✅
- [x] `asc_nulls_first(col)` — `col ASC NULLS FIRST`
- [x] `asc_nulls_last(col)` — `col ASC NULLS LAST`
- [x] `desc(col)` — ✅
- [x] `desc_nulls_first(col)` — `col DESC NULLS FIRST`
- [x] `desc_nulls_last(col)` — `col DESC NULLS LAST`

---

## 5. Math Functions

- [x] `abs(col)` — ✅
- [x] `acos(col)` — `ACOS(col)`
- [x] `acosh(col)` — `ACOSH(col)`
- [x] `asin(col)` — `ASIN(col)`
- [x] `asinh(col)` — `ASINH(col)`
- [x] `atan(col)` — `ATAN(col)`
- [x] `atan2(colY, colX)` — `ATAN2(colY, colX)`
- [x] `atanh(col)` — `ATANH(col)`
- [x] `bin(col)` — `BIN(col)` — ver suporte no dialeto alvo
- [x] `bround(col[, scale])` — `BROUND(col, scale)` (banker's rounding)
- [x] `cbrt(col)` — `CBRT(col)`
- [x] `ceil(col)` — ✅
- [x] `ceiling(col)` — alias para `CEIL`
- [x] `conv(col, fromBase, toBase)` — `CONV(col, fromBase, toBase)`
- [x] `cos(col)` — `COS(col)`
- [x] `cosh(col)` — `COSH(col)`
- [x] `cot(col)` — `COT(col)`
- [x] `csc(col)` — `CSC(col)`
- [x] `degrees(col)` — `DEGREES(col)`
- [x] `e()` — `EXP(1)` ou `E()`
- [x] `exp(col)` — ✅
- [x] `expm1(col)` — `EXP(col) - 1`
- [x] `factorial(col)` — `FACTORIAL(col)`
- [x] `floor(col)` — ✅
- [x] `greatest(*cols)` — `GREATEST(col1, col2, ...)`
- [x] `hex(col)` — `HEX(col)`
- [x] `hypot(col1, col2)` — `SQRT(col1*col1 + col2*col2)`
- [x] `least(*cols)` — `LEAST(col1, col2, ...)`
- [x] `ln(col)` — `LN(col)`
- [x] `log(col)` — ✅ (`LOG(col)`)
- [x] `log10(col)` — `LOG10(col)`
- [x] `log1p(col)` — `LOG(1 + col)`
- [x] `log2(col)` — `LOG2(col)`
- [x] `negate(col)` — `-col`
- [x] `negative(col)` — `-col` (alias)
- [x] `pi()` — `PI()`
- [x] `pmod(col, divisor)` — `col % divisor` (positive mod)
- [x] `positive(col)` — `+col`
- [x] `pow(col, exp)` — ✅
- [x] `power(col, exp)` — ✅ (alias)
- [x] `radians(col)` — `RADIANS(col)`
- [x] `rand([seed])` — `RAND(seed)`
- [x] `randn([seed])` — `RANDN(seed)` — ver suporte sqlglot
- [x] `random([seed])` — alias para `rand`
- [x] `rint(col)` — `RINT(col)`
- [x] `round(col[, scale])` — ✅
- [x] `sec(col)` — `1 / COS(col)`
- [x] `sign(col)` — `SIGN(col)`
- [x] `signum(col)` — alias para `sign`
- [x] `sin(col)` — `SIN(col)`
- [x] `sinh(col)` — `SINH(col)`
- [x] `sqrt(col)` — ✅
- [x] `tan(col)` — `TAN(col)`
- [x] `tanh(col)` — `TANH(col)`
- [x] `try_add(col1, col2)` — `col1 + col2` com trat. erro
- [x] `try_divide(col1, col2)` — `col1 / col2` com trat. erro
- [x] `try_mod(col1, col2)` — `col1 % col2` com trat. erro
- [x] `try_multiply(col1, col2)` — `col1 * col2` com trat. erro
- [x] `try_subtract(col1, col2)` — `col1 - col2` com trat. erro
- [x] `unhex(col)` — `UNHEX(col)`
- [x] `uniform(low, high[, seed])` — gera valor aleatório uniforme
- [x] `width_bucket(col, min, max, nBuckets)` — `WIDTH_BUCKET(col, min, max, nBuckets)`

---

## 6. String Functions

- [x] `ascii(col)` — `ASCII(col)`
- [x] `base64(col)` — `BASE64(col)`
- [x] `bit_length(col)` — `BIT_LENGTH(col)`
- [x] `btrim(col[, trimStr])` — `BTRIM(col, trimStr)`
- [x] `char(col)` — `CHAR(col)`
- [x] `char_length(col)` — `CHAR_LENGTH(col)`
- [x] `character_length(col)` — alias
- [x] `chr(col)` — `CHR(col)`
- [x] `collate(col, collation)` — `col COLLATE collation`
- [x] `collation(col)` — `COLLATION(col)`
- [x] `concat(*cols)` — ✅
- [x] `concat_ws(sep, *cols)` — ✅
- [x] `contains(col, other)` — `CONTAINS(col, other)`
- [x] `decode(col, charset)` — `DECODE(col, charset)`
- [x] `elt(n, *strings)` — `ELT(n, str1, str2, ...)`
- [x] `encode(col, charset)` — `ENCODE(col, charset)`
- [x] `endswith(col, suffix)` — `col LIKE '%' || suffix`
- [x] `find_in_set(str, strArray)` — `FIND_IN_SET(str, strArray)`
- [x] `format_number(col, decimalPlaces)` — ✅
- [x] `format_string(format, *args)` — `FORMAT_STRING(format, args)`
- [x] `initcap(col)` — ✅
- [x] `instr(col, substr)` — `INSTR(col, substr)`
- [x] `is_valid_utf8(col)` — `IS_VALID_UTF8(col)` — ver suporte
- [x] `lcase(col)` — alias `LOWER`
- [x] `left(col, len)` — `LEFT(col, len)`
- [x] `length(col)` — ✅
- [x] `levenshtein(col1, col2)` — `LEVENSHTEIN(col1, col2)`
- [x] `locate(substr, col[, pos])` — `LOCATE(substr, col, pos)`
- [x] `lower(col)` — ✅
- [x] `lpad(col, len, pad)` — `LPAD(col, len, pad)`
- [x] `ltrim(col)` — ✅
- [x] `make_valid_utf8(col)` — `MAKE_VALID_UTF8(col)` — ver suporte
- [x] `mask(col[, upperChar, lowerChar, digitChar, otherChar])` — ✅ máscara proprietária Spark
- [x] `octet_length(col)` — `OCTET_LENGTH(col)`
- [x] `overlay(col, replace, pos[, len])` — `OVERLAY(col PLACING replace FROM pos FOR len)`
- [x] `position(substr, col)` — `POSITION(substr IN col)`
- [x] `printf(format, *args)` — `PRINTF(format, args)`
- [x] `quote(col)` — `QUOTE(col)`
- [x] `randstr(len[, seed])` — `RANDSTR(len, seed)` — ver suporte
- [x] `regexp_count(col, regex)` — `REGEXP_COUNT(col, regex)`
- [x] `regexp_extract(col, regex[, idx])` — `REGEXP_EXTRACT(col, regex, idx)`
- [x] `regexp_extract_all(col, regex[, idx])` — `REGEXP_EXTRACT_ALL(col, regex, idx)`
- [x] `regexp_instr(col, regex)` — `REGEXP_INSTR(col, regex)`
- [x] `regexp_replace(col, regex, repl[, pos])` — `REGEXP_REPLACE(col, regex, repl)`
- [x] `regexp_substr(col, regex)` — `REGEXP_SUBSTR(col, regex)`
- [x] `repeat(col, n)` — `REPEAT(col, n)`
- [x] `replace(col, search, repl)` — ✅
- [x] `reverse(col)` — ✅
- [x] `right(col, len)` — `RIGHT(col, len)`
- [x] `rpad(col, len, pad)` — `RPAD(col, len, pad)`
- [x] `rtrim(col)` — ✅
- [x] `sentences(col[, lang, country])` — `SENTENCES(col, lang, country)` — ver suporte
- [x] `soundex(col)` — `SOUNDEX(col)`
- [x] `split(col, pattern[, limit])` — ✅
- [x] `split_part(col, delimiter, partNum)` — `SPLIT_PART(col, delimiter, partNum)`
- [x] `startswith(col, prefix)` — `col LIKE prefix || '%'`
- [x] `substr(col, pos[, len])` — alias (já implementado como `substring`)
- [x] `substring(col, pos[, len])` — ✅
- [x] `substring_index(col, delim, count)` — `SUBSTRING_INDEX(col, delim, count)`
- [x] `to_binary(col[, fmt])` — `TO_BINARY(col, fmt)`
- [x] `to_char(col, fmt)` — `TO_CHAR(col, fmt)`
- [x] `to_number(col, fmt)` — `TO_NUMBER(col, fmt)`
- [x] `to_varchar(col, fmt)` — alias `TO_CHAR`
- [x] `translate(col, from, to)` — `TRANSLATE(col, from, to)`
- [x] `trim(col)` — ✅
- [x] `try_to_binary(col[, fmt])` — `TRY_TO_BINARY(col, fmt)`
- [x] `try_to_number(col, fmt)` — `TRY_TO_NUMBER(col, fmt)`
- [x] `try_validate_utf8(col)` — `TRY_VALIDATE_UTF8(col)` — ver suporte
- [x] `ucase(col)` — alias `UPPER`
- [x] `unbase64(col)` — `UNBASE64(col)`
- [x] `upper(col)` — ✅
- [x] `validate_utf8(col)` — `VALIDATE_UTF8(col)` — ver suporte

---

## 7. Bitwise Functions

- [x] `bit_count(col)` — `BIT_COUNT(col)`
- [x] `bit_get(col, pos)` — `BIT_GET(col, pos)`
- [x] `bitwise_not(col)` — `~col`
- [x] `getbit(col, pos)` — `GETBIT(col, pos)`
- [x] `shiftleft(col, n)` — `col << n`
- [x] `shiftright(col, n)` — `col >> n`
- [x] `shiftrightunsigned(col, n)` — `col >> n` unsigned — ver suporte

---

## 8. Date / Time Functions

- [x] `add_months(col, n)` — `ADD_MONTHS(col, n)`
- [x] `convert_timezone(fromTz, toTz, col)` — `CONVERT_TIMEZONE(fromTz, toTz, col)`
- [x] `curdate()` — `CURRENT_DATE`
- [x] `current_date()` — ✅
- [x] `current_time()` — `CURRENT_TIME`
- [x] `current_timestamp()` — ✅
- [x] `current_timezone()` — `CURRENT_TIMEZONE()`
- [x] `date_add(col, days)` — ✅
- [x] `date_diff(end, start)` — `DATEDIFF(end, start)`
- [x] `date_format(col, fmt)` — `DATE_FORMAT(col, fmt)`
- [x] `date_from_unix_date(col)` — `DATE_FROM_UNIX_DATE(col)`
- [x] `date_part(field, col)` — `DATE_PART(field, col)`
- [x] `date_sub(col, days)` — ✅
- [x] `date_trunc(fmt, col)` — `DATE_TRUNC(fmt, col)`
- [x] `dateadd(col, days)` — alias `date_add`
- [x] `datediff(end, start)` — ✅
- [x] `datepart(field, col)` — alias `date_part`
- [x] `day(col)` — ✅
- [x] `dayname(col)` — `DAYNAME(col)`
- [x] `dayofmonth(col)` — `DAYOFMONTH(col)`
- [x] `dayofweek(col)` — `DAYOFWEEK(col)`
- [x] `dayofyear(col)` — `DAYOFYEAR(col)`
- [x] `extract(field, col)` — `EXTRACT(field FROM col)`
- [x] `from_unixtime(col[, fmt])` — ✅
- [x] `from_utc_timestamp(col, tz)` — `FROM_UTC_TIMESTAMP(col, tz)`
- [x] `hour(col)` — ✅
- [x] `last_day(col)` — `LAST_DAY(col)`
- [x] `localtimestamp()` — `LOCALTIMESTAMP`
- [x] `make_date(y, m, d)` — `MAKE_DATE(y, m, d)`
- [x] `make_dt_interval([days[, hours, mins, secs]])` — `MAKE_DT_INTERVAL(...)` — ver suporte
- [x] `make_interval([years, months, weeks, days, hours, mins, secs])` — `MAKE_INTERVAL(...)`
- [x] `make_time(h, m, s)` — `MAKE_TIME(h, m, s)`
- [x] `make_timestamp(y, m, d, h, mi, s[, tz])` — `MAKE_TIMESTAMP(...)`
- [x] `make_timestamp_ltz(y, m, d, h, mi, s[, tz])` — `MAKE_TIMESTAMP_LTZ(...)`
- [x] `make_timestamp_ntz(y, m, d, h, mi, s)` — `MAKE_TIMESTAMP_NTZ(...)`
- [x] `make_ym_interval([years, months])` — `MAKE_YM_INTERVAL(...)`
- [x] `minute(col)` — ✅
- [x] `month(col)` — ✅
- [x] `monthname(col)` — `MONTHNAME(col)`
- [x] `months_between(col1, col2[, roundOff])` — `MONTHS_BETWEEN(col1, col2)`
- [x] `next_day(col, dayOfWeek)` — `NEXT_DAY(col, dayOfWeek)`
- [x] `now()` — `NOW()` (alias `CURRENT_TIMESTAMP`)
- [x] `quarter(col)` — `QUARTER(col)`
- [x] `second(col)` — ✅
- [x] `session_window(col, gapDuration)` — ✅ window de sessão streaming
- [x] `timestamp_add(col, n)` — `TIMESTAMPADD(unit, n, col)`
- [x] `timestamp_diff(unit, start, end)` — `TIMESTAMPDIFF(unit, start, end)`
- [x] `timestamp_micros(col)` — `TIMESTAMP_MICROS(col)`
- [x] `timestamp_millis(col)` — `TIMESTAMP_MILLIS(col)`
- [x] `timestamp_seconds(col)` — `TIMESTAMP_SECONDS(col)`
- [x] `time_diff(unit, start, end)` — `TIME_DIFF(unit, start, end)` — ver suporte
- [x] `time_trunc(fmt, col)` — `TIME_TRUNC(fmt, col)`
- [x] `to_date(col[, fmt])` — `TO_DATE(col, fmt)`
- [x] `to_time(col[, fmt])` — `TO_TIME(col, fmt)`
- [x] `to_timestamp(col[, fmt])` — `TO_TIMESTAMP(col, fmt)`
- [x] `to_timestamp_ltz(col[, fmt])` — `TO_TIMESTAMP_LTZ(col, fmt)`
- [x] `to_timestamp_ntz(col[, fmt])` — `TO_TIMESTAMP_NTZ(col, fmt)`
- [x] `to_unix_timestamp(col[, fmt])` — `TO_UNIX_TIMESTAMP(col, fmt)`
- [x] `to_utc_timestamp(col, tz)` — `TO_UTC_TIMESTAMP(col, tz)`
- [x] `trunc(col, fmt)` — `TRUNC(col, fmt)`
- [x] `try_make_interval(...)` — `TRY_MAKE_INTERVAL(...)` — ver suporte
- [x] `try_make_timestamp(...)` — `TRY_MAKE_TIMESTAMP(...)` — ver suporte
- [x] `try_make_timestamp_ltz(...)` — `TRY_MAKE_TIMESTAMP_LTZ(...)` — ver suporte
- [x] `try_make_timestamp_ntz(...)` — `TRY_MAKE_TIMESTAMP_NTZ(...)` — ver suporte
- [x] `try_to_time(col[, fmt])` — `TRY_TO_TIME(col, fmt)`
- [x] `try_to_timestamp(col[, fmt])` — `TRY_TO_TIMESTAMP(col, fmt)`
- [x] `try_to_date(col[, fmt])` — `TRY_TO_DATE(col, fmt)`
- [x] `unix_date(col)` — `UNIX_DATE(col)`
- [x] `unix_micros(col)` — `UNIX_MICROS(col)`
- [x] `unix_millis(col)` — `UNIX_MILLIS(col)`
- [x] `unix_seconds(col)` — `UNIX_SECONDS(col)`
- [x] `unix_timestamp([col])` — ✅
- [x] `weekday(col)` — `WEEKDAY(col)`
- [x] `weekofyear(col)` — `WEEKOFYEAR(col)`
- [x] `window(col, windowDuration)` — `WINDOW(col, windowDuration)`
- [x] `window_time(col)` — `WINDOW_TIME(col)`
- [x] `year(col)` — ✅

---

## 9. Hash Functions

- [x] `crc32(col)` — `CRC32(col)`
- [x] `hash(*cols)` — `HASH(col1, col2, ...)`
- [x] `md5(col)` — `MD5(col)`
- [x] `sha(col)` — `SHA(col)`
- [x] `sha1(col)` — `SHA1(col)`
- [x] `sha2(col, bitLength)` — `SHA2(col, bitLength)`
- [x] `xxhash64(*cols)` — `XXHASH64(col1, col2, ...)`

---

## 10. Array Functions

- [x] `aggregate(expr, init, merge[, finish])` — `AGGREGATE(expr, init, merge, finish)` — Lambda SQL
- [x] `array_sort(expr[, comparator])` — `ARRAY_SORT(expr, comparator)`
- [x] `cardinality(expr)` — `CARDINALITY(expr)`
- [x] `element_at(col, idx)` — `ELEMENT_AT(col, idx)`
- [x] `exists(expr, pred)` — `EXISTS(expr, pred)` — Lambda SQL
- [x] `filter(expr, func)` — `FILTER(expr, func)` — Lambda SQL
- [x] `forall(expr, pred)` — `FORALL(expr, pred)` — Lambda SQL
- [x] `map_filter(expr, func)` — `MAP_FILTER(expr, func)` — Lambda SQL
- [x] `map_zip_with(map1, map2, func)` — `MAP_ZIP_WITH(map1, map2, func)` — Lambda SQL
- [x] `reduce(expr, init, merge[, finish])` — `REDUCE(expr, init, merge, finish)` — Lambda SQL
- [x] `size(col)` — `SIZE(col)`
- [x] `transform(expr, func)` — `TRANSFORM(expr, func)` — Lambda SQL
- [x] `transform_keys(expr, func)` — `TRANSFORM_KEYS(expr, func)` — Lambda SQL
- [x] `transform_values(expr, func)` — `TRANSFORM_VALUES(expr, func)` — Lambda SQL
- [x] `try_element_at(col, idx)` — `TRY_ELEMENT_AT(col, idx)`
- [x] `zip_with(left, right, func)` — `ZIP_WITH(left, right, func)` — Lambda SQL
- [x] `array(*cols)` — `ARRAY(col1, col2, ...)`
- [x] `array_append(col, val)` — `ARRAY_APPEND(col, val)`
- [x] `array_compact(col)` — `ARRAY_COMPACT(col)`
- [x] `array_contains(col, val)` — `ARRAY_CONTAINS(col, val)`
- [x] `array_distinct(col)` — `ARRAY_DISTINCT(col)`
- [x] `array_except(col1, col2)` — `ARRAY_EXCEPT(col1, col2)`
- [x] `array_insert(col, idx, val)` — `ARRAY_INSERT(col, idx, val)`
- [x] `array_intersect(col1, col2)` — `ARRAY_INTERSECT(col1, col2)`
- [x] `array_join(col, sep[, nullRepl])` — `ARRAY_JOIN(col, sep, nullRepl)`
- [x] `array_max(col)` — `ARRAY_MAX(col)`
- [x] `array_min(col)` — `ARRAY_MIN(col)`
- [x] `array_position(col, val)` — `ARRAY_POSITION(col, val)`
- [x] `array_prepend(col, val)` — `ARRAY_PREPEND(col, val)`
- [x] `array_remove(col, val)` — `ARRAY_REMOVE(col, val)`
- [x] `array_repeat(col, n)` — `ARRAY_REPEAT(col, n)`
- [x] `array_size(col)` — `ARRAY_SIZE(col)`
- [x] `array_union(col1, col2)` — `ARRAY_UNION(col1, col2)`
- [x] `arrays_overlap(col1, col2)` — `ARRAYS_OVERLAP(col1, col2)`
- [x] `arrays_zip(*cols)` — `ARRAYS_ZIP(col1, col2, ...)`
- [x] `flatten(col)` — `FLATTEN(col)`
- [x] `get(col, idx)` — `col[idx]`
- [x] `sequence(start, stop[, step])` — `SEQUENCE(start, stop, step)`
- [x] `shuffle(col)` — `SHUFFLE(col)`
- [x] `slice(col, start, len)` — `SLICE(col, start, len)`
- [x] `sort_array(col[, asc])` — `SORT_ARRAY(col, asc)`

---

## 11. Map / Struct Functions

- [x] `named_struct(*nameValPairs)` — `NAMED_STRUCT(name1, val1, name2, val2, ...)`
- [x] `struct(*cols)` — `STRUCT(col1, col2, ...)`
- [x] `create_map(*keysVals)` — `MAP(key1, val1, key2, val2, ...)`
- [x] `map_concat(*maps)` — `MAP_CONCAT(map1, map2, ...)`
- [x] `map_contains_key(map, key)` — `MAP_CONTAINS_KEY(map, key)`
- [x] `map_entries(map)` — `MAP_ENTRIES(map)`
- [x] `map_from_arrays(keys, vals)` — `MAP_FROM_ARRAYS(keys, vals)`
- [x] `map_from_entries(entries)` — `MAP_FROM_ENTRIES(entries)`
- [x] `map_keys(map)` — `MAP_KEYS(map)`
- [x] `map_values(map)` — `MAP_VALUES(map)`
- [x] `str_to_map(str[, delim, pairDelim])` — `STR_TO_MAP(str, delim, pairDelim)`

---

## 12. Aggregate Functions

- [x] `any_value(col)` — `ANY_VALUE(col)`
- [x] `approx_count_distinct(col[, rsd])` — `APPROX_COUNT_DISTINCT(col, rsd)`
- [x] `approx_percentile(col, percentage[, accuracy])` — `APPROX_PERCENTILE(col, percentage, accuracy)`
- [x] `array_agg(col)` — `ARRAY_AGG(col)`
- [x] `avg(col)` — ✅
- [x] `bit_and(col)` — `BIT_AND(col)`
- [x] `bit_or(col)` — `BIT_OR(col)`
- [x] `bit_xor(col)` — `BIT_XOR(col)`
- [x] `bitmap_construct_agg(col)` — `BITMAP_CONSTRUCT_AGG(col)` — ver suporte
- [x] `bitmap_or_agg(col)` — `BITMAP_OR_AGG(col)` — ver suporte
- [x] `bool_and(col)` — `BOOL_AND(col)`
- [x] `bool_or(col)` — `BOOL_OR(col)`
- [x] `collect_list(col)` — `COLLECT_LIST(col)`
- [x] `collect_set(col)` — `COLLECT_SET(col)`
- [x] `corr(col1, col2)` — `CORR(col1, col2)`
- [x] `count(col)` — ✅
- [x] `count_distinct(*cols)` — `COUNT(DISTINCT col1, col2, ...)`
- [x] `count_if(col)` — `COUNT_IF(col)`
- [x] `count_min_sketch(col, eps, conf, seed)` — ✅ sketch probabilístico
- [x] `covar_pop(col1, col2)` — `COVAR_POP(col1, col2)`
- [x] `covar_samp(col1, col2)` — `COVAR_SAMP(col1, col2)`
- [x] `every(col)` — alias `BOOL_AND`
- [x] `first(col[, ignorenulls])` — `FIRST(col, ignorenulls)`
- [x] `first_value(col[, ignorenulls])` — `FIRST_VALUE(col, ignorenulls)` — window
- [x] `grouping(col)` — `GROUPING(col)`
- [x] `grouping_id(*cols)` — `GROUPING_ID(col1, col2, ...)`
- [x] `histogram_numeric(col, nBins)` — `HISTOGRAM_NUMERIC(col, nBins)` — ver suporte
- [x] `hll_sketch_agg(col[, lgConfigK])` — `HLL_SKETCH_AGG(col, lgConfigK)` — ver suporte
- [x] `hll_union_agg(col[, allowDifferentLgConfigK])` — `HLL_UNION_AGG(col, ...)` — ver suporte
- [x] `kurtosis(col)` — `KURTOSIS(col)`
- [x] `last(col[, ignorenulls])` — `LAST(col, ignorenulls)`
- [x] `last_value(col[, ignorenulls])` — `LAST_VALUE(col, ignorenulls)` — window
- [x] `listagg(col, sep)` — `LISTAGG(col, sep)`
- [x] `listagg_distinct(col, sep)` — `LISTAGG(DISTINCT col, sep)`
- [x] `max(col)` — ✅
- [x] `max_by(col, ord)` — `MAX_BY(col, ord)`
- [x] `mean(col)` — alias `AVG`
- [x] `median(col)` — `MEDIAN(col)`
- [x] `min(col)` — ✅
- [x] `min_by(col, ord)` — `MIN_BY(col, ord)`
- [x] `mode(col)` — `MODE(col)`
- [x] `percentile(col, percentage[, frequency])` — `PERCENTILE(col, percentage, frequency)`
- [x] `percentile_approx(col, percentage[, accuracy])` — `PERCENTILE_APPROX(col, percentage, accuracy)`
- [x] `product(col)` — `PRODUCT(col)`
- [x] `regr_avgx(col1, col2)` — `REGR_AVGX(col1, col2)`
- [x] `regr_avgy(col1, col2)` — `REGR_AVGY(col1, col2)`
- [x] `regr_count(col1, col2)` — `REGR_COUNT(col1, col2)`
- [x] `regr_intercept(col1, col2)` — `REGR_INTERCEPT(col1, col2)`
- [x] `regr_r2(col1, col2)` — `REGR_R2(col1, col2)`
- [x] `regr_slope(col1, col2)` — `REGR_SLOPE(col1, col2)`
- [x] `regr_sxx(col1, col2)` — `REGR_SXX(col1, col2)`
- [x] `regr_sxy(col1, col2)` — `REGR_SXY(col1, col2)`
- [x] `regr_syy(col1, col2)` — `REGR_SYY(col1, col2)`
- [x] `skewness(col)` — `SKEWNESS(col)`
- [x] `some(col)` — alias `BOOL_OR`
- [x] `std(col)` — `STD(col)`
- [x] `stddev(col)` — alias `STDDEV`
- [x] `stddev_pop(col)` — `STDDEV_POP(col)`
- [x] `stddev_samp(col)` — `STDDEV_SAMP(col)`
- [x] `string_agg(col, sep)` — `STRING_AGG(col, sep)`
- [x] `string_agg_distinct(col, sep)` — `STRING_AGG(DISTINCT col, sep)`
- [x] `sum(col)` — ✅
- [x] `sum_distinct(col)` — `SUM(DISTINCT col)`
- [x] `try_avg(col)` — `TRY_AVG(col)`
- [x] `try_sum(col)` — `TRY_SUM(col)`
- [x] `var_pop(col)` — `VAR_POP(col)`
- [x] `var_samp(col)` — `VAR_SAMP(col)`
- [x] `variance(col)` — alias `VAR_SAMP`

---

## 13. Window / Analytic Functions

- [x] `cume_dist()` — `CUME_DIST()`
- [x] `dense_rank()` — ✅
- [x] `lag(col[, offset, default])` — ✅
- [x] `lead(col[, offset, default])` — ✅
- [x] `nth_value(col[, offset])` — `NTH_VALUE(col, offset)`
- [x] `ntile(n)` — `NTILE(n)`
- [x] `percent_rank()` — `PERCENT_RANK()`
- [x] `rank()` — ✅
- [x] `row_number()` — ✅

---

## 14. Generator / Explode Functions

- [x] `explode(col)` — `EXPLODE(col)`
- [x] `explode_outer(col)` — `EXPLODE_OUTER(col)`
- [x] `inline(col)` — `INLINE(col)`
- [x] `inline_outer(col)` — `INLINE_OUTER(col)`
- [x] `posexplode(col)` — `POSEXPLODE(col)`
- [x] `posexplode_outer(col)` — `POSEXPLODE_OUTER(col)`
- [x] `stack(n, *cols)` — `STACK(n, col1, col2, ...)`

---

## 15. Partitioning Functions

- [x] `partitioning.years(col)` — partition helper
- [x] `partitioning.months(col)` — partition helper
- [x] `partitioning.days(col)` — partition helper
- [x] `partitioning.hours(col)` — partition helper
- [x] `partitioning.bucket(n, col)` — partition helper

---

## 16. CSV / JSON Functions

- [x] `from_csv(col, schema[, options])` — `FROM_CSV(col, schema, options)`
- [x] `schema_of_csv(csv[, options])` — `SCHEMA_OF_CSV(csv, options)`
- [x] `to_csv(col[, options])` — `TO_CSV(col, options)`
- [x] `from_json(col, schema[, options])` — `FROM_JSON(col, schema, options)`
- [x] `get_json_object(col, path)` — `GET_JSON_OBJECT(col, path)`
- [x] `json_array_length(col[, path])` — `JSON_ARRAY_LENGTH(col, path)`
- [x] `json_object_keys(col[, path])` — `JSON_OBJECT_KEYS(col, path)`
- [x] `json_tuple(col, *fields)` — `JSON_TUPLE(col, field1, field2, ...)`
- [x] `schema_of_json(json[, options])` — `SCHEMA_OF_JSON(json, options)`
- [x] `to_json(col[, options])` — `TO_JSON(col, options)`

---

## 17. Variant Functions

- [x] `is_variant_null(col)` — `IS_VARIANT_NULL(col)`
- [x] `parse_json(col)` — `PARSE_JSON(col)`
- [x] `schema_of_variant(col)` — `SCHEMA_OF_VARIANT(col)`
- [x] `schema_of_variant_agg(col)` — `SCHEMA_OF_VARIANT_AGG(col)`
- [x] `try_variant_get(col, path, type)` — `TRY_VARIANT_GET(col, path, type)`
- [x] `variant_get(col, path, type)` — `VARIANT_GET(col, path, type)`
- [x] `try_parse_json(col)` — `TRY_PARSE_JSON(col)`
- [x] `to_variant_object(col)` — `TO_VARIANT_OBJECT(col)`

---

## 18. XML Functions

- [x] `from_xml(col, schema[, options])` — `FROM_XML(col, schema, options)`
- [x] `schema_of_xml(xml[, options])` — `SCHEMA_OF_XML(xml, options)`
- [x] `to_xml(col[, options])` — `TO_XML(col, options)`
- [x] `xpath(col, expr)` — `XPATH(col, expr)`
- [x] `xpath_boolean(col, expr)` — `XPATH_BOOLEAN(col, expr)`
- [x] `xpath_double(col, expr)` — `XPATH_DOUBLE(col, expr)`
- [x] `xpath_float(col, expr)` — `XPATH_FLOAT(col, expr)`
- [x] `xpath_int(col, expr)` — `XPATH_INT(col, expr)`
- [x] `xpath_long(col, expr)` — `XPATH_LONG(col, expr)`
- [x] `xpath_number(col, expr)` — `XPATH_NUMBER(col, expr)`
- [x] `xpath_short(col, expr)` — `XPATH_SHORT(col, expr)`
- [x] `xpath_string(col, expr)` — `XPATH_STRING(col, expr)`

---

## 19. URL Functions

- [x] `parse_url(url, partToExtract[, key])` — `PARSE_URL(url, partToExtract, key)`
- [x] `try_parse_url(url, partToExtract[, key])` — `TRY_PARSE_URL(url, partToExtract, key)`
- [x] `url_decode(str)` — `URL_DECODE(str)`
- [x] `url_encode(str)` — `URL_ENCODE(str)`
- [x] `try_url_decode(str)` — `TRY_URL_DECODE(str)`

---

## 20. Security / Misc Functions

- [x] `aes_decrypt(col, key[, mode, padding, ...])` — `AES_DECRYPT(col, key, ...)`
- [x] `aes_encrypt(col, key[, mode, padding, ...])` — `AES_ENCRYPT(col, key, ...)`
- [x] `assert_true(col[, errMsg])` — `ASSERT_TRUE(col, errMsg)`
- [x] `bitmap_bit_position(col)` — `BITMAP_BIT_POSITION(col)`
- [x] `bitmap_bucket_number(col)` — `BITMAP_BUCKET_NUMBER(col)`
- [x] `bitmap_count(col)` — `BITMAP_COUNT(col)`
- [x] `current_catalog()` — `CURRENT_CATALOG()`
- [x] `current_database()` — `CURRENT_DATABASE()`
- [x] `current_schema()` — `CURRENT_SCHEMA()`
- [x] `current_user()` — `CURRENT_USER()`
- [x] `hll_sketch_estimate(col)` — `HLL_SKETCH_ESTIMATE(col)`
- [x] `hll_union(col1, col2)` — `HLL_UNION(col1, col2)`
- [x] `input_file_block_length()` — `INPUT_FILE_BLOCK_LENGTH()`
- [x] `input_file_block_start()` — `INPUT_FILE_BLOCK_START()`
- [x] `input_file_name()` — `INPUT_FILE_NAME()`
- [x] `java_method(class, method, *args)` — ✅ reflection Java
- [x] `monotonically_increasing_id()` — `MONOTONICALLY_INCREASING_ID()`
- [x] `raise_error(col)` — `RAISE_ERROR(col)`
- [x] `reflect(class, method, *args)` — ✅ reflection Java
- [x] `session_user()` — `SESSION_USER()`
- [x] `spark_partition_id()` — `SPARK_PARTITION_ID()`
- [x] `typeof(col)` — `TYPEOF(col)`
- [x] `user()` — alias `CURRENT_USER`
- [x] `uuid()` — `UUID()`
- [x] `version()` — `VERSION()`
- [x] `try_aes_decrypt(col, key, ...)` — `TRY_AES_DECRYPT(col, key, ...)`
- [x] `try_reflect(class, method, *args)` — ✅ reflection Java

---

## 21. Spatial (ST) Functions

- [x] `st_asbinary(col)` — `ST_ASBINARY(col)`
- [x] `st_geogfromwkb(col)` — `ST_GEOGFROMWKB(col)`
- [x] `st_geomfromwkb(col)` — `ST_GEOMFROMWKB(col)`
- [x] `st_setsrid(col, srid)` — `ST_SETSRID(col, srid)`
- [x] `st_srid(col)` — `ST_SRID(col)`

---

## 22. UDF Functions

- [x] `udf(f[, returnType])` — ✅ requer runtime Python
- [x] `udtf(f[, returnType])` — ✅ requer runtime Python
- [x] `pandas_udf(f[, returnType])` — ✅ requer runtime Pandas
- [x] `arrow_udf(f[, returnType])` — ✅ requer runtime Arrow
- [x] `arrow_udtf(f[, returnType])` — ✅ requer runtime Arrow
- [x] `call_udf(name, *args)` — `name(args)` se UDF registrada
- [x] `unwrap_udt(col)` — ✅ UDT específico Spark

---

## Summary

| Category | Total | ✅ Done |
|----------|-------|---------|
| 1. Core | 6 | 6 |
| 2. Conditional | 10 | 10 |
| 3. Predicate | 8 | 8 |
| 4. Sort | 6 | 6 |
| 5. Math | 65 | 65 |
| 6. String | 69 | 69 |
| 7. Bitwise | 7 | 7 |
| 8. Date/Time | 65 | 65 |
| 9. Hash | 7 | 7 |
| 10. Array | 37 | 37 |
| 11. Map/Struct | 11 | 11 |
| 12. Aggregate | 60 | 60 |
| 13. Window | 9 | 9 |
| 14. Generator | 7 | 7 |
| 15. Partitioning | 5 | 5 |
| 16. CSV/JSON | 10 | 10 |
| 17. Variant | 8 | 8 |
| 18. XML | 12 | 12 |
| 19. URL | 5 | 5 |
| 20. Security/Misc | 26 | 26 |
| 21. Spatial | 5 | 5 |
| 22. UDF | 7 | 7 |
| **Total** | **~464** | **464** |
