# Security, unsafe soundness, FFI and dependency hygiene

Load for parsers, unsafe code, FFI, network inputs, shared-memory structures, C/CUDA/GPU drivers, cryptographic boundaries and software supply chain reviews.

## Risk-first review

- Establish what untrusted callers/peers can control: length, allocation, nesting depth, integer values, UTF-8, path, address, identity, content, retry rate and event replay. Check limits *before* allocating, parsing or copying. Use checked arithmetic for sizes and offsets.
- Rust memory safety does not imply protocol, authentication, cryptographic, privacy, denial-of-service or business-logic security. Threat-model each trust boundary and separate authentication from authorization.
- Do not log secrets, private keys, full user payloads or unbounded high-cardinality input. Zeroization is relevant for secret material but does not retroactively guarantee it was never copied.

## Unsafe change checklist

1. Try a safe design or established safe abstraction first. Isolate necessary unsafe operations in the smallest private module and keep its fields private.
2. Write invariants for allocation provenance, alignment, initialization, aliasing/exclusivity, mutability, thread safety, lifetime, drop order and panic/unwind behavior.
3. Put a concrete `// SAFETY: ...` argument at each unsafe block. Document `# Safety` obligations on public unsafe functions/traits. A comment saying "safe because tested" is not a proof.
4. In `unsafe fn`, use explicit `unsafe { ... }` for unsafe operations; respect the edition's lint/policy. Review `unsafe impl Send/Sync` as a promise affecting all users of the type.
5. For FFI, verify `repr(C)`/ABI where required, ownership transfer, allocator matching, nullability, byte length, handle lifetime and callback/unwind rules. Rust 2024 requires `unsafe extern` blocks and unsafe attribute syntax such as `#[unsafe(no_mangle)]` where applicable.
6. Add tests at boundary values and run Miri on compatible tests; use fuzzing/sanitizers or hardware/target-specific testing where supported. Miri does not run every FFI/GPU scenario and cannot establish general soundness.

## Dependency policy

- Prefer maintained, minimally privileged dependencies; review maintenance, features, transitive risk, license and source. Favor explicit versions/feature selections under project policy.
- For projects with `Cargo.lock`, run `cargo audit` (RustSec advisories). Configure `cargo deny check` for advisory, license, source and duplicate/banned dependency policy where desired; install these tools separately. Record advisory exceptions with an owner, reason and review date.
- Pin release toolchains and audit dependencies in CI and periodically after merge. Reproducible builds lower drift, not malicious-dependency risk to zero.
- Treat generated/bindgen/vendor code as code requiring review; do not infer that a crate being popular makes its unsafe interfaces sound.

Sources: [Rustonomicon: safe/unsafe](https://doc.rust-lang.org/nomicon/safe-unsafe-meaning.html), [Rust 2024 unsafe extern](https://doc.rust-lang.org/edition-guide/rust-2024/unsafe-extern.html), [Rust 2024 unsafe attributes](https://doc.rust-lang.org/edition-guide/rust-2024/unsafe-attributes.html), [RustSec](https://rustsec.org/), [cargo-deny checks](https://embarkstudios.github.io/cargo-deny/checks/index.html).
