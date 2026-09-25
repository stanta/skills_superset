# Consistency and coordination playbook

Load this reference when the architecture has replicated mutable state, cross-node ordering, leases, distributed transactions, or offline concurrent updates.

## 1. Describe guarantees per operation

| Guarantee | What it means | Typical use | Failure/latency cost |
| --- | --- | --- | --- |
| Linearizable operation | Appears to take effect atomically between invocation and response, respecting real-time order | Critical leader/config state, uniquely allocated resource | Needs a sound coordination/read protocol and may lose availability during a partition |
| Serializability | Concurrent transactions have an equivalent serial execution | Cross-row/business invariants | Does not *by itself* imply real-time ordering; distinguish strict serializability |
| Causal consistency | A process observes causally related operations in causal order | Collaboration, conversation, dependent graph updates | Track dependencies and define visibility across replicas |
| Read-your-writes / monotonic session | A client does not regress relative to its own prior observations | User-visible updates after a write | Session routing/tokens or sufficiently fresh replicas |
| Eventual convergence | Replicas converge after updates cease and communication/reconciliation succeeds | Cache, presence, mergeable metadata | Conflict semantics matter; no promised convergence under permanent partitions |
| Per-key/partition order | Only messages for one key/partition are ordered | Actor mailbox, inventory item, per-neuron state | Migration, retries and multiple producers can break assumed ordering |
| No shared-state guarantee | Operations remain local, later messages are best-effort | Independent compute, opportunistic discovery | Explicit output/result completeness conditions required |

Never say "the system is consistent" without naming the operation, scope, and guarantee. Read staleness and write conflict tolerance separately.

## 2. Minimize the coordination surface

Classify state as (a) immutable, (b) single-writer/shard-owner, (c) commutatively mergeable, or (d) requiring mutual exclusion/consensus. Default to local ownership for (b), combine independent updates for (c), and pay for (d) only around the invariant. Use versioned snapshots and explicit ownership epochs for handoff; never infer exclusive write authority solely from a locally cached membership list.

A Raft/Paxos-style replicated state machine is a practical building block for durable ordered critical state when a quorum can be contacted. Prefer a mature implementation rather than writing consensus ad hoc. Include leader election, log replication, storage sync, membership changes, replay after crash, client request deduplication, and linearizable read implementation in the decision. A leader that responds from a stale local log does not automatically give a linearizable read.

Quorum math is not enough: R + W > N and W > N/2 can still fail to deliver a claimed guarantee if membership changes, sloppy quorums, version reconciliation, clock assumptions, or implementation paths violate the proof. Define the actual quorum protocol and test it.

## 3. Leases, epochs, and stale actors

A lease is a claim of temporary authority subject to failure detector and clock assumptions. A paused worker may resume after its lease has expired, even if the worker never observed that expiry. Use a monotonically increasing **fencing token / ownership epoch** on each protected write; the downstream resource must reject tokens older than the highest accepted epoch. A token checked only by the caller is not fencing.

Handoff protocol:
1. Advance durable ownership epoch at the authority.
2. Establish a new owner and transfer a verified snapshot/position.
3. Reject old-owner effects at the state/effect boundary.
4. Make in-flight commands retryable with stable operation IDs.
5. Drain or explicitly expire old pending work and reconcile divergent buffered events.

For a pure actor partition, a single owner and durable mailbox may avoid consensus in the hot path, but durable ownership election still needs a reliable authority if split-brain violates the invariant.

## 4. CRDTs and anti-entropy

Choose a CRDT only after stating its merge algebra: associative, commutative, idempotent merge for state-based CRDTs; operation-based CRDTs need their own reliable/causal delivery assumptions. Test invariants beyond convergence. Counter addition does not prevent an account from going below zero; a last-writer-wins register can discard concurrent work; observed-remove sets require careful tombstone/causal-context retention and garbage collection.

For gossip/anti-entropy define peer selection, sampling rate, version summaries, bandwidth budget, state hashing/verification, periodic full reconciliation, compaction, and lifecycle for retired nodes. Convergence is conditional on eventual communication and correct merge semantics; gossip does **not** ensure bounded-time delivery or globally agreed membership.

For causal tracking, Lamport timestamps give a happened-before-compatible ordering but cannot detect concurrency; vector clocks/dotted version vectors can represent concurrent versions at metadata cost. Hybrid logical clocks can aid ordering/latency but do not by themselves confer consensus, fairness, or unique ownership.

## 5. Distributed workflows and transactions

Use a local ACID transaction when all authoritative state fits in one owner/database. For multi-owner workflows choose among:

- Sagas and compensations when effects are durable and business reversal is possible. Compensation may fail, must be idempotent, and may not undo external observations.
- Transactional outbox/inbox plus local transactions for asynchronous propagation; lag and replay must be visible.
- Coordinated distributed transactions only when participants and operational failure model justify the coupling; prepare/commit introduces availability and recovery costs.

Do not replace a hard financial or uniqueness invariant with a CRDT simply to eliminate coordination.

## 6. Testable claims

For each consistency claim write a minimal concurrent history: operations, invocation/response times or causal edges, fault timeline, expected/forbidden outcome. Check at least stale leader, overlapping writes, lost ACK, partition heal, ownership migration, replica lag, conflicting offline edits, and restart with partially persisted state. A test can find counterexamples; absence of counterexamples is not a proof.

Primary readings: [sources](sources.md), especially Raft, Google SRE distributed consensus, SWIM, and distributed locking with fencing.
