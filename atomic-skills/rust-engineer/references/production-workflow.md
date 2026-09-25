# Production workflow: architecture, Cargo, API and CI

Load for new crates, migrations, PR review, production releases, or choosing validation commands. Follow the repository's `rust-toolchain.toml` and supported targets before suggesting upgrades.

## 1. Make requirements executable

- Record success behavior and explicit negative cases; represent protocol/version/unit distinctions as newtypes or enums.
- Identify a public API's ownership model: borrowed inputs for synchronous reading, owned input when retaining or moving into a spawned task, iterator versus allocation trade-offs. Do not return references to temporary values.
- Keep domain rules separate from IO, clocks, transport, logging and database adapters. Put side effects behind narrow interfaces so unit tests can use in-memory fakes. Do not introduce trait/object layers solely to satisfy a preferred architecture.
- Reserve `Arc` for *shared ownership* and `Mutex`/`RwLock` for coordinated mutation; they solve different problems. Prefer message-passing for a single owner of hot mutable state when it simplifies correctness.
- Design library errors for callers: stable categories, preserved sources, no accidental secret leakage. For applications, add context at boundaries, not at every function.

## 2. Edition and compatibility

- Read `[package].edition`, `[package].rust-version`, resolver, feature definitions, crate types, `[workspace]` and pinned toolchain. A new crate can use Rust 2024 if deployment supports its compiler; do not silently migrate an older project.
- `cargo fix --edition` helps with migration but does **not** discharge semantic, FFI or unsafe audits. Compare warnings and test on supported targets. Document public breaking changes separately from an edition change.
- Test the claimed MSRV on that actual compiler; stable CI tests do not prove MSRV. A library may not commit `Cargo.lock` while binaries commonly should; follow the project's chosen policy and explain reproducibility impacts.
- For public libraries, review semver surface (visibility, trait bounds, auto traits, `#[non_exhaustive]`, error types), feature unification and default features. All-features checking is conditional on feature compatibility.

## 3. Small-step engineering

1. Reproduce the issue or write a small behavior/property test. Do not refactor unrelated code in the same patch.
2. Make ownership and state transitions explicit. Prefer exhaustive `match`; isolate parser validation before costly operations.
3. Add boundary tests: empty, max, malformed, duplicate, timeout, reconnect, cancellation, overflow, Unicode, cross-platform paths.
4. Keep rustdoc examples realistic; document `# Errors`, `# Panics`, and `# Safety` when applicable.
5. Review allocation, clone and collect calls only after correctness, with input sizes and a profiler when performance matters.

## 4. Suggested checks and when to run them

| Gate | Command or method | Notes |
| --- | --- | --- |
| Formatting | `cargo fmt --all -- --check` | Install rustfmt for pinned toolchain. |
| Compile / targets | `cargo check --workspace --all-targets` | Add supported target triples as needed. |
| Lints | `cargo clippy --workspace --all-targets -- -D warnings` | Pin CI toolchain to avoid surprise new lints; record reasoned exceptions. |
| Unit + integration + doctests | `cargo test --workspace` | Add `--locked` if lockfile policy requires. |
| Docs | `RUSTDOCFLAGS="-D warnings" cargo doc --workspace --no-deps` | Public library docs, warnings policy permitting. |
| Features | Test each supported feature set; `--all-features` if compatible | Mutually exclusive features require separate jobs. |
| MSRV | Check on `rust-version` compiler | May need dependency pinning/`--locked`. |
| Security | `cargo audit` or configured `cargo deny check` | Separately installed tools; scheduled reruns. |
| Unsafe or parser risk | Miri, fuzz/property tests, sanitizers where supported | Each tool catches different classes; none proves soundness. |
| Cross-OS/arch | CI matrix for supported Linux/macOS/Windows, CPU/targets | Architecture-, libc- and FFI-specific paths deserve coverage. |

Choose a small PR gate and a slower scheduled gate; report the actual commands and failures rather than a blanket "all checks passed." For performance regressions, compare representative workload and toolchain with repeatable measurements, not one timing.

Sources: [Cargo CI](https://doc.rust-lang.org/cargo/guide/continuous-integration.html), [Cargo manifest](https://doc.rust-lang.org/cargo/reference/manifest.html), [Rust 2024 Edition](https://doc.rust-lang.org/edition-guide/rust-2024/index.html), [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/checklist.html), [Cargo tests](https://doc.rust-lang.org/cargo/guide/tests.html), [Clippy in CI](https://doc.rust-lang.org/clippy/continuous_integration/index.html).
