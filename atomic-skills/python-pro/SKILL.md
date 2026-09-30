---
name: python-pro
description: Use for modern Python development across CPython 3.10-3.14 when version-aware typing, asyncio, testing, packaging, performance, or migration guidance is required. Always identify the supported Python range before choosing syntax or runtime features, and gate 3.11/3.12/3.13/3.14-only capabilities explicitly.
license: MIT
metadata:
  author: https://github.com/Jeffallan
  version: "1.2.0"
  domain: language
  triggers: Python development, Python 3.10, Python 3.11, Python 3.12, Python 3.13, Python 3.14, type hints, async Python, pytest, mypy, dataclasses, Python best practices, Pythonic code, Python migration
  role: specialist
  scope: implementation
  output-format: code
  python-versions: "3.10-3.14"
  related-skills: fastapi-expert, python-dev, devops-engineer
---

# Python Pro

Version-aware modern Python specialist for CPython 3.10-3.14, focused on type safety, structured concurrency, robust errors, testing, packaging, and production readiness.

## Version applicability

**Applies to:** Python 3.10, 3.11, 3.12, 3.13, and 3.14.

Before writing or reviewing code, determine the project's minimum and maximum supported Python versions. Never emit syntax or APIs newer than the declared minimum unless the user explicitly requests a migration.

Current lifecycle policy (2026-09):
- **3.10:** security-only, EOL in October 2026. Treat as legacy compatibility; do not select for new long-lived projects.
- **3.11:** security-only. Preserve when required by deployed environments, but avoid introducing it as a new baseline without a compatibility reason.
- **3.12:** security-only. Good compatibility floor when ecosystem constraints require it, but no longer receives regular bugfix releases.
- **3.13:** bugfix-supported. Prefer as the conservative modern baseline when dependencies are compatible.
- **3.14:** bugfix-supported and latest stable. Prefer for greenfield projects when dependencies and deployment targets support it.

For exact lifecycle dates and version-specific capabilities, load `references/version-compatibility.md`.

## Version-gating rules

Use these markers whenever a feature is not valid across the whole 3.10-3.14 range:

- **[3.10+]** structural pattern matching, `X | Y` unions, `ParamSpec`, `TypeGuard`, dataclass `slots=` and `kw_only=`.
- **[3.11+]** `asyncio.TaskGroup`, `ExceptionGroup` / `except*`, `tomllib`, `typing.Self`, `Required` / `NotRequired`, variadic generics.
- **[3.12+]** PEP 695 type-parameter syntax and `type Alias = ...`, PEP 701 unrestricted f-string expressions. `distutils` is removed.
- **[3.13+]** type-parameter defaults; changed `locals()` semantics. Free-threaded CPython and JIT exist in 3.13 but are experimental and must not be assumed.
- **[3.14+]** deferred annotation evaluation, `annotationlib`, template strings, `concurrent.interpreters`, `compression.zstd`; free-threaded CPython is officially supported but remains optional.

When supporting multiple versions, prefer the oldest-version-compatible spelling or use `typing_extensions` / conditional imports where that is materially simpler than raising the minimum version.

## When to use this skill

- Writing, reviewing, or modernizing Python 3.10-3.14 code.
- Choosing a project minimum Python version.
- Migrating between 3.10 → 3.11 → 3.12 → 3.13 → 3.14.
- Writing type-safe public APIs and internal domain code.
- Implementing async I/O and structured concurrency.
- Setting up pytest, mypy/pyright, Ruff, formatting, and packaging.
- Evaluating free-threaded CPython, subinterpreters, or JIT-related changes.
- Auditing code for deprecated/removed stdlib behavior.

## Core workflow

1. **Resolve version policy** — Read `requires-python`, CI matrices, Docker/runtime images, deployment platform, and type-checker target version.
2. **Analyze codebase** — Review structure, dependencies, typing coverage, async model, tests, and packaging.
3. **Design interfaces** — Prefer explicit protocols, dataclasses/typed models, and stable boundaries.
4. **Implement with version gates** — Use only features valid for the supported floor.
5. **Test across supported minors** — CI must include the minimum and maximum supported Python versions; add intermediates where dependency or interpreter behavior is version-sensitive.
6. **Validate** — Run the project's formatter/linter/type checker/tests; do not claim success for commands that were not actually run.
7. **Migration check** — For interpreter upgrades, review deprecations/removals and runtime behavior changes before changing the CI default.

## Reference guide

