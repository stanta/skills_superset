# Operations and reliability

## Topology

Use homogeneous nodes when practical and make fault domains explicit: datacenter, rack/AZ, host.

Production keyspaces should use `NetworkTopologyStrategy`; `SimpleStrategy` is not a production default because it is not DC/rack-aware.

ScyllaDB uses Raft for schema and topology management in current releases. Topology/schema changes require the relevant Raft quorum, while ordinary data availability follows the chosen RF and operation consistency level.

## Tablets and topology changes

Current ScyllaDB stable uses tablets by default for new keyspaces.

Before expansion, shrink, node replacement or DC change:

- verify tablet support state and driver compatibility;
- check disk/network headroom for migration;
- watch tablet balancing and streaming;
- avoid simultaneous unrelated heavy operations that compete for the same I/O/network budget;
- verify post-change ownership/balance before declaring completion.

## Hardware and OS

Follow current platform-specific ScyllaDB system requirements rather than generic Cassandra advice.

Current official guidance includes:

- modern multi-core CPUs; ScyllaDB scales shard-per-core;
- at least 2 GB RAM per core and at least 16 GB per system as a baseline;
- fast NVMe SSDs for demanding workloads;
- RAID0 across multiple drives when relying on ScyllaDB replication for durability;
- XFS for production;
- 10 Gbps or faster networking for large/production nodes;
- run ScyllaDB setup/iotune/perftune tooling and keep CPU/IRQ placement intentional.

RAID0 is a performance layout, not a durability mechanism; durability comes from replication plus backup.

## Disk capacity

Plan capacity from **physical replicated bytes**, not logical application bytes.

```text
cluster_physical ~= logical_data * RF * storage_overhead
per_node ~= cluster_physical / node_count
```

Then reserve headroom for compaction, repair/rebalance, snapshots and growth.

Current ScyllaDB guidance lists recommended utilization targets approximately as:

- ICS: around 70% used (30% free), minimum safety around 80% used;
- LCS: around 50% used;
- STCS/TWCS: around 50% used.

Treat these as operational guidance, not a promise that every workload is safe at those exact numbers. Alert earlier when growth or repair traffic is bursty.

## Compaction

Compaction choice:

- **ICS**: default/general recommendation when no workload-specific reason exists; STCS-like read/write amplification with lower temporary space amplification.
- **LCS**: useful for read-heavy/update-heavy workloads where lower read amplification and predictable obsolete-data cleanup justify higher write I/O.
- **TWCS**: time-series/TTL workloads with time-window lifecycle; works best when TTL behavior is uniform and old windows stop receiving writes.
- **STCS**: legacy/general LSM behavior but usually prefer ICS when both are suitable.

Avoid routine major compactions. They can consume large I/O and disk headroom and are not a general maintenance step.

Monitor compaction backlog, pending tasks, disk amplification and latency during compaction.

## Repair and anti-entropy

Replication does not eliminate divergence. Repair reconciles replicas.

Rules:

- schedule repairs and verify completion;
- keep repair interval compatible with tombstone retention/`gc_grace_seconds`;
- avoid lowering grace periods without proving repair coverage;
- for tablet tables, consider the current automatic/incremental repair capabilities of the deployed release;
- test repair impact under production-like traffic.

## Backup and restore

Replication protects availability from replica failure; it does not protect against operator error, bad application writes, logical corruption or cluster-wide loss.

Maintain external backups. ScyllaDB Manager can orchestrate cluster backup; current documentation also describes snapshot/incremental and object-storage restore procedures.

A backup policy is incomplete without:

- retention;
- encryption/access control;
- off-cluster/object-store target;
- restore procedure;
- periodic restore drill;
- measured RPO/RTO;
- validation that restored schema/data is usable.

## Monitoring

Deploy ScyllaDB Monitoring Stack or equivalent Prometheus/Grafana/Alertmanager instrumentation outside the database cluster.

Watch at least:

- coordinator and replica p50/p95/p99 latency;
- dropped/rejected/timeout/error rates;
- per-shard CPU utilization and imbalance;
- cache hit ratio;
- disk utilization and I/O saturation;
- compaction backlog/throughput;
- memtable flush behavior;
- network bandwidth and packet loss;
- large partitions/rows/cells;
- repair age/status;
- tablet migration/balance;
- node availability and Raft/topology health.

Tail latency plus shard skew is often more actionable than cluster-average CPU.

## Failure drills

Test:

- one node loss at RF=3 under each production CL;
- rack/AZ loss;
- network partition;
- coordinator timeout after a write may already have committed;
- application retry storm;
- full/slow disk;
- compaction backlog;
- hot partition;
- node replacement;
- rolling upgrade;
- loss of topology/schema quorum;
- backup restore to a clean environment.

Document which APIs remain available in every failure mode and what staleness/data-loss contract clients observe.
