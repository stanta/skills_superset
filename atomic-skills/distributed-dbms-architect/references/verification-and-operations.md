# Correctness verification, observability and operations

Use this file for design reviews, implementation acceptance and incident preparation. For chaos tests, also read the existing chaos-engineer skill; do not inject failures into production without authorization, blast-radius limits, stop conditions and a verified rollback.

## 1. Turn promises into falsifiable invariants

Create an evidence ledger with one row per promise: contract and scope → safety invariant → protocol state → observable trace → failure injection → checker/oracle → owner and result. Examples:

| Promise | Invariant / oracle | Inject and inspect |
| --- | --- | --- |
| Acknowledged writes are durable | After specified faults and recovery, an ACKed committed write remains visible; inspect history and durable log | Kill leader and power-cycle quorum members around ACK/fsync |
| At most one authoritative owner per range | Every accepted write is covered by a valid membership epoch/lease and linearization rule | Partition old leader during leader transfer and range split |
| Serializable cross-shard transactions | Adversarial histories contain no forbidden dependency cycle; check predicates as well as keys | Concurrent write-skew, coordinator crash and retries |
| Atomic transaction visibility | No legal read can observe only part of a committed multi-shard transaction | Delay finalization/intent resolution on one participant |
| Bounded-staleness follower reads | Observed read timestamp/lag respects explicit limit, otherwise fail/redirect | Slow follower, leader change and clock drift |
| Resumable online resharding | Exactly one authoritative mapping at cutover; no missing/duplicated logical mutations | Kill mover between snapshot, catch-up and cutover |
| Disaster recovery | Restore achieves measured RPO/RTO and passes integrity plus representative query checks | Restore backup + WAL/change archive into isolated cluster |

Run deterministic simulation with reproducible seed and controlled virtual time where possible (crash, drop, reorder, disk fault, clock jump, process pause). Use property-based state-machine tests for membership and transaction decision transitions; model-check a minimal protocol with TLA+/PlusCal or equivalent for high-risk algorithms. Run Jepsen/Elle-style histories on a representative deployed cluster: acknowledged and ambiguous operations must be represented accurately. Jepsen findings are workload/model-specific; a successful limited test does not prove all histories safe.

## 2. Failure matrix to fill in before rollout

For each event, document: allowed client result, data exposure, recovery owner, recovery steps, timing budget and acceptance test. Cover process crash, OS/power loss, disk-full/corruption, slow/partitioned network, asymmetric partition, clock skew/jump, AZ and region loss, metadata quorum loss, timestamp service outage, schema version skew, rolling upgrade, bad config and credential/key loss.

Critical rules:
- Quorum loss: stop operations whose contract requires a quorum, rather than promote by intuition or force a second writer.
- Unknown transaction outcome: preserve status and recover decision; do not treat timeout as rollback.
- Metadata outage: name which existing reads/writes may continue from versioned cache, and which topology/schema changes must pause.
- Storage corruption: verify checksums and repair from a trustworthy replica/backup; do not blindly overwrite the healthy copy.
- Failback: treat a rejoined former primary as a stale replica requiring rebootstrap/catch-up and fencing checks.

## 3. Database-specific observability

Expose dimensions by cluster, shard/range, replica, leader/term, AZ/region, tenant, operation and software version; cap high-cardinality labels or sample intelligently. Minimum signals:

- Request success/timeout/unknown outcome, p50/p95/p99 latency and throughput by consistency mode and workload.
- Raft/equivalent current term, quorum health, election churn, commit/applied/durable index gap, replica catch-up, snapshot install failures, membership/config generation and leader lease expiry.
- Transaction attempt/commit/abort/retry/IN_DOUBT counts, conflict and deadlock rates, prepare/decision age, slowest active read version, lock wait and intent-resolution backlog.
- Per-shard size, bytes and QPS skew, replica placement compliance, leader hotspot, ongoing split/merge/rebalance state, scheduler queue depth and failed/stuck operators.
- WAL fsync p99, disk errors and free space, compaction backlog/write stalls, MVCC GC debt, read amplification, cache/CPU/memory/network, log/CDC retention and backup lag.
- Auth failures, permission changes, KMS/certificate expiry, configuration drift and administrator/operator actions.

Alert on violated safety preconditions *before* availability dashboards turn red: unhealthy quorum, invalid epochs, near-full WAL, stuck prepared transactions, unsafe clock uncertainty, stale backups and replication lag beyond the promised freshness budget. Attach a runbook and operator action to every high-severity alert.

## 4. Backups and disaster recovery

Define data and metadata coverage, encryption and access restrictions, immutable/offsite copy where required, retention/legal constraints, PITR cut line, consistent per-shard/transaction snapshot semantics and WAL/log retention dependency. Explicitly distinguish local quorum availability from geo DR and cross-region async replication. Set numeric RPO and RTO **for each disaster class**, not one universal number.

Schedule isolated restores, check user-visible data and schema/index integrity, replay transactions/changefeeds as intended, compare manifest/checksums, measure loss window and elapsed recovery, and record evidence. Rehearse failover and failback using production-like volumes and constrained bandwidth. A snapshot created successfully is not a restore test.

## 5. Rolling change and operator safety

Implement explicit cluster and storage format versions, protocol feature gates and backward/forward compatibility matrix. Roll out one fault domain at a time where quorum math permits; gate upgrades on replication health, prepared-transaction age and disk headroom. Make metadata and schema migrations monotonic or provide a tested rollback. For irreversible on-disk upgrades use forward-fix plans and block unsupported downgrades. Keep a stable emergency admin path for pausing placement and fencing broken nodes.

For every split, move, repair, or upgrade persist an operation ID, precondition revision, phase, idempotent continuation step, rate/bandwidth budget, timeout behavior, rollback/roll-forward procedure and audit actor. Admission control must prefer foreground transactions over runaway repairs while ensuring background debt cannot grow without bound.

## 6. Benchmark protocol and release gate

Benchmark realistic distributions (uniform, Zipf/hot keys, long range scans, cross-shard transactions, mixed reads/writes), concurrency, data volume and geographic RTT. Record p99 **during** compaction, one-AZ outage and rebalance, not just idle throughput. Verify no safety regression when tuning batching, leases, follower reads, retries or WAL settings. Include cold start and recovery time.

Release only after: invariant-to-test mapping is complete; consistency histories and crash recovery pass within the defined test budget; every critical fault class has an exercised runbook; backup restore verifies RPO/RTO; security and tenant isolation are tested; p99/capacity SLO under degradation is measured; on-call has an explicit rollback/fencing path. Track unresolved risks as explicit deployment blockers or approved limitations.
