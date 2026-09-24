---
name: sqlalchemy-alembic-expert
description: This skill should be used when writing, reviewing, or refactoring SQLAlchemy ORM models, DAL/repository classes, async session configuration, connection pool tuning, or Alembic migration scripts in Python async backends (asyncpg/PostgreSQL). Covers SQLAlchemy 2.x patterns (DeclarativeBase, Mapped[], mapped_column), async engine configuration, NullPool strategy, Generic BaseDAL pattern, db_error_handler decorator, upsert via pg_insert().on_conflict_do_update(), eager loading to prevent N+1, Alembic env.py async pattern, naming conventions for constraints, migration hygiene, and pytest integration using alembic upgrade head + NullPool. Trigger phrases: SQLAlchemy, Alembic, migration, ORM model, AsyncSession, DAL, session management, connection pool, eager loading, N+1, upsert, JSONB mutation, DeclarativeBase, mapped_column, alembic revision, autogenerate.
metadata:
  category: database
  source:
    repository: https://github.com/sqlalchemy/sqlalchemy
    path: docs/orm/extensions/asyncio.html
---

# SQLAlchemy + Alembic Expert

Specialised guidance for SQLAlchemy 2.x ORM and Alembic migrations in async Python backends (PostgreSQL/asyncpg). Detailed reference: [`references/best-practices.md`](references/best-practices.md).

---

## Quick Decision Map

| Task | Go-to pattern |
|---|---|
| New model | `DeclarativeBase` + `Mapped[]` + `mapped_column()` |
| New shared field | Mixin class (`TimestampMixin`, `WithID`) |
| New migration | `alembic revision --autogenerate -m "..."` → review → add `downgrade()` |
| Production engine | `create_async_engine(dsn, pool_pre_ping=True, pool_size=20, max_overflow=0)` |
| Alembic / test engine | `poolclass=pool.NullPool` |
| Bulk insert / upsert | `pg_insert().on_conflict_do_update()` |
| Multi-object read | `selectinload()` or `joinedload()` (bare attribute access = N+1) |
| Raw SQL | `text("... WHERE id = :id")` with bound params — never f-strings |
| rowcount from DML | `_rowcount(result)` helper using `cast(CursorResult, result).rowcount` |
| JSONB mutation | Reassign the whole dict: `obj.data = {**obj.data, "k": "v"}` |

---

## Non-negotiable Rules

1. **`expire_on_commit=False`** on every `async_sessionmaker` — mandatory in async, prevents `MissingGreenlet`.
2. **One session per unit of work.** Never share an `AsyncSession` between concurrent `asyncio.Task`s.
3. **Always `await`** `session.execute()`, `session.flush()`, `session.commit()`, `session.close()`.
4. **`NullPool`** for Alembic `env.py` and all test engines.
5. **`pool_pre_ping=True`** for every production engine.
6. **All models imported in `env.py`** before `autogenerate` runs — missing import = missing migration.
7. **`naming_convention` on `MetaData`** — deterministic constraint names prevent `alembic downgrade` failures.
8. **Never edit an applied migration.** Create a new one.
9. **`downgrade()` must be implemented** in every migration file.
10. **`alembic check`** must pass in CI before any deployment.

---

## Models (SQLAlchemy 2.x)

```python
from datetime import datetime
from sqlalchemy import MetaData, String, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=NAMING_CONVENTION)

class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

class User(TimestampMixin, Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str | None] = mapped_column(String(255))  # Optional = nullable
```

---

## Async Session

```python
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

engine = create_async_engine(
    dsn,
    pool_pre_ping=True,   # required in production
    pool_size=20,
    max_overflow=0,
    pool_recycle=3600,
    echo=False,
)
async_session = async_sessionmaker(engine, expire_on_commit=False)

# Usage — always as context manager
async with async_session() as session:
    async with session.begin():
        session.add(obj)
    # auto-commit on success; auto-rollback on exception
```

