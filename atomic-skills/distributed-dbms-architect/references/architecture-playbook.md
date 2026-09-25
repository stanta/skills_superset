# Distributed DBMS architecture playbook

Use this guide after the requirements/guarantee contract in ../SKILL.md. Treat the matrix as a decision process, not a universal ranking. Separate **design invariant** (must always hold) from **optimization policy** (may evolve).

## 1. Choose the deployment and ownership model

| Family | Typical reason to consider | Cost/failure consequence to verify |
| --- | --- | --- |
| Single writer + async/sync followers | Existing relational semantics, limited write scale | Primary fencing, promotion safety, replica lag, replication mode, failover RPO |
| Partitioned leader-based KV/SQL, each shard replicated by Raft/Paxos | Independent shard throughput, explicit fault tolerance | Cross-shard transaction cost, routing, leader hotspots, one consensus group per partition |
| Leaderless/quorum/CRDT-oriented system | Available local writes and mergeable operations under partitions | Conflict policy, read repair/anti-entropy, tombstones, causal context, non-mergeable constraints |
| Separated transaction/log/storage roles | Independently scale write pipeline, commit conflict resolution, storage | Recovery epochs, coordinator bottlenecks, failure coupling and log retention |
| Geo-distributed transaction system | Cross-region transactional guarantees | Inter-region RTT, clock assumptions, placement and residency, quorum placement |

Avoid a binary CP/AP label. State concrete operations and partition scenarios. Explicitly compare an existing platform with a new DBMS build, including operational burden, compatibility, failure handling, license and vendor dependence.

## 2. Planes, contracts, and authoritative state

**Client/query plane:** authentication and admission; SQL/query parsing, planning and distributed execution if needed; shard-map cache with version; request IDs, deadlines, retries, snapshot and result freshness; bounded scatter/gather with pagination and cancellation.

**Transaction plane:** transaction coordinator, read timestamp/version, MVCC visibility and lock/conflict resolution; deadlock handling, intent resolution and commit decision; cancellation must not erase an in-doubt transaction. Define where transaction status is durably discoverable.

**Replication/data plane:** per-partition consensus groups (or explicitly different replicated state machine), replica apply ordering, WAL, snapshots, compaction and checksum. Distinguish durable log acknowledgment from later state-machine apply and from client-visible commit. On recovery, replay only committed entries and reconcile incomplete intents by documented rules.

**Control plane:** durable cluster identity, node/store registration, topology/failure domains, shard/range metadata, membership epochs, replica placement, operator scheduling, schema/feature versions, timestamp issuance if architecture requires it, key rotations and audit. Drive placement via reconcile(desired, observed), not unbounded imperative retries. Give each operation an ID, generation/precondition, progress status, abort/resume mechanism and rate limit. The control plane may be a separate consensus-backed service; avoid making every read synchronously depend on it when a versioned, safe cache suffices.

**Operator/security plane:** status API, emergency fencing, canary, pause/resume, change audit, mTLS, per-tenant authorization and encryption/key lifecycle. A management API may request topology changes; it must never bypass data-plane membership and epoch safety.

Key boundaries to document: shard map (version, owner group, key interval), node identity versus process incarnation, leadership term/lease, membership config, transaction version and decision, and observed durable log position.

## 3. Placement, partitioning, and online resharding

1. Select range, hash, consistent-hash, tenant-aware or hybrid partitioning from access locality, range scans and skew. Choose an initial shard size based on measured recovery, compaction and migration bandwidth, not an arbitrary shard count.
2. Model placement against failure domains (machine, rack, AZ, region), residency, tenant isolation and storage class. Avoid two replicas of the same shard in one correlated fault domain when the fault model excludes that domain.
3. Track per-shard bytes, QPS, CPU, writes, latency, replication lag, compaction debt and network. Placement objective should combine capacity, hot-spot relief, locality and safety. Throttle leader transfers, snapshot copying and concurrent moves to preserve foreground SLOs.
4. Define shard-state transition, e.g. SERVING → PREPARING_SPLIT → COPYING/CATCHING_UP → CUTOVER → CLEANUP. Make each transition durable, idempotent and restartable. Allocate new generation(s); redirect stale clients and fence old writes. Preserve transaction intent ownership and backup/CDC continuity across split and merge.
5. For replica changes, use the consensus protocol's safe configuration-change mechanism (joint consensus or implementation-specific equivalent). Add/catch up a new voter before removing an old voter, subject to the selected protocol's rules; never casually mutate the voter list in a control-plane database alone.
6. Specify what happens on metadata quorum outage: existing groups may continue serving with sufficiently valid cached placement, if epochs, auth and leases make it safe; routing to a moved group, new placement, cluster reconfiguration or timestamp allocation may have to stop. Document the exact contract.

## 4. Replication, read serving and fencing

For each shard record a stable group ID, incarnation, current config, term, leader, committed/applied indexes, durable log and snapshot identifiers. Prefer one leader for ordered writes where constraints are not naturally commutative. A leader acknowledges only after the protocol's commit condition and required storage durability are met; verify that acknowledgments survive the assumed failures, including lost page cache / disk failure where in scope.

Reads must identify their guarantee and mechanism: quorum/ReadIndex or an appropriate proven leader-lease protocol for linearizable reads; safe read timestamp and applied-index wait for follower reads; explicitly bounded staleness when offered. A follower merely having an open TCP connection to a leader does not prove freshness. A stale former leader may not accept writes after an epoch change; enforce fencing at the storage/application point, not only via client routing.

Snapshot installation must preserve checksums and generation, bound transferred bytes, reconcile concurrent log tail and reject incompatible snapshots. WAL retention and snapshot cadence must account for lagging replicas, CDC consumers and PITR. Test unclean restart after acknowledged writes, majority partition, disk-full, slow follower and delayed messages.

## 5. Storage engine and query/CDC boundaries

Use a WAL plus MVCC-aware B-tree or LSM engine according to access patterns. Benchmark write/read amplification, range scans, point reads, compaction stalls, compression, tombstones, bloom filters, write stalls, fsync and recovery time on realistic skew. Garbage-collect old versions only after the minimum of active transaction/snapshot, replica catch-up, backup, changefeed and legal-retention watermarks allows it; measure a stuck oldest snapshot explicitly.

Index writes and base-data writes must share an atomicity story. For secondary indexes with asynchronous maintenance, state the stale-read/repair semantics. For distributed joins and aggregations, bound fan-out, network shuffle, result memory, retry and tenant resource budgets. Define physical-plan stability and schema/index migration (expand → backfill → validate → cut over → contract); retain old readers during rolling upgrades where required.

For CDC/changefeeds, define whether the stream emits per-shard order, transaction order or global order; how snapshots and live events join without gaps; checkpoint position; deduplication; and the consequence of rebalance. An at-least-once feed needs idempotent consumers or a carefully specified transactional sink protocol, not an unqualified "exactly once" claim.

## 6. Capacity/cost evaluation

Estimate steady-state plus failure-mode headroom for CPU, disk usable space, replica count, WAL/snapshot backlog, network egress, inter-AZ/region replication, transaction metadata and compaction. Evaluate p99 under compaction, leader transfers, concurrent rebalances and one fault domain lost. Report trade-offs as measurements and assumptions; do not treat published benchmark throughput as portable to a different workload.

## ADR skeleton

Document context/workload, scope of promise, alternative designs, chosen invariant and algorithm, message/state sequence, durability boundary, fault assumptions, worst-case unavailability, performance/cost estimate, migration plan, observability, failure injection test and rollback. Mark unknowns that block implementation.
