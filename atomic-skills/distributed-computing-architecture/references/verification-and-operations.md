# Verification, operations, and review rubric

Load when turning a proposed distributed architecture into a falsifiable correctness argument, an operating plan, or launch acceptance criteria.

## Design evidence packet

Capture a compact artifact before making implementation claims:

~~~yaml
architecture:
  workload: ""
  failure_model: [crash-recovery, partition, delay, duplicate, reorder]
  trust_model: ""
  invariant:
    id: ""
    statement: ""
    scope: ""
  progress_assumption: ""
  consistency_by_operation: {}
  state_owners: {}
  replication_and_handoff: ""
  delivery_and_effect_contract: ""
  timeout_and_retry_budget: ""
  bounded_resources: {}
  observability: {}
  recovery: {}
  decision_adr: ""
  evidence:
    - source_or_revision: ""
      claim: ""
      status: fact_or_assumption_or_inference
  unresolved_risks: []
~~~

Use a table with one row per dependency: synchronous/async boundary, time budget, overload behavior, state ownership, durability/ACK point, retry owner, telemetry, and fault test. For any proposed protocol, sketch a transition table with current state, input, guard, durable effect, emitted messages, and next state. Pay attention to forbidden transitions and duplicate/reordered events.

## Required safety and liveness tests

| Injection or schedule | Candidate invariant / observable |
| --- | --- |
| Worker crashes before processing | No acknowledged effect without durable work; redelivery is possible |
| Worker commits effect then crashes before ACK | Same logical effect is not applied twice |
| Lost outbound event after local state commit | Outbox eventually republishes without duplicate business effect |
| Two workers concurrently take same job | Durable unique receipt or fencing ensures one acceptable effect |
| Old owner pauses past lease and resumes | Resource rejects stale ownership epoch |
| Minority / majority network partition | Documented read/write availability; no forbidden split-brain writes |
| Clock jumps forward/backward | No clock-dependent ownership or incorrect data deletion |
| Queue reaches cap | Admission rejects/sheds/degrades; memory stays bounded; recovery traffic proceeds |
| Retry storm during partial outage | Attempts and downstream load remain inside budget |
| Stream restores from checkpoint | State and source offset reconcile; sink effects match chosen guarantee |
| Peer leaves/joins during topology update | Missing/duplicated work is detected, rerouted, or explicitly expired |
| Duplicate feedback on one contribution ID | Applied once |
| Different feedback contributions to same activation | Both applied according to aggregation semantics |
| Activation expires before feedback arrives | Explicit late policy; no stale state resurrection |

For a complete system, include storage corruption, disk exhaustion, process and host crashes, packet loss, delay/jitter, asymmetric partitions, stale DNS/discovery, mixed-version rolling upgrades, checkpoint loss, capacity skew, and untrusted messages. Byzantine tests are justified only when included in the threat model.

## Testing ladder

1. **Pure model and property tests:** define the smallest state machine and generate event interleavings; assert invariants for duplicate/reorder/timeout/expiration and concurrent branches. Use deterministic virtual time and seeded randomized schedules.
2. **Model checking:** TLA+/PlusCal or a comparable formal tool for hard coordination protocols, especially election, fencing, leases, membership, and atomic effect claims. Model assumptions explicitly; a model proof does not certify a different implementation.
3. **Integration tests with real storage/broker:** crash at each transaction, persistence, publish, and ACK boundary; verify replay and uniqueness across restart.
4. **Jepsen-style histories:** record invocation and response, client-visible outcomes, fault timeline, then check the specified consistency and uniqueness properties.
5. **Performance and load:** reproduce expected key skew and fan-out, then burst, degrade a dependency, and recover while backlog exists. Report p50/p95/p99/p99.9, queue age, error rate, recovery duration, bytes/messages per useful effect, and resource/energy costs.
6. **Controlled chaos and disaster recovery:** smallest blast radius first; explicit steady state, abort/rollback, recovery check, accountable owner, and follow-up changes. Do not run production chaos merely because a test plan exists.

Separate evidence levels: "tested on a simulator", "passed on an integration cluster", "observed in a staged rollout", and "formally proved under specified assumptions" are not interchangeable.

## SLO and dashboard starter

Choose targets from actual user impact rather than copying numbers:

- End-to-end successful result latency by workload/priority, including tail latency and deadline miss rate.
- Safety counters: forbidden duplicate effects, conflicting ownership, stale-epoch write rejection, missing causal predecessor, invariant-check failures.
- Transport: send/ACK latency, retries per original operation, expired messages, redelivery count, malformed or unauthorized messages.
- Backpressure: oldest pending age, bounded queue utilization in bytes and items, load-shedding count, worker concurrency, hot-shard skew.
- Replication: commit/index lag, anti-entropy backlog, checkpoint age, last successful restore, replay duration, consistency probe failures.
- Topology: suspect vs confirmed unavailable, membership propagation delay, join/leave rate, reassignment churn and orphan work.
- Graph/training: pending-activation bytes, feedback lag, unique vs duplicate contribution rates, expired activations, per-node update throughput, stability/convergence measures when a valid evaluation exists.

Instrument both data and control planes. Include low-cardinality metric labels; use exemplars/traces for individual IDs. Trace correlation is useful but not an authoritative transaction ledger.

## Runbook and launch gates

Define who can stop ingestion, change placement, drain nodes, replay queues, repair corrupted state, rotate credentials, and restore snapshots. Document what data is lost/duplicated at each recovery mode; keep replay and live traffic within a shared resource budget. Version and test schema migration, persistent snapshot compatibility, node identity rotation, rollback, and partial deployment.

Minimum release checks:
- all named safety invariants have a test and source revision;
- timeout/retry, ACK, idempotency, and expiry contracts are explicit;
- bounded queues and admission work during dependency failure;
- recovery has been observed from a real failure injection;
- dashboards and alerts distinguish transport success from committed business effect;
- rollback is exercised and RPO/RTO are measured;
- residual risks and missing evidence are listed rather than labeled "production ready".

For review reports, prioritize reproducible counterexamples and specific remediation over generic ratings. A finding should include the violated invariant, exact protocol/code evidence, minimal failure schedule, severity rationale, and a test that would prevent regression.

Primary references: [sources](sources.md), particularly Jepsen, Google SRE, and OpenTelemetry.
