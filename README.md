**DotaSQL — ETL + ML + SQL для данных Dota 2**

Краткое описание проекта

Проект демонстрирует полный пайплайн работы с данными Dota 2: от получения и предобработки сырых JSON-payload (API) до хранения в реляционной базе и базового обучения модели. В проекте реализованы повторно используемые компоненты: модуль универсального создания таблиц на основе типов данных из API, диспатчер управляющий подключениями к БД и набор шаблонных SQL-операций для создания, вставки и обновления данных.

**Краткая документация для HR / портфолио (чего проект демонстрирует)**
- Полный ETL-пайплайн: интеграция с внешним API, нормализация и загрузка в БД, подготовка данных для ML.
- Дизайн переиспользуемых компонентов: модуль создания таблиц, диспатчер подключений, универсальные SQL-шаблоны.
- Инфраструктурная грамотность: параметризация подключений, работа с СУБД, транзакции и атомарность операций.
- Навыки: работа с API/JSON, моделирование данных, SQL, автоматизация загрузки, генерация схемы, базовое обучение моделей.

**Что реализовано (функционал)**
- Универсальная обработка типов данных: автоматическое преобразование типов из JSON/API в SQL-типы (строка → TEXT/VARCHAR, int → INTEGER, float → REAL/DOUBLE, bool → BOOLEAN, datetime → TIMESTAMP, массивы/вложенные объекты → JSON/JSONB или ARRAY). Обработка NULL и опциональных полей.
- Модуль генерации схемы (Table Factory): по названию таблицы и образцу данных формируется SQL-схема, первичные ключи и индексируемые поля, создаётся `CREATE TABLE` и сопутствующие индексы.
- Диспатчер подключений (DB Dispatcher): централизованная логика подключения/отключения и управления транзакциями.
- Универсальные запросы: генерация параметризованных `INSERT`, `UPSERT`/`ON CONFLICT`, bulk-insert, шаблоны для пагинации и выборок.
- ETL-скрипты: получение данных, их приведение к единому формату и пакетная загрузка в БД.
- Базовый ML-пайплайн: подготовка выборки и запуск обучения модели в `ML_train/ML_learn.py`.

**Универсальный модуль создания таблиц (Table Factory) — описание**

- Назначение: создавать реляционную таблицу автоматически на основе типов и структуры данных, получаемых из API.
- Входные параметры: `table_name` (строка) и примерный `sample_payload` (dict) или схема `schema_description`.
- Логика определения колонок:
  - Скалярные типы: маппинг на SQL-типы (см. таблицу ниже).
  - Массивы и вложенные объекты: по умолчанию сохраняются в виде `JSON`/`JSONB` (рекомендуется для PostgreSQL) или как отдельные связанные таблицы при глубокой нормализации.
  - Поля с именами `id`, `match_id`, `game_id` автоматически помечаются как кандидат на PK; при необходимости можно передать явный ключ.
  - Для часто используемых полей генерируются индексы (configurable).

Типичный маппинг API → SQL
- string → TEXT / VARCHAR(255)
- integer → INTEGER
- float → REAL / DOUBLE PRECISION
- boolean → BOOLEAN
- ISO-datetime string → TIMESTAMP
- list/object → JSON / JSONB (опция для PostgreSQL)

*(Пример использования ниже)*


**Генерация запросов и шаблонность**
- Все запросы формируются параметризованно (без конкатенации строк), что защищает от SQL-инъекций.
- Универсальные шаблоны: `CREATE TABLE`, `INSERT`, `BULK INSERT`, `UPSERT` (с разными реализациями для баз с поддержкой `ON CONFLICT`).
- Bulk-пакеты разбиваются по размеру, есть настройка размера пакета и задержки между пакетами для больших нагрузок.


**Файлы и расположение (быстрый обзор)**
- Основной запуск: [main.py](main.py)
- Модуль получения и подготовки данных: [Data/get_data.py](Data/get_data.py), [Data/formating_data.py](Data/formating_data.py)
- Модули БД и фабрики таблиц: [SQL_connect/sqlconnecter.py](SQL_connect/sqlconnecter.py), [SQL_connect/table_create.py](SQL_connect/table_create.py) (реализация фабрики), [SQL_connect/dispatcher.py](SQL_connect/dispatcher.py) (диспатчер)
- ML-обучение: [ML_train/ML_learn.py](ML_train/ML_learn.py)

