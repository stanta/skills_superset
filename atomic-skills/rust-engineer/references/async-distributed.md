# Async, Tokio, WebSocket and distributed nodes

Load for Tokio services, WebSocket clients/servers, protocol peers, cancellation, retries, high-concurrency servers, or DANMA-like decentralised systems. Read the existing `async.md` for basic syntax; this document adds operational invariants.

## Concurrency budget and ownership

- Map every task's owner, lifetime and shutdown path. Use a bounded `mpsc` channel for work queues and `Semaphore` for concurrent in-flight operations; set per-peer and process-wide budgets for sockets, message bytes, tasks, memory and retries.
- Separate socket reading, validated event processing and socket writing when backpressure requires it. One bounded writer queue per peer avoids unbounded concurrent sends. Define behavior when full: await capacity, reject, coalesce, or shed low-priority traffic; never drop learning or financial events silently.
- Distinguish cheap asynchronous waiting from CPU-heavy work. `spawn_blocking` isolates blocking calls but is not necessarily abortable after starting; use separate worker pools/processes for genuinely hard timeouts. Avoid blocking std locks across `.await`; minimize all lock scopes.
- `tokio::select!` drops losing futures. Audit cancellation safety before placing reads/writes, transactions or state updates in a `select!` branch; a dropped partial operation may lose bytes or work. Separate "accepted" from "durably committed".
- Propagate errors from `JoinHandle`/`JoinSet`; a spawned future panic or cancellation does not equal business success. Use `CancellationToken` or an equivalent signal, close input channels, drain/abort with explicit policy, then join with a bounded grace period.

## Transport and event protocol

1. Define versioned frames with identity, sender/authentication, payload length limit, `EventID`, optional branch/correlation IDs, expiry/TTL and acknowledgement semantics. Validate before allocation and before side effects.
2. Treat delivery as potentially delayed, duplicated, reordered or lost, including reconnect/retry cases. Make handlers idempotent within a stated deduplication retention window. Avoid a universal "exactly once" claim across crashes and partitions.
3. Acknowledge only after the chosen durability boundary; otherwise document possible loss. Persist transactional state with dedupe keys if "processed" must survive restart.
4. Bound timeouts, retries, exponential backoff and jitter, retry budgets and peer reputation/rate limits. Use monotonic elapsed time for local timeouts and explicit clocks for cross-node expiry.
5. Trace events with bounded-cardinality metrics. Keep EventID in sampled traces/logs where appropriate, not as a metrics label.

## DANMA optional profile: local asynchronous learning

Use only when the project is actually implementing DANMA or a similar neuron/feedback protocol; do not impose this topology on ordinary services.

- Keep each neuron/node responsible only for its own state and computations. Do not require network-wide synchronous consistency or replication of every neuron's work.
- Store a bounded activation record keyed by `EventID` to match later feedback to the *specific forward activation* and its incoming sources/weights. Retain it for the feedback window and evict safely.
- Propagate a finite feedback TTL and reject loops/expired or unauthorized feedback. Specify hop-limit versus time-expiry semantics; decrement the hop budget before forwarding.
- **Deduplicate delivery without erasing legitimate fan-out.** Track the identity of an individual feedback contribution (for example `(EventID, branch_or_child_id, feedback_id)` plus authenticated source). A replay of the same contribution must not update weights twice; distinct branch contributions may each count per a defined aggregation rule. A single global "seen EventID" flag is incorrect for branched activations.
- When local learning must be crash-safe, atomically record the dedupe marker and the applied weight/state update (or use a replayable event log). Otherwise document at-least-once processing risk. Expire both records using protocol retention and resource budgets, not a bare unbounded hash set.
- GOSSIP/discovery can find reachable neurons; distinguish address discovery and message delivery from local gradient/feedback computation. Avoid assuming gossip yields a global consistent view.

## Tests to require

Simulate peer disconnect/reconnect, backpressure, slow consumers, cancellation between reception and commit, duplicate delivery, reordering, independently valid feedback branches, malicious oversized frames, TTL exhaustion, and restart/replay. For race-sensitive shared state use deterministic scheduling/model tests when available; stress tests alone cannot prove absence of races.

Sources: [Tokio bounded channels](https://tokio.rs/tokio/tutorial/channels), [Tokio graceful shutdown](https://tokio.rs/tokio/topics/shutdown), [Tokio `select!`](https://docs.rs/tokio/latest/tokio/macro.select.html), [Tokio `spawn_blocking`](https://docs.rs/tokio/latest/tokio/task/fn.spawn_blocking.html).
