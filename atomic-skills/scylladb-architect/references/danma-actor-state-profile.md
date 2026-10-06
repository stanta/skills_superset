# DANMA / actor-state profile

This profile applies to systems with very large numbers of independently addressed mutable state objects: neurons, actors, agents, simulation cells or graph vertices. It is not a requirement for ordinary ScyllaDB applications.

## Baseline model

For one independently addressable object per partition:

```sql
CREATE TABLE danma.neuron_state (
    neuron_id bigint PRIMARY KEY,
    version bigint,
    static_state blob,
    trainable_state blob,
    updated_at timestamp
) WITH compaction = {
    'class': 'IncrementalCompactionStrategy'
};
```

A 10 KB row is comfortably below ScyllaDB's low-latency soft row limits. The primary design questions are write frequency, RF, cache hit rate and hot-key distribution.

## Split by lifecycle, not by aesthetic purity

A useful decomposition is:

```text
long-lived static metadata
    neuron_id -> topology/configuration

mutable trainable state
    neuron_id -> weights/version/stats

short-lived event state
    (bucket, event_id, neuron_id) -> activation/dedup/feedback
```

Reasons to separate:

- static state should not be rewritten with every training update;
- trainable state may use overwrite-heavy compaction behavior;
- event/dedup state may use TTL and TWCS/bucketed partitions;
- retention and backup requirements differ.

Do not split if every operation always requires all fields and the split only adds network round trips.

## Hot working set

Preferred runtime path:

```text
signal -> DANMA worker -> RAM-resident active neuron
                         |
                         +-- cache miss -> ScyllaDB
                         |
                         +-- coalesced/async durable write-back -> ScyllaDB
```

Avoid:

```text
signal -> remote DB read -> compute -> remote DB write
```

for every activation when the arithmetic itself is microsecond-scale.

Use ScyllaDB for:

- durable backing state;
- crash recovery;
- shard/node migration;
- replicas/failover;
- checkpointed trainable state;
- bounded TTL event/dedup persistence when crash survival is required.

## Ownership and concurrency

If exactly one compute owner should mutate a neuron at a time, maintain an application-level owner epoch/version.

Possible patterns:

- deterministic owner from runtime partitioning plus failover fencing;
- `UPDATE ... IF version = ?` only when a linearizable ownership transition is needed;
- store owner/epoch in a small control table instead of putting every ordinary state update through LWT.

The hot path should use ordinary prepared writes once ownership is established.

## Consistency suggestions

These are defaults to test, not mandates:

| State | Candidate CL |
|---|---|
| reconstructible cache/checkpoint data | LOCAL_ONE |
| durable trainable state where stale failover is unacceptable | LOCAL_QUORUM |
| ownership/epoch compare-and-set | LWT + appropriate serial consistency |
| TTL event/dedup state | LOCAL_ONE or LOCAL_QUORUM according to duplicate/replay tolerance |

Do not call the entire system "strongly consistent" because one table uses quorum or LWT.

## Write amplification control

Do not rewrite a monolithic 10 KB state blob on every tiny weight delta without measurement.

Options:

- keep state in RAM for a bounded flush interval;
- coalesce multiple updates to the same neuron;
- persist versioned checkpoints;
- split frequently updated scalar/version columns from larger infrequently changed blobs;
- append a bounded delta log only if replay cost and compaction/retention are explicitly controlled.

Every buffering choice changes crash-loss RPO. State that RPO in the design.

## Capacity example

For `1e9` neurons at 10 KB logical each:

```text
logical ~= 10 TB decimal
RF=3 raw replicas ~= 30 TB before LSM/metadata/headroom
```

Do not size a production cluster at 30 TB usable. Add:

- compaction/free-space target;
- growth;
- repair/rebalance headroom;
- snapshots/backups;
- secondary tables/event state.

The practical bottleneck may be write rate and hot working set rather than raw capacity.

## Benchmark plan

Measure separately:

1. hot RAM-hit activation latency;
2. ScyllaDB cache-miss read latency;
3. dirty-state flush throughput;
4. p99 under compaction;
5. failover state reload time;
6. node loss at RF=3;
7. hotspot skew;
8. write coalescing interval versus RPO;
9. 10 KB value read/update throughput;
10. tablet rebalance during continued training traffic.

The target is not "ScyllaDB is fast"; the target is that storage overhead stays outside the dominant compute path.
