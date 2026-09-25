# Performance, resource budgets and observability

Load only when a measurable latency, throughput, memory, startup, binary size or CPU goal exists. Correctness and testability precede micro-optimisation.

## Measure → explain → change → remeasure

1. Specify the workload (message sizes, burst patterns, fan-out, number of peers, target OS/CPU, compiler flags), baseline and percentile/SLO. Measure release builds under representative load; control warmup, I/O and network variance.
2. Profile before editing: CPU flamegraph, allocation counts, heap snapshots, async task/blocking traces, lock contention and serialization copies. Keep benchmark harness and data versioned.
3. Optimize the dominant cause. Typical candidates: redundant allocations/`clone`/`collect`, repeated UTF-8 or JSON conversions, oversized `Arc<Mutex<_>>` critical sections, lock convoying, per-message task spawning, unnecessary network round-trips, unbounded queues and cache locality.
4. Preserve semantics: use ownership-aware sharing (`Arc`, bytes-like immutable buffers) only when measured; do not casually replace safe indexing with unchecked access, add `unsafe`, or preallocate unbounded memory for speed.
5. Compare new and baseline distributions and inspect p95/p99 as well as median; account for memory, CPU, fairness and tail latency. Revert optimisations that do not reproduce a meaningful benefit.

## Distributed node instrumentation

- Use structured logs and tracing spans carrying request/event correlation and peer context, with redaction and sampling. Track queue length, dropped/retried work, accepted/committed events, feedback latency and cancellation outcomes.
- Bound metrics cardinality; never attach one series per `EventID` or unbounded peer ID. Prefer metrics for aggregate rates and sampled traces/logs for event-by-event diagnosis.
- Watch the *whole pipeline*: per-peer rate limits, incoming frame limits, decode, dedupe lookup, local computation, outgoing bounded queue, reconnect policy and feedback expiry.
- Compare performance with protocol correctness: a faster path that violates idempotency or drops feedback is a regression.

## Useful tools (availability and compatibility vary)

- `cargo bench` for project benchmarks; Criterion for statistical microbenchmarks (configured as a bench target).
- `cargo flamegraph`/system profiler for CPU hotspots; allocator/profiling tooling for actual allocations; Tokio tracing/console where enabled.
- `cargo build --release` is not sufficient evidence of performance. No estimated speedup without a before/after benchmark and stated environment.

Sources: [Cargo profiles](https://doc.rust-lang.org/cargo/reference/profiles.html), [Cargo bench](https://doc.rust-lang.org/cargo/commands/cargo-bench.html), [Tokio channels and backpressure](https://tokio.rs/tokio/tutorial/channels), [Rust Performance Book](https://nnethercote.github.io/perf-book/).