---

## Alembic `env.py` (Async Pattern)

```python
import asyncio
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context

# Import ALL models here — missing import = missing migration
from myapp.models import Base
import myapp.other_models  # noqa: F401

target_metadata = Base.metadata

def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations():
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as conn:
        await conn.run_sync(do_run_migrations)
    await connectable.dispose()

def run_migrations_online():
    asyncio.run(run_async_migrations())
```

---

## Generic DAL / Repository

```python
from typing import Generic, TypeVar, Type, Any, cast
import functools
from sqlalchemy.engine import CursorResult
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

Model = TypeVar("Model", bound=Base)

def _rowcount(result: Any) -> int:
    """Return DML rowcount; works around Result[Any] vs CursorResult type gap."""
    return cast(CursorResult[Any], result).rowcount

def db_error_handler(func):
    @functools.wraps(func)
    async def wrapper(self, *args, **kwargs):
        try:
            return await func(self, *args, **kwargs)
        except IntegrityError as exc:
            if getattr(exc.orig, "pgcode", "") == "23505":
                raise UniqueConstraintError("Unique constraint violated") from exc
            raise DBIntegrityError() from exc
        except SQLAlchemyError as exc:
            raise DBIntegrityError() from exc
    return wrapper

class BaseDAL(Generic[Model]):
    model: Type[Model]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, pk: int) -> Model | None:
        return await self.session.get(self.model, pk)

    @db_error_handler
    async def create(self, data: dict) -> Model:
        obj = self.model(**data)
        self.session.add(obj)
        await self.session.flush()
        return obj
```

---

## Testing Setup

```python
# conftest.py
import subprocess, asyncio
from sqlalchemy import NullPool, create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy_utils import create_database, drop_database

def pytest_sessionstart(session):
    create_database(SYNC_TEST_URI)
    subprocess.run(["alembic", "-c", ALEMBIC_INI, "upgrade", "head"], check=True)

def pytest_sessionfinish(session, exitstatus):
    close_all_sessions()
    drop_database(SYNC_TEST_URI)

# Per-test rollback fixture
@pytest_asyncio.fixture
async def db_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    conn = await test_engine.connect()
    trans = await conn.begin()
    session = AsyncSession(bind=conn, expire_on_commit=False)
    try:
        yield session
    finally:
        await session.close()
        await trans.rollback()
        await conn.close()
```

Add to `pyproject.toml`:
```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
```

---

## Alembic CLI Reference

```bash
alembic revision --autogenerate -m "description"  # generate (always review!)
alembic upgrade head        # apply all pending
alembic current             # current revision
alembic history --verbose   # full history
alembic check               # CI gate — fails if model changes lack migration
alembic downgrade -1        # roll back one step
alembic upgrade head --sql  # dry run — print SQL only
alembic merge -m "merge" rev1 rev2  # resolve forked heads
```

---

## Top Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| N+1 queries | Thousands of SELECT for loop | `selectinload` / `joinedload` |
| `DetachedInstanceError` | Attribute access after session close | `expire_on_commit=False` or load inside context |
| JSONB not saved | Mutation looks right but DB unchanged | Reassign whole dict |
| Forgot `await` | Silent no-op | All session methods are coroutines |
| Shared session in tasks | Race conditions / corruption | One session per task |
| Missing model import in env.py | `autogenerate` produces empty migration | Import all model modules |
| No `naming_convention` | `alembic downgrade` fails on FK names | Add to `MetaData` |

---

## References

See [`references/best-practices.md`](references/best-practices.md) for complete documentation with:
- Full SQLAlchemy 2.x model patterns with examples
- Eager loading strategy comparison table
- Zero-downtime migration table (nullable, NOT NULL, rename, index CONCURRENTLY)
- asyncpg + PgBouncer statement cache configuration
- Sentry integration patterns
- `alembic-postgresql-enum` plugin for ENUM migrations
