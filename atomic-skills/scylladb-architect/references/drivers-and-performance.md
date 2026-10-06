# Drivers and performance

## Use ScyllaDB-native drivers

Prefer a current supported ScyllaDB driver for Java, Python, Go, Rust, C#/CPP-RS or Node.js when available. ScyllaDB drivers understand shard-aware routing and current drivers expose tablet support.

Version rule: check the current driver support matrix when upgrading ScyllaDB. Do not hardcode an old driver version into architecture guidance.

## Prepared statements

Prepare repeated statements.

Benefits:

- parsing/preparation is amortized;
- routing key metadata enables token/shard-aware routing;
- less query text is repeatedly transmitted;
- bind values reduce injection risk.

A "fast CQL query" that is repeatedly sent as an unprepared string can still route and parse inefficiently.

## Routing

Best order:

1. tablet-aware + shard-aware ScyllaDB driver;
2. shard-aware driver;
3. at minimum token-aware driver;
4. round-robin/non-aware routing only when unavoidable.

Ensure statements carry the keyspace and routing key information needed by the driver.

## Concurrency

ScyllaDB gains throughput from concurrency, but unbounded in-flight work causes queueing, timeouts and retry storms.

Set budgets for:

- in-flight requests per app instance;
- per-host connections;
- request deadline;
- retry count/budget;
- speculative execution;
- bulk-import concurrency;
- per-tenant or per-priority-class work.

Increase concurrency until p99 latency, server queueing or saturation metrics show the knee; do not optimize for highest throughput after tail latency collapses.

## Batching

CQL `BATCH` is not a generic bulk throughput mechanism.

Use it when:

- multiple mutations target the same partition and round-trip reduction helps;
- the atomicity semantics are actually required.

Avoid large multi-partition logged batches. A single coordinator must fan them out and batchlog/atomicity adds cost. Independent writes are usually better sent as concurrent prepared requests so each can route directly to its own replica.

## Paging

Page SELECTs that may return large result sets. A single huge result creates memory pressure and long request occupancy. Keep page size aligned with row size and downstream consumption rate.

For analytical scans, use a workload path that avoids polluting the latency-critical cache when the deployed release supports bypass-cache/workload prioritization features.

## Idempotence, retries and speculative execution

Classify every write:

- idempotent deterministic set;
- commutative but repeated effect changes magnitude;
- conditional/LWT;
- non-idempotent append/list/counter/external effect.

Only enable automatic retry/speculation where duplicate execution is safe under the driver's semantics. In current ScyllaDB Java driver behavior, retries/speculative executions are tied to idempotence marking.

Timeout on a write means **outcome unknown**. If the application needs exactly-once effect, use a stable operation ID and a data model that makes duplicate application harmless; a driver retry policy cannot provide end-to-end exactly once.

## Hot partitions and admission control

A hot partition is a single-shard bottleneck even when the rest of the cluster is idle.

Mitigations:

- redesign the partition key;
- add a bounded hash/time bucket;
- cache read-heavy immutable/hot state outside the DB;
- coalesce writes at the owner;
- use per-partition rate limiting as overload protection where appropriate;
- separate priority classes/workload classes.

## Cache-aware design

ScyllaDB keeps hot data in memory, but application-side locality can still matter when every database round trip is expensive relative to the computation.

For actor/neuron/state-machine workloads:

- keep active working state near the compute owner;
- use ScyllaDB as durable distributed backing state;
- fetch on cache miss/migration/recovery;
- coalesce or asynchronously flush state updates according to durability requirements.

This turns database latency from a per-arithmetic-operation tax into an amortized storage/recovery cost.

## Benchmark method

Always report:

- ScyllaDB version;
- driver/version;
- tablets or vnodes;
- schema and compaction;
- RF and consistency level;
- dataset size relative to RAM;
- read/write/update/delete mix;
- row and partition sizes;
- key popularity/skew;
- concurrency and connection count;
- cache warm/cold state;
- p50/p95/p99/p99.9;
- throughput;
- CPU, disk, network and compaction load.

Test steady state long enough for memtable flush and compaction behavior to appear. Short tests that fit in cache are not storage benchmarks.