| Topic | Reference | Load when |
| --- | --- | --- |
| Version matrix | `references/version-compatibility.md` | Choosing/migrating Python 3.10-3.14, syntax/API availability |
| Type system | `references/type-system.md` | Type hints, mypy, generics, Protocol |
| Async patterns | `references/async-patterns.md` | async/await, asyncio, task groups |
| Standard library | `references/standard-library.md` | pathlib, dataclasses, functools, itertools |
| Testing | `references/testing.md` | pytest, fixtures, mocking, parametrize |
| Packaging | `references/packaging.md` | pyproject.toml, pip/uv/Poetry, distributions |

## Best practices

### Runtime baseline and compatibility
- Declare `requires-python` in `pyproject.toml`; keep it consistent with classifiers, CI, type-checker config, Docker images, and deployment runtime.
- Do not set a type checker to one Python version while package metadata says another.
- For libraries, test the minimum supported version explicitly. For applications, test production plus the next intended upgrade target.
- Keep 3.10 compatibility only for an explicit need; its security support ends in October 2026.

### Typing
- **[3.10+]** Prefer `X | None` and built-in generics.
- **[3.11+]** Use `Self`, `Required`, and `NotRequired` when the minimum permits; otherwise use `typing_extensions`.
- **[3.12+]** PEP 695 syntax is cleaner, but do not use it in code that still supports 3.11 or earlier.
- **[3.14+]** Do not depend on eager annotation side effects. Runtime introspection should prefer documented `annotationlib` APIs.
- Static types do not replace runtime validation at untrusted boundaries.

### Async and concurrency
- Use async for I/O concurrency, not as a blanket replacement for synchronous code.
- **[3.11+]** Prefer `asyncio.TaskGroup` for related child tasks when failure should cancel siblings.
- Apply explicit timeouts around external I/O and preserve cancellation.
- Avoid fire-and-forget tasks unless ownership, shutdown, and error reporting are explicit.
- **[3.13]** Free-threaded builds are experimental: benchmark and test dependencies/C extensions.
- **[3.14+]** Free-threaded builds are supported but optional. Audit shared mutable state and extension compatibility.
- **[3.14+]** Prefer `asyncio.run(..., loop_factory=...)` or `asyncio.Runner`; event-loop policies are deprecated for removal in 3.16.

### Errors
- Catch the narrowest exception that you can handle meaningfully.
- Preserve causes with `raise ... from ...` when translating exceptions.
- **[3.11+]** Use `ExceptionGroup` / `except*` only for genuinely grouped failures.
- Never swallow cancellation or broad exceptions merely to keep a service alive.

### Testing
- Favor deterministic unit tests and focused integration tests.
- Test behavior, not implementation details.
- CI must include the minimum and maximum supported Python minors.
- Add migration tests for annotation introspection, serialization, asyncio cancellation/scheduling, and C-extension integration when relevant.
- Coverage is a diagnostic metric, not a universal quality target.

### Packaging and tools
- Use `pyproject.toml` as source of truth.
- Do not use `distutils`; it is removed in Python 3.12.
- Prefer reproducible dependency workflows and committed lockfiles for applications.
- Libraries should avoid unnecessary dependency upper bounds.
- Follow the repository's existing formatter/linter/type-checker/package-manager standard; do not force Black, mypy, Poetry, or any specific tool.

## Compatibility examples

### Code supporting Python 3.10-3.14

```python
from collections.abc import Iterable

def total(values: Iterable[int]) -> int:
    return sum(values)

def find_name(user_id: int) -> str | None:
    ...
```

### Structured concurrency [3.11+]

```python
import asyncio

async def fetch_both() -> tuple[bytes, bytes]:
    async with asyncio.TaskGroup() as tg:
        first = tg.create_task(fetch("/a"))
        second = tg.create_task(fetch("/b"))
    return first.result(), second.result()
```

### PEP 695 generic syntax [3.12+ only]

```python
def first[T](items: list[T]) -> T:
    return items[0]

type UserId = int
```

If Python 3.10 or 3.11 is supported, use older `TypeVar` / assignment-style alias syntax.

## Output requirements

Report:
1. Supported Python range.
2. Version-specific features used, marked with minimum version.
3. Files/tests/tooling changed.
4. Validation actually executed and result.
5. Upgrade/compatibility risks.

## Knowledge reference

CPython 3.10-3.14, Python Developer's Guide lifecycle, typing and typing_extensions, asyncio, pytest, Ruff, mypy/pyright, pyproject.toml packaging, free-threaded CPython, subinterpreters, annotationlib.
