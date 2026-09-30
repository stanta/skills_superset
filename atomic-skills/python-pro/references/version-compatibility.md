# Python 3.10-3.14 version compatibility and migration matrix

Last reviewed: 2026-09-30.

Use this reference whenever code, tooling, or recommendations depend on a particular Python minor version. **The minimum supported Python version determines which syntax and stdlib APIs may appear unguarded in source code.**

## Support lifecycle

| Version | First release | Status on 2026-09-30 | End of life | Skill policy |
| --- | --- | --- | --- | --- |
| 3.10 | 2021-10-04 | security-only | 2026-10 | Legacy compatibility only; plan migration now |
| 3.11 | 2022-10-24 | security-only | 2027-10 | Maintain when required; not a new-project default |
| 3.12 | 2023-10-02 | security-only | 2028-10 | Compatibility floor when ecosystem/deployment requires it |
| 3.13 | 2024-10-07 | bugfix | 2029-10 | Conservative modern baseline |
| 3.14 | 2025-10-07 | bugfix | 2030-10 | Latest stable; greenfield default when dependencies support it |

Python 3.15 is prerelease on 2026-09-30. Do not silently use 3.15 features in skills scoped to 3.10-3.14.

## Python 3.10

**Applies: 3.10+**

Notable capabilities:
- Structural pattern matching: `match` / `case`.
- Union syntax: `X | Y` and `X | None`.
- `ParamSpec` / `Concatenate`, `TypeAlias`, and `TypeGuard`.
- `zip(..., strict=True)`.
- Dataclass `slots=`, `kw_only=`, and `KW_ONLY`.
- Precise line numbers for debugging/profiling.

Best practices:
- This is the lowest covered version, so built-in generics and `X | Y` are safe across the entire 3.10-3.14 range.
- Do not use `Self`, `TaskGroup`, `tomllib`, PEP 695 syntax, or 3.14 annotation semantics without compatibility handling.
- Because 3.10 reaches EOL in October 2026, avoid adding new 3.10 compatibility unless consumers or deployment infrastructure require it.

## Python 3.11

**Applies: 3.11+**

Notable capabilities:
- `asyncio.TaskGroup` structured concurrency.
- `ExceptionGroup` and `except*`.
- Exception notes.
- `tomllib`.
- Fine-grained traceback locations.
- Typing: `Self`, `Required`, `NotRequired`, variadic generics, `LiteralString`, `dataclass_transform`.
- Major CPython execution-speed improvements relative to 3.10.

Best practices:
- Prefer `TaskGroup` over manually created sibling tasks when child lifetime/failure should be scoped together.
- Use grouped exceptions only when multiple independent failures are meaningful to the caller.
- If supporting 3.10, use `typing_extensions` for backported typing constructs where appropriate.

## Python 3.12

**Applies: 3.12+**

Notable capabilities:
- PEP 695 type-parameter syntax and the `type` statement.
- PEP 701 full-grammar f-string expressions.
- Per-interpreter GIL support at the C API level.
- Low-impact monitoring API.
- `distutils` removed from the standard library.

Best practices:
- Use PEP 695 syntax only when `requires-python >= 3.12`; it is a syntax error on 3.11 and below.
- Do not use `distutils`; use standards-based packaging and maintained build backends.
- Libraries supporting 3.10/3.11 should retain older generic syntax.

## Python 3.13

**Applies: 3.13+ unless marked experimental**

Notable capabilities:
- Improved interactive interpreter and colored tracebacks.
- **Experimental** free-threaded CPython.
- **Experimental** JIT compiler.
- Defined mutation semantics for `locals()`.
- Type parameters can have defaults.
- Removal of multiple legacy stdlib modules deprecated under PEP 594.

Best practices:
- Do not claim normal Python 3.13 is "GIL-free"; free-threading is an explicit build/runtime mode.
- Verify wheel/C-extension support and benchmark the real workload before free-threaded adoption.
- Do not enable the experimental JIT merely because it exists.
- Audit legacy stdlib imports during migration.

## Python 3.14

**Applies: 3.14+**

Notable capabilities:
- Deferred evaluation of annotations (PEP 649/749).
- `annotationlib` for runtime annotation introspection.
- Template string literals `t"..."`.
- `concurrent.interpreters`.
- Free-threaded Python is officially supported but remains optional.
- `compression.zstd` and the `compression` namespace.
- Asyncio task/call-graph introspection.
- Better free-threaded support in asyncio.
- Asyncio event-loop policy system deprecated for removal in 3.16.

Best practices:
- Frameworks/libraries that read annotations must test 3.14 explicitly.
- Do not rely on annotation expressions executing eagerly at definition time.
- Prefer documented `annotationlib` APIs for introspection.
- `from __future__ import annotations` still works, but do not add it automatically to 3.14-only code.
- Free-threading does not make shared mutable state safe; audit locks, caches, registries, native extensions, DB/client libraries, and observability integrations.
- Prefer `asyncio.run(..., loop_factory=...)` or `asyncio.Runner` over event-loop policy customization.

## Selecting a baseline

For a new project in late 2026:
1. Prefer **3.14** when the dependency and deployment matrix supports it.
2. Prefer **3.13** when a more conservative compatibility baseline is needed.
3. Use **3.12** only when platform/dependency constraints require it.
4. Avoid starting new long-lived projects on **3.10 or 3.11**.

For libraries:
- Set the minimum from actual consumers.
- Test the minimum and maximum supported minors in CI.
- Keep examples valid on the declared minimum.
- Raise the minimum deliberately and document which compatibility code is removed.

## Cross-version implementation rules

- Source syntax must parse on the minimum supported Python version.
- Keep `requires-python`, CI, type-checker target, linter/formatter target, Docker/runtime images, and docs aligned.
- Prefer feature detection/version checks only where APIs truly differ at runtime; do not scatter checks instead of defining a support policy.
- Prefer `typing_extensions` for typing backports.
- Avoid private CPython APIs unless the project intentionally targets CPython internals.
- Benchmark concurrency/runtime changes under the exact interpreter build used in production.

## Upgrade checklists

### 3.10 → 3.11
- Add 3.11 to CI before changing production.
- Review task ownership/cancellation for `TaskGroup`.
- Review exception aggregation.
- Keep 3.10-compatible syntax until the minimum is raised.

### 3.11 → 3.12
- Audit packaging for `distutils`.
- Decide whether PEP 695 is worth dropping 3.11.
- Test code-generation/parsing tools against PEP 701 f-strings.
- Validate native extensions if using subinterpreters/per-interpreter-GIL APIs.

### 3.12 → 3.13
- Audit removed PEP 594 modules and `locals()`/debugger assumptions.
- Keep free-threaded/JIT trials isolated until dependencies and benchmarks are ready.
- Test C-extension and wheel availability for free-threaded trials.

### 3.13 → 3.14
- Test frameworks/libraries that introspect annotations.
- Replace direct/private annotation-dict introspection with documented APIs where necessary.
- Review asyncio loop-policy customization and plan migration to `loop_factory`.
- If evaluating free-threading, retest the complete dependency stack.
- Adopt Zstandard, template strings, or subinterpreters only when they solve a concrete problem.

## Primary sources for future refreshes

Use primary CPython sources first:
- Python Developer's Guide: version lifecycle/status.
- "What's New" for each Python minor.
- Standard-library docs for `typing`, `asyncio`, `annotationlib`, and `concurrent.interpreters`.
- Accepted PEPs for rationale, but current documentation for final runtime semantics.
