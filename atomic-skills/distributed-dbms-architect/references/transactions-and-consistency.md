# Consistency and distributed transaction protocol guide

Specify the observed behavior first, then select a protocol and test it against adversarial histories. Do not infer transactional guarantees from the replication algorithm alone. See [Jepsen's consistency models](https://jepsen.io/consistency/models) for the exact relationship and incomparability of common isolation models.

## 1. Publish a guarantee per operation

| Contract | Scope to declare | Typical counterexample to test |
| --- | --- | --- |
| Linearizable read/write | Single key/object, range or documented API scope; real-time order | Read after acknowledged write via stale leader/follower |
| Serializable transactions | Multi-object transactions equivalent to a serial order; no requirement that order reflect wall-clock completion | Write skew/phantom caused by overlapping predicate reads |
| Strict serializability | Transaction serial order also respects real-time precedence | T1 commits, T2 starts later and misses T1 |
| Snapshot isolation (SI) | Atomic snapshot and write-conflict prevention under the product's exact SI definition | Doctors-on-call write skew on disjoint rows |
| Causal/session guarantees | Causally ordered updates; read-your-writes/monotonic reads where advertised | Session switches region and moves backward in visible history |
| Eventual/CRDT convergence | Merge function, anti-entropy, conflict resolution and tombstone policy | Concurrent updates and delete resurrection after delayed replication |

An isolation level is not identical to a consistency model for all client operations. Specify if real-time guarantees cross sessions/regions and whether failed transactions or read-only transactions have special behavior. Do not silently equate Serializable with Strict Serializable or Raft with linearizable multi-key transactions.

## 2. Single-shard write and strong read

Document the concrete commit linearization point. For a replicated state machine this generally entails durable leader logging, quorum replication under the current configuration, commit-index advance and correct ordered application. Whether follower durable fsync is part of acknowledgment depends on the chosen protocol, implementation and fault model; verify rather than assume. Crash-recovery must restore term/vote, log, membership and snapshot state in a way that cannot acknowledge a previously lost committed entry.

For strong reads, use a protocol with a proven freshness guarantee such as consensus ReadIndex/quorum validation or a rigorously bounded leader lease with appropriate fencing. Check leader change between the freshness check and read, applied-index lag, and split/move epochs. A local read at an old applied index is a stale read unless explicitly allowed.

## 3. Multi-shard read/write transactions

Choose the concurrency control method based on the desired guarantee:

- **MVCC + optimistic validation:** specify read version, read and write sets, predicate/range conflicts, validation and retry. Snapshot isolation needs write/write conflicts; serializability also needs to prevent anti-dependency cycles, write skew and phantom anomalies (for example serializable validation or SSI). Long readers delay GC.
- **MVCC + pessimistic locking:** specify lock table/intent durability, wait queues, timeouts, deadlock detection/avoidance, priority inversion and orphan cleanup. Do not let lock expiration allow two writers to commit across an incomplete coordinator transition.
- **Deterministic ordering:** specify transaction admission and knowledge of read/write sets, deterministic execution, sequencer availability and handling of non-deterministic functions. A sequencer does not eliminate durability or cross-partition recovery requirements.

Cross-shard atomicity needs a decision protocol **separate from each shard's replication**. If using two-phase commit, specify a durable transaction identifier, coordinator state and participant prepare records, the commit/abort decision and safe retries. Consensus-backed shards can durably replicate prepare/commit records; transaction recovery must reconstruct a unique global decision. Traditional 2PC can block when the decision is unavailable: do not claim non-blocking progress without a stronger protocol and proof. A participant must not forget a prepared transaction before it can safely learn the decision. Visibility of all writes across shards also needs explicit intent resolution, timestamp ordering or a read protocol that does not expose partially committed state.

Minimum transaction state model (implementation may refine it):
NEW → READING → PREPARING → {COMMITTED, ABORTED}, with an IN_DOUBT recovery state and terminal decision recorded durably. Document how racing abort and commit proposals are serialized; a timeout alone is not permission to abort a transaction whose commit may already be durable.

## 4. Time, snapshots and garbage collection

Record the actual assumptions for physical clocks, monotonic timers, NTP/PTP, failure and skew. HLC and centralized timestamp oracles help order events but do not by themselves prove external consistency. A TrueTime-style commit-wait requires a documented uncertainty bound and correct implementation. If the timestamp service is unreachable, specify whether transactions block, use a bounded allocation lease or degrade to a weaker explicitly exposed mode.

For follower/read-only snapshots, document globally safe read timestamp, lease/closed-timestamp or resolved timestamp mechanism, per-shard applied watermark and waiting/deadline. If a shard has not applied through requested read version, block, redirect or return a documented stale/error response. Set MVCC GC horizon no newer than the oldest read/snapshot, unresolved transaction, CDC or backup retention requirement.

## 5. Idempotency and ambiguous outcomes

Assume the network can drop the reply *after* a commit. Expose transaction-status lookup by stable transaction ID or idempotency key; persist deduplication for at least the actual retry horizon and across node failover. A client retry must not create a second external effect. Define client-side transaction retry of the **entire** transaction when validation fails; never reuse a stale read snapshot or replay a non-idempotent external call inside an automatically retried transaction. Distinguish NOT_COMMITTED, COMMITTED and UNKNOWN/IN_DOUBT in protocol and telemetry.

CDC, message sinks and payment-like side effects require an outbox/inbox or explicitly atomic sink contract. Avoid marketing "exactly once" unless its boundaries (transaction, durable dedupe, consumer side effects and retention) are specified and tested.

## 6. Counterexample-driven acceptance cases

1. T1 writes A then receives ACK; T2 starts on another gateway/region and reads A. Assert the advertised real-time behavior.
2. Two concurrent doctors each observe the other on call and each set themselves off call. SI may allow both; serializable must preserve the invariant through conflict detection or another constraint.
3. Crash a coordinator just before prepare, after all prepares, after durable commit but before reply, and while finalizing only one shard. Repeated retries and recovery must converge on one decision without partial visibility under an atomic contract.
4. Delay old-leader messages while electing a new leader and resharding. Epoch checks and consensus must reject stale authoritative writes.
5. Force max clock skew, suspend the timestamp oracle, delay a follower, and hold a long read while GC/compaction occurs. Assert read guarantees or explicit failure, never silent corruption.
6. Replay transaction/status and CDC delivery after failover. Validate idempotence, ordering scopes and retention policy.

For detailed runbooks and test coverage use verification-and-operations.md. Link every guarantee to an executable workload/history checker and a fault assumption.
