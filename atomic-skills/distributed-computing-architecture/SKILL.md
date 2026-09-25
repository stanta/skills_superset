---
name: distributed-computing-architecture
description: Designs and reviews reliable distributed computation, from microservices and stream processing to peer-to-peer, actor, and asynchronous graph networks. Use for consistency and consensus trade-offs, message delivery, partitioning, scheduling, backpressure, failure recovery, gossip membership, distributed learning, and correctness testing.
metadata:
  category: software-architecture
  version: "1.0.0"
  related-skills: architecture-designer, microservices-architect, chaos-engineer, rlm-roec-context-reasoning
---

# Distributed Computing Architecture

Design distributed computations by making correctness, progress, resource limits, and failure behavior explicit **before** choosing protocols or infrastructure. This skill covers both coordinated systems and decentralized, asynchronous computation; microservices and global consensus are not defaults.

## When to use

- Design or review a distributed system, distributed scheduler, worker pool, dataflow, stream processor, actor network, P2P overlay, or compute cluster.
- Select partitioning, replication, leader election, consensus, CRDT, gossip, checkpointing, or exactly-once *effect* boundaries.
- Diagnose lost, duplicated, late, reordered, or conflicting messages; overload; inconsistent recovery; split-brain; stale leaders; or cascading failures.
- Specify an asynchronous computation graph whose nodes maintain local state and exchange forward signals and delayed feedback.
- Produce an architecture decision record (ADR), protocol contract, failure matrix, capacity model, correctness argument, or test plan.

For distributed database engines and storage internals use [distributed-dbms-architect](../distributed-dbms-architect/SKILL.md). For general component architecture use [architecture-designer](../architecture-designer/SKILL.md); for service boundaries use [microservices-architect](../microservices-architect/SKILL.md); for executable failure injection use [chaos-engineer](../chaos-engineer/SKILL.md). For large, conflicting repository evidence, apply [rlm-roec-context-reasoning](../rlm-roec-context-reasoning/SKILL.md): retrieve relevant slices, record source/revision, test counterexamples, and stop when the decision is supported.

## Non-negotiable design principles

1. **State the invariant and its scope.** Identify what must *never* happen (safety), what eventually must happen under stated conditions (liveness), and which failures make progress impossible. Name the specific key, shard, transaction, model state, or node rather than assuming global consistency.
2. **Partial failure is normal.** Remote calls can be slow, dropped, duplicated, or completed after the caller times out. A timeout means the outcome may be unknown; it is not proof of cancellation or rollback.
3. **Choose the weakest consistency sufficient for the invariant.** Use a proven consensus-backed component only where single authority or strong ordering is required. Independent partitions, immutable events, associative/commutative merges, and local learning should not pay a global coordination tax.
4. **Specify delivery and effect separately.** At-least-once delivery plus durable idempotent effects is often practical. Broker-level exactly-once claims do not automatically cover an external API, filesystem, side effect, or downstream state.
5. **Bound everything that can accumulate.** Queues, retries, dedup records, pending activations, fan-out, gossip, payloads, checkpoints, concurrent work, and recovery work need admission limits, expiry, and measurable budgets.
6. **Make recovery a protocol, not a restart command.** Persist enough state to replay safely; define ownership handoff, epochs/fencing, resynchronization, and what happens to late messages from the old owner.
7. **Prove by falsification.** Use a reference state machine, explicit fault assumptions, deterministic simulation, property tests, and live-cluster fault injection. A healthy-cluster benchmark is not correctness evidence.

## Design workflow

### 1. Frame requirements and the failure model

Record workload type (request/response, batch, streaming, interactive graph, training), node count and churn, heterogeneity, state size, update rate, key skew, network topology, trust boundaries, and deployment geography. Define p50/p99/p99.9 latency, throughput, cost/energy, availability target, acceptable data loss, RPO/RTO, and behavior under overload. Classify failures: crash-stop, crash-recovery, partitions, delay, reorder, duplicates, clock drift, disk loss, and Byzantine behavior **only if** the threat model requires it.

Produce a per-operation invariants table:

