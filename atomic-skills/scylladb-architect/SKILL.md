---
name: scylladb-architect
description: Design, review, tune, benchmark and operate ScyllaDB clusters and applications. Use for CQL data modeling, partitioning, tablets, shard-aware drivers, consistency levels, LWT, compaction, repair, backup/restore, multi-DC topology, capacity planning, monitoring, and high-throughput low-latency workloads.
license: MIT
metadata:
  category: distributed-databases
  version: "1.0.0"
  last_verified: "2026-10-06"
  related-skills: distributed-dbms-architect, distributed-computing-architecture, database-optimizer, rust-engineer
---

# ScyllaDB Architect

Use this skill for ScyllaDB-specific architecture and operations. Use [distributed-dbms-architect](../distributed-dbms-architect/SKILL.md) when the task is to compare database families or design a database engine itself; use this skill when ScyllaDB is already selected or is a serious candidate.

ScyllaDB is a distributed, shared-nothing, LSM-based database with shard-per-core execution. Treat partitions, replica placement, consistency level, compaction and client routing as one end-to-end design. Do not tune one layer in isolation.

## Core workflow

1. **Specify the workload.** Record key cardinality, row/partition size distributions, read/write ratio, update/delete/TTL rate, fan-out, p50/p95/p99 latency targets, throughput, dataset growth, failure domains, DC layout, RPO/RTO, and whether any operation needs linearizability.
2. **Design from queries, not entities.** Start with concrete query shapes. Choose partition and clustering keys so each request reaches a bounded amount of data on a small, predictable replica set. Duplicate data across tables when required by distinct query patterns instead of forcing joins or broad scans.
3. **Choose topology and replication deliberately.** Prefer `NetworkTopologyStrategy` for production. Use RF >= 3 for fault-tolerant production unless an explicit durability/cost analysis justifies otherwise. For multi-DC, set RF per DC and choose client-local consistency levels.
4. **Use tablets unless a verified feature constraint requires vnodes.** Current stable ScyllaDB creates new keyspaces with tablets by default. Size and topology changes should be planned around tablet movement, balance and driver compatibility.
5. **Match consistency to the invariant.** `LOCAL_ONE`/ `ONE` optimize availability and latency but allow stale reads. `LOCAL_QUORUM` with RF=3 is a common per-DC choice when quorum intersection is required. Use `ALL` only with a quantified reason. Use LWT/Paxos only for operations that truly require linearizable compare-and-set semantics.
6. **Use ScyllaDB-native, shard-aware drivers.** Prefer current supported drivers with tablet support. Use prepared statements for repeated queries so routing information is available; use token-aware fallback only when shard-aware routing is unavailable.
7. **Bound concurrency and retries.** Use async concurrency/pipelining instead of giant batches. Retries and speculative executions are safe only for operations whose idempotence is known. Treat timeout outcomes as ambiguous for writes.
8. **Pick compaction from the write/read lifecycle.** Default to ICS unless workload properties favor LCS or TWCS. Avoid changing compaction strategy casually; measure read, write and space amplification.
9. **Budget disk for compaction and recovery.** Size for live data, RF, growth, compaction headroom, snapshots/backups and rebalance/repair traffic. Never plan to operate near full disk.
10. **Operate with repair, backup, monitoring and restore drills.** Replication is not backup. Schedule repair, verify external backups, test restore, monitor shard/node skew, tail latency, cache hit ratio, compaction backlog, disk pressure and large partitions.
11. **Benchmark the exact schema and driver path.** Test realistic key distributions, value sizes, consistency levels, concurrency and failure modes. Compare p50/p99/p99.9 and saturation behavior, not only peak throughput.

## Non-negotiable design rules

