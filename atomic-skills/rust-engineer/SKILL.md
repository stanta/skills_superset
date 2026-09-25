---
name: rust-engineer
description: >
  This skill should be used when designing, implementing, reviewing, debugging, testing, securing,
  or profiling Rust and Cargo projects: ownership and borrowing, lifetimes, traits and API design,
  Rust 2021/2024 editions, async Tokio, WebSocket and distributed nodes, FFI and unsafe soundness,
  dependency supply chain, performance, and production CI.
license: MIT
metadata:
  author: https://github.com/Jeffallan
  version: "2.0.0"
  updated: "2026-09-25"
  domain: language
  triggers: Rust, Cargo, rustc, rustfmt, Clippy, Rust 2024, ownership, borrowing, Tokio, async, WebSocket, FFI, unsafe, profiling
  role: specialist
  scope: implementation-review
  output-format: code-and-verification
  related-skills: test-master, systematic-debugging, security-reviewer
---

# Rust Engineer — production-grade workflow

Apply this skill to Rust code and design work. Prefer an existing project's documented constraints over generic defaults. **Never claim a command passed without seeing its output.** The detailed references are opt-in; load only those relevant to the request.

## Execution loop

1. **Inspect before changing.** Read `Cargo.toml`, workspace layout, `rust-toolchain.toml`, `rust-version`, edition, target triples, lockfile policy, feature matrix, CI, and nearby tests. Identify the actual runtime (Tokio, async-std, synchronous, no_std) rather than introducing one.
2. **Write the contract.** State behavior and failure modes; data ownership; trait/API boundaries; thread-safety and `Send`/`Sync`; cancellation and shutdown; memory/CPU/queue limits; security-sensitive inputs; and measurable performance constraints. Distinguish requirements from assumptions.
3. **Implement the smallest coherent change.** Start with a regression test for a bug or a failing behavior test for a new contract where practical. Make invalid states unrepresentable with enums/newtypes and narrow public interfaces. Prefer safe Rust and the standard library; add dependencies only with a reason.
4. **Validate proportionally.** Run targeted tests first, then the applicable quality gates below. Test feature and platform combinations that the product actually supports; do not assume `--all-features` is valid when features are mutually exclusive. For networked/unsafe code, include failure, cancellation, and hostile-input tests.
5. **Review and report evidence.** Inspect the final diff for panic paths, clones/allocations, lock scope, cancellation, exposed secrets, `unsafe` proof obligations, API compatibility, and missing tests. Report commands run, pass/fail, unrun checks, and residual risks.

## High-value Rust decisions

- Borrow `&str`/`&[T]` when the callee only reads for the duration of the call; own `String`/`Vec<T>` when data must outlive the caller or cross spawned-task boundaries. Avoid clones by design, but do not contort lifetimes to avoid a cheap, justified clone.
- Prefer simple concrete types; introduce generics/traits when they represent real variation. Use newtypes for IDs, units, validated state, and protocol versions. Expose library errors with useful variants (`thiserror` is optional); attach context at application boundaries (`anyhow` is optional). Use `?` for propagation.
- Handle expected failure with `Result`/`Option`. Treat `unwrap` and `expect` alike as potential panics: reserve either for tests or invariants that are genuinely proven and explained. A custom message alone does not make a production panic safe.
- Treat text as UTF-8: byte-index a `str` only at verified character boundaries. Avoid `s[..N]` for a character-count preview; use `s.chars().take(N).collect::<String>()` if character count is intended.
- Use the repository's edition. Rust 2024 is available from Rust 1.85, but migration is a deliberate compatibility change; `edition` and minimum supported `rust-version` are separate decisions. For 2024, review `unsafe_op_in_unsafe_fn`, unsafe extern blocks, and unsafe attributes.
- Keep `unsafe` inside a small, private boundary with documented invariants. A safe wrapper must remain sound for *all* safe callers; use FFI only with explicit ownership, ABI, alignment, lifetime, unwind, and error contracts.
- For Tokio, bound tasks and queues, explicitly handle cancellation/shutdown, keep blocking work off async executor threads, and do not hold a blocking mutex guard across `.await`. Avoid assuming that timeouts stop `spawn_blocking` work.

## Reference routing

| Need | Read |
| --- | --- |
| Ownership, lifetimes, smart pointers, Pin | `references/ownership.md` |
| Traits, generics and type-system trade-offs | `references/traits.md` |
| Results, error taxonomies and propagation | `references/error-handling.md` |
| Existing Tokio/async examples | `references/async.md` |
| Existing unit/integration/benchmark examples | `references/testing.md` |
| Edition, workspace, API boundaries, test pyramid, Cargo and CI gates | `references/production-workflow.md` |
| Tokio cancellation/backpressure, WebSocket and distributed event processing; DANMA profile | `references/async-distributed.md` |
| Unsafe, FFI, input limits, dependencies, fuzzing and audit | `references/security-unsafe-ffi.md` |
| Profiling, allocations, latency budgets and observability | `references/performance-observability.md` |

## Baseline verification (adapt to this repository)

```bash
cargo fmt --all -- --check
cargo check --workspace --all-targets
cargo clippy --workspace --all-targets -- -D warnings
cargo test --workspace
cargo doc --workspace --no-deps
```

Add `--locked` where a checked-in application lockfile is required. Add `--all-features` **only** when combinations are supported. Optional, separately installed tools: `cargo audit` or `cargo deny check` for dependency policy; `cargo +nightly miri test` for compatible unsafe code; `cargo fuzz` for parsers; `cargo bench`/Criterion for measured hot paths. `cargo clippy` is not a test or a soundness proof.

## Completion format

Return the changed paths and interface decisions; precise checks actually run (and results); how failures, cancellation, and security boundaries are handled; measured performance only if benchmarked; and known gaps. If the environment lacks Rust, network access, a target, or credentials, state what was not verified rather than inventing success.

Authoritative starting points: [Rust Edition Guide](https://doc.rust-lang.org/edition-guide/rust-2024/index.html), [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/), [Cargo CI guide](https://doc.rust-lang.org/cargo/guide/continuous-integration.html), [Tokio graceful shutdown](https://tokio.rs/tokio/topics/shutdown), and [Rustonomicon](https://doc.rust-lang.org/nomicon/).
