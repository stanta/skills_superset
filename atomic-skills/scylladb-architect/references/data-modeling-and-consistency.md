# Data modeling and consistency

## Query-first modeling

ScyllaDB is not a relational modeling exercise. Start from the exact reads and writes the application performs and create tables that make those access patterns single-partition or tightly bounded whenever possible.

For every query, write:

```text
query:
partition_key:
clustering_range:
expected_rows:
expected_bytes:
expected_qps:
consistency:
```

If a query cannot be expressed without scanning unrelated partitions, either redesign the table or move that query to a different serving/analytics system.

## Partition keys

Good partition keys have both:

1. **cardinality** high enough to distribute data;
2. **traffic distribution** broad enough to avoid hot keys.

A UUID is not automatically a good partition key if most traffic targets only a tiny subset of UUIDs.

Estimate partition size before implementation:

```text
partition_bytes ~= rows_per_partition * avg_row_bytes + metadata/LSM overhead
hot_partition_qps ~= total_qps * hottest_key_fraction
```

Use time/hash bucketing when logical entities can grow indefinitely:

```sql
PRIMARY KEY ((tenant_id, bucket), event_time, event_id)
```

The bucket width must be chosen from retention, QPS and expected bytes, not from a generic "daily/monthly" rule.

Large partitions increase single-shard latency and can create oversized allocations. Use ScyllaDB's `system.large_partitions` diagnostics and alert before partitions become operationally dangerous.

## Clustering keys

Use clustering columns to keep rows needed together ordered inside a partition. The WHERE clause should bind the partition key and then constrain clustering columns in their declared order.

Do not model "one table for everything" with wide optional columns and later depend on filtering.

## Row and blob sizing

Current ScyllaDB limits allow very large rows/blobs, but low-latency workloads should stay far below hard limits. The official limits page describes hundreds of KB as a soft range for good row latency and recommends blobs below 1 MB. Treat 10 KB values as ordinary; still measure rewrite and network cost if frequently updated.

For mutable object state, prefer a representation that avoids rewriting large unrelated fields on every update. Splitting a logical object across columns/tables is useful only when access and lifecycle patterns genuinely differ.

## Denormalization

Duplicate data when two query patterns require different partition layouts. Keep update fan-out explicit and bounded. If duplicated tables must be updated together, decide whether temporary divergence is acceptable; do not assume multi-table atomicity.

## Deletes, TTLs and tombstones

Deletes and expired TTL data create tombstones that remain until compaction can safely remove them.

Rules:

- choose retention deliberately;
- avoid high-frequency delete/reinsert churn when a different lifecycle model works;
- keep repair cadence compatible with `gc_grace_seconds` safety;
- for TWCS tables, prefer a consistent table TTL and avoid arbitrary overwrites/deletes that prevent whole SSTables from expiring efficiently;
- do not lower `gc_grace_seconds` merely to reclaim space unless repair and failure assumptions justify it.

## Consistency matrix

Consistency level is per operation.

Typical single-DC RF=3 choices:

| Operation need | Candidate CL | Trade-off |
|---|---|---|
| Lowest latency / stale read acceptable | LOCAL_ONE | One local replica; highest availability, weaker freshness |
| Quorum visibility in local DC | LOCAL_QUORUM | Majority of local replicas; higher latency and lower availability |
| Every replica must respond | ALL | Stronger acknowledgement but fragile under failures |

A quorum write plus quorum read on the same replica set gives quorum intersection, but "strong consistency" still depends on exact operation semantics and conflict/timestamp behavior. Use precise wording.

For multi-DC clusters, keep latency-critical requests local unless the invariant requires cross-DC coordination. Configure RF per DC with `NetworkTopologyStrategy`.

## LWT / conditional updates

Statements with `IF` use Paxos and provide linearizable conditional behavior. They add coordination rounds and have ambiguous timeout outcomes: a timeout does not prove the condition/update failed.

Use LWT for:

- ownership acquisition;
- version/epoch compare-and-set;
- uniqueness when no weaker design suffices;
- fencing transitions.

Avoid LWT for ordinary counters, telemetry updates, append-like events or state changes that can be modeled with an idempotent deterministic write.

After an uncertain LWT result, follow driver/documented recovery semantics: retry transient failures when safe or read the state to determine the outcome.

## Keyspace baseline

Production keyspaces should normally use `NetworkTopologyStrategy`. New stable ScyllaDB keyspaces use tablets by default unless configuration or an explicit keyspace option changes that.

Example single-DC baseline:

```sql
CREATE KEYSPACE app
WITH replication = {
  'class': 'NetworkTopologyStrategy',
  'dc1': 3
}
AND durable_writes = true;
```

Do not disable durable writes in production without a quantified durability analysis.

## Tablets

Tablets are ScyllaDB's current data-distribution mechanism for new keyspaces. They move and balance across nodes and shards during topology changes.

Design implications:

- verify all client drivers support tablets for the deployed ScyllaDB version;
- consider expected table size and tablet sizing for very large tables;
- monitor tablet balance/migration during expansion or replacement;
- do not assume old vnode operational procedures apply unchanged;
- enabling/disabling tablets is a keyspace creation choice, not a casual online toggle.

Use vnodes only when a required feature or compatibility constraint is verified against the current release.