- **No unbounded partitions.** Bucket by time/hash/tenant dimension when one logical key can grow without a strict bound.
- **No hot partition keys.** A uniform row count is insufficient if a tiny key set receives most traffic.
- **No `ALLOW FILTERING` as a production query strategy.** Model a table for the access pattern instead.
- **No multi-partition batch as a bulk-ingest shortcut.** A batch is not a SQL transaction and a coordinator must fan it out. Prefer concurrent prepared writes; reserve batches mainly for same-partition mutations or an actual atomicity requirement.
- **No blind LWT.** Conditional statements use Paxos and add coordination. Use them for ownership/version transitions that require linearizability, not routine updates.
- **No blind retry.** Mark idempotence explicitly and keep retry budgets bounded.
- **No full-cluster scans in a latency-critical path.** Use a suitable table, index feature, analytics path, or separate workload class.
- **No schema/data-model review without partition-size math.** Estimate rows/partition, bytes/partition and request rate/partition.
- **No production deployment without repair and restore procedures.**
- **No performance claim without the exact ScyllaDB version, driver version and workload description.**

## Data-model checklist

For every table state:

- query it serves;
- partition key and expected key cardinality;
- clustering order and query bounds;
- expected median/p95/max partition size;
- read/write QPS per hot partition;
- row/cell/blob size;
- overwrite/delete/TTL behavior;
- consistency level by operation;
- compaction strategy and why;
- retention and tombstone lifecycle;
- whether LWT, CDC, secondary indexes or materialized views are used;
- expected tablet/data size and growth.

See [data modeling and consistency](references/data-modeling-and-consistency.md).

## Driver and request checklist

- use a supported ScyllaDB driver and verify tablet support for the deployed version;
- prepare repeated CQL statements;
- provide routing key/keyspace so token/shard routing works;
- bound in-flight requests per application instance;
- separate online latency-critical traffic from bulk/analytic traffic;
- use paging for potentially large SELECT results;
- classify statements as idempotent or non-idempotent before enabling retries/speculation;
- use same-partition batches only when they reduce round trips or enforce needed atomicity;
- instrument client latency separately from coordinator/server latency.

See [drivers and performance](references/drivers-and-performance.md).

## Operations checklist

- production topology uses DC/rack-aware placement and `NetworkTopologyStrategy`;
- tablets/Raft topology state is verified before topology changes or upgrades;
- CPU, memory, disk and network meet ScyllaDB recommendations;
- XFS and tuned I/O/IRQ settings are used for production deployments where applicable;
- disk free-space alerting accounts for compaction strategy;
- repair is scheduled and completes within the tombstone/repair safety window;
- backup leaves the cluster and restore is tested;
- ScyllaDB Monitoring Stack or equivalent metrics/alerts is deployed outside the database cluster;
- upgrades, node replacement, DC loss and quorum-loss behavior are documented and rehearsed.

See [operations and reliability](references/operations-and-reliability.md).

## Optional DANMA / actor-state profile

For a large asynchronous state machine, neuron network or actor system where the dominant access is `StateID -> compact mutable state`:

- use the state ID as a high-cardinality partition key when each state object is independently addressable;
- avoid storing transient per-event state in the same long-lived row if it has a different TTL/update pattern;
- keep hot state in the compute node's RAM and use ScyllaDB as durable distributed backing storage rather than doing a remote read/write for every arithmetic operation;
- write back changed state in bounded batches of independent prepared requests or by coalescing updates per state owner;
- separate immutable/static state, trainable mutable state, and TTL-bound event/dedup state into tables with different compaction/retention behavior when that reduces rewrite and tombstone amplification;
- use `LOCAL_ONE` for data that tolerates stale reads, `LOCAL_QUORUM` for state transitions requiring quorum visibility, and LWT only for ownership/version fencing that truly requires compare-and-set;
- benchmark cache-miss latency and write-back throughput separately from hot-path compute latency.

This profile is a starting point, not a universal schema. See [DANMA / actor-state profile](references/danma-actor-state-profile.md).

## Verification packet

For a production design, return:

1. workload and SLO table;
2. schema with query-to-table mapping;
3. partition-size and hotspot calculations;
4. replication/DC/tablet plan;
5. consistency matrix by operation;
6. compaction and retention plan;
7. driver/retry/concurrency configuration;
8. capacity model including RF and free-disk headroom;
9. repair/backup/restore plan;
10. benchmark plan and failure matrix;
11. observability dashboard/alert list;
12. explicit assumptions and version-specific caveats.

Primary sources and version notes: [sources](references/sources.md).