| Operation/state | Safety invariant | Progress condition | Consistency scope | Recovery evidence |
| --- | --- | --- | --- | --- |
| Example: debit | No double debit for one command | Quorum/storage available | One account or ledger | Durable idempotency record + transaction |
| Example: graph feedback | One application per contribution identity | Activation still retained; route available | One activation and contributor | Pending activation + applied-contribution ledger |

If requirements are missing, label assumptions and offer alternatives rather than inventing production numbers.

### 2. Place computation and state deliberately

Separate **data plane** (work and messages) from **control plane** (membership, discovery, placement, policy, schema, upgrades). Choose ownership by key/actor/partition when local state and affinity matter; use stateless worker pools for independent work; use stream DAGs and watermarks for event-time processing. Consider data locality, hotspots, consistent hashing with explicit migration semantics, replication, and recovery traffic.

Make the choice explicit: centralized coordinator, per-shard leader, quorum, actor/mailbox, queue/consumer group, gossip overlay, or hybrid. A coordinator can be the simplest correct design; decentralization is a requirement to justify, not a virtue to assume. Minimize synchronous fan-out and cross-partition transactions on latency-critical paths.

### 3. Allocate consistency only where needed

For every state transition, decide whether it requires linearizability, a serializable transaction, read-your-writes/session guarantees, causal order, eventual convergence, or no shared consistency. Distinguish ordering within a key or stream partition from ordering across the entire deployment. Use version checks/CAS for optimistic ownership; implement fencing for stale workers. For concurrent offline edits, consider CRDTs only if the merge algebra and deletion/tombstone lifecycle match business semantics.

Record what happens during a network partition: which side may read, accept writes, queue commands, or explicitly reject operations. CAP concerns the conflict between strong consistency and availability *during a partition*; it is not a universal CP/AP product label. See [consistency-and-coordination](references/consistency-and-coordination.md).

### 4. Define the wire protocol and effect boundary

Write an explicit versioned message envelope, sender/recipient, auth, causation, correlation/trace, stable logical operation ID, unique delivery ID, attempt number, epoch, ordering key, payload schema, deadline/TTL, and size limits. If one activation fans out, distinguish **a duplicate of one contribution** from **two legitimate contributions to the same activation**.

Specify acknowledgment point (received, durably stored, effect committed), retryable vs permanent errors, dedup storage and expiry, poison message handling, schema evolution, and replay policy. Prefer atomic inbox/effect commit for a consumer; use transactional outbox/CDC when publishing events with a database change. Do not describe exactly-once end-to-end unless every source, state transition, and sink satisfies the guarantee. See [messaging-and-resilience](references/messaging-and-resilience.md).

### 5. Design overload and failure containment

For every remote boundary define: end-to-end deadline, connect/request timeout, bounded attempts at **one** designated retry layer, exponential backoff with jitter, per-caller retry budget, circuit breaking only where helpful, admission control, bounded queues, load shedding, and graceful degradation. Distinguish retries for idempotent reads from irreversible writes. A cancellation signal is advisory unless the receiving protocol guarantees otherwise.

Isolate tenants, priority classes, and expensive tasks with bulkheads; ensure control-plane and recovery traffic cannot be starved by user workload. Explicitly bound recovery storms, checkpoint fan-out, and consumer rebalances. See [messaging-and-resilience](references/messaging-and-resilience.md).

### 6. Model capacity, placement, and time

Identify CPU, GPU, memory, disk, network, and tail-latency bottlenecks. Model arrival rate and service capacity per shard, burst size, backlog drain time, work stealing, locality, batching, speculative duplicate work for stragglers **only when effects are safe**, and checkpoint cadence. Little's law applies to stable queues; do not substitute average utilization for p99 under bursty arrivals. Budget end-to-end latency across serial stages and concurrent fan-out. State how clock uncertainty affects leases, timestamps, TTL, and event-time watermarks.

### 7. Security, observability, and operations

Authenticate nodes and messages; authorize operations at their destination; rotate identities and keys; protect membership against Sybil/poisoning where peers are untrusted; encrypt transport; enforce payload and resource quotas. Treat trace headers and gossip data from external peers as untrusted inputs. Propagate trace context across async boundaries without putting secrets in baggage.