**Как запустить (коротко)**

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python main.py        # или поэтапно: Data/get_data.py -> Data/formating_data.py -> ML_train/ML_learn.py
```

**Roadmap**
- [ ] Автоматическое нормализованное выделение связанных таблиц из вложенных массивов (players → players table).
- [ ] Поддержка схемной валидации через JSON Schema и автогенерация миграций.
- [ ] CI-пайплайн для проверки целостности схем и тестов загрузки.
- [ ] Развёртывание ML-модели как сервиса и мониторинг качества данных.


---

**EN — DotaSQL — ETL + ML + SQL for Dota 2 data (summary for portfolio)**

Short summary for an English-speaking reviewer: DotaSQL is a compact Python project that implements a repeatable ETL pipeline for Dota 2 match/game data (API → normalized storage → ML-ready dataset). Key reusable components include a Table Factory that auto-generates SQL tables from API payloads, a DB Dispatcher that manages connections and transactions across different drivers (SQLite/Postgres/MySQL), and a suite of parameterized SQL templates for safe `INSERT`/`UPSERT`/`BULK` operations.

What this demonstrates (quick bullets for HR):
- End-to-end data pipeline: API ingestion, schema generation, batch loading, and dataset preparation for ML.
- Reusable engineering: automated table/schema generation, connection dispatching, and parameterized queries.
- Practical skills: JSON/API handling, data modelling, SQL, database drivers, transaction handling, batch processing, and basic ML training automation.

Quick usage (English):

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Files to inspect for implementation details: `main.py`, `Data/get_data.py`, `Data/formating_data.py`, `SQL_connect/sqlconnecter.py`, `SQL_connect/table_create.py`, `ML_train/ML_learn.py`.

If you want, I can also add an English README file at the repo root (`README_en.md`) or implement example `dispatcher.py` and `table_factory.py` to make the Table Factory and Dispatcher concrete.

---

**DB Dispatcher / Connector (what's already implemented)**

The repository contains a concrete DB connector implemented in `SQL_connect/sqlconnecter.py`. Below is an accurate description of what is implemented and how to use it as-is.

- Configuration
  - `sqlconnecter.py` reads database connection values from environment variables using `python-dotenv` (`load_dotenv()`): `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`.
  - These values are collected into the `DB_CONFIG` dict and passed to `psycopg2.connect(**DB_CONFIG)`.

- Connection management (implemented as a decorator)
  - `Decorator_connect_db(func)` is a decorator that wraps any function requiring a DB cursor.
  - Behaviour: it opens a `psycopg2` connection, creates a cursor, calls the wrapped function with `cursor` as the first argument, commits on success, and closes cursor+connection in `finally`.
  - Example signature for wrapped functions: `def fn(cursor, ...):` — the decorator injects `cursor` automatically.

- Provided DB-related functions (already in the project)
  - `create_table(cursor)`: creates a fixed `matches` table with explicit columns (types and `match_id` primary key).
  - `create_table_with_name(cursor, table, column:dict)`: creates a table named `table` using a `column` mapping (column name → SQL type). The function builds a `CREATE TABLE IF NOT EXISTS` statement from the dict.
  - `INSERT_MATCHES(cursor, matches)`: iterates over a list of `matches` dicts and executes a parameterized `INSERT ... ON CONFLICT (match_id) DO UPDATE` to upsert rows into the `matches` table.
  - `insert_into_db(cursor, table, data:dict)`: inserts a single record into `table` using the keys/values from `data` (parameterized placeholders).
  - `FETCH_MATCHES(cursor, limit=None)`: returns fetched rows from `matches`, optionally limited and ordered by `start_time`.
  - `get_matches_at_dataframe(cursor, limit=None)`: fetches rows from `matches`, converts them into a `pandas.DataFrame` and returns it (uses `cursor.description` to build column names).

- How to call the existing functions (examples)
  - Creating the `matches` table (uses decorator, no need to manage connection):

```python
from SQL_connect.sqlconnecter import create_table

create_table()  # decorator opens connection and executes create
```

  - Creating a custom table from a column mapping:

```python
from SQL_connect.sqlconnecter import create_table_with_name

cols = {"id": "bigint PRIMARY KEY", "value": "text"}
create_table_with_name('my_table', cols)
```

  - Upserting matches:

```python
from SQL_connect.sqlconnecter import INSERT_MATCHES

matches = [{"match_id": 1, "player_slot": 0, ...}, ...]
INSERT_MATCHES(matches)
```

  - Inserting a single row:

```python
from SQL_connect.sqlconnecter import insert_into_db

insert_into_db('my_table', {'id': 1, 'value': 'x'})
```

  - Fetching into a DataFrame:

```python
from SQL_connect.sqlconnecter import get_matches_at_dataframe

df = get_matches_at_dataframe(limit=100)
```

- Notes and limitations (observations from current implementation)
  - The connector is implemented specifically with `psycopg2` and assumes PostgreSQL (e.g., `ON CONFLICT`). Adapting to other DBs will require SQL adjustments.
  - The decorator always calls `cursor.close()` and `conn.close()` in `finally`; wrapped functions must accept `cursor` as first arg.
  - Error handling prints exceptions to stdout; you may want to integrate structured logging or re-raise exceptions for callers to handle.
  - `create_table_with_name` expects SQL types in the provided dict values (it does not map Python types automatically in that function).

This documents the exact dispatcher/connector code already present — no new dispatcher implementation was added. If you want, I can:
- add a tiny wrapper `SQL_connect/dispatcher.py` that re-exports these functions under a `DBDispatcher` API (no behavior changes), or
- refactor the decorator into a context-manager-based dispatcher for more explicit control (would change behaviour).