Expose SLOs, per-stage queue age and depth, inflight work, retries, dedup hit rate, redeliveries, consistency lag, checkpoint age, membership churn, orphan/expired work, and error budgets. Document deployment, mixed-version protocol compatibility, resharding, rollback, draining, disaster recovery, and manual intervention. See [verification-and-operations](references/verification-and-operations.md).

### 8. Validate invariants before scale claims

For each safety invariant, create a model/property test that can fail under reordered, duplicated, lost, delayed, and concurrent messages. Inject network partitions, crash-after-effect-before-ack, stale leader after pause, full queues, lost checkpoints, late feedback, malicious or malformed messages, clock shifts, and join/leave storms. Separate **safety** (never violates invariant) from **liveness** (eventually progresses given assumptions). Use bounded model checking/TLA+ or a reference-state-machine model when interleavings are material; use Jepsen-style histories for storage/coordination claims; run controlled chaos experiments with blast-radius and rollback limits.

## Pattern selection: start from the invariant

| Problem | Candidate pattern | Caveat / required proof |
| --- | --- | --- |
| Critical single-owner state | Proven Raft/Paxos-backed service, per-shard leader | Quorum loss blocks progress; stale writers need fencing |
| Independent tasks | Partitioned queue + competing workers | Duplicates, lease expiry, poison messages, checkpointing |
| Replayable streaming computations | Log + state snapshots/checkpoints + replay | External sinks must be idempotent or transactional |
| Mergeable offline state | CRDT / anti-entropy gossip | Define merge algebra, deletes, bounded metadata, convergence assumptions |
| Dynamic peer membership | SWIM-like suspect/probe + gossip | A suspicion is not proof of failure; avoid instant reallocation on suspicion |
| Local actor or neuron state | Actor/mailbox + keyed events + local journal | Explicit per-activation lifecycle and feedback identity |
| Cross-service multi-step business action | Saga + compensations | Compensation is a new action, not general ACID rollback |
| Critical read under replica lag | Leader/quorum read or session token | Measure latency and specify partition behavior |

Use this table to generate options, not to select technology by keyword. For graph and neuromorphic work read [asynchronous-graph-computation](references/asynchronous-graph-computation.md).

## Required output

Provide, proportionate to task size:

1. **Architecture decision packet:** assumptions; workload and trust/failure model; NFRs; 2–3 feasible options; decision and rejected alternatives; measurable costs and trade-offs; ADRs for high-impact choices.
2. **Topology/data-flow view:** node roles, partition keys, state ownership, replication, control/data plane, hot path, recovery path, and trust boundaries.
3. **Protocol and state machines:** envelope, dedup/effect identity, acknowledgment/durability points, local transition table, versioning, and expiration.
4. **Failure/consistency matrix:** failure × component × safety impact × degraded behavior × recovery × test.
5. **Verification and rollout plan:** invariants as executable checks, load tests with skew, partitions and duplicates, telemetry, safe canary/rollback, acceptance thresholds.

If the user asks only for a narrow decision or review, deliver the relevant subset while preserving all correctness-relevant qualifications.

## Fast architecture review (red flags)

- Claims of guaranteed message delivery or exactly-once effects without a durable effect boundary and sink contract.
- Lost acknowledgment interpreted as failed operation; retry can repeat an irreversible effect.
- Leader lease without fencing at the resource; clock timestamps used as a causality proof.
- Every read or local computation blocked on global membership or consensus without a matching invariant.
- Gossip treated as reliable broadcast; membership suspicion treated as certified death.
- Unbounded queues, retries, in-flight activations, feedback loops, or dedup records.
- Duplicate suppression keyed only on parent event when independent fan-out branches legitimately contribute.
- Load tests without skew, recovery traffic, partitions, lag, or p99; chaos tests without a stated invariant or rollback.
- A new distributed service added when a modular monolith, single owner, or existing queue would suffice.

## Sources and evidence

Use [sources](references/sources.md) for primary research and official guidance. Check sources again when evaluating current product-specific capabilities, broker guarantees, implementation versions, or security defaults. Keep source facts, scenario assumptions, and architectural inference separate.
