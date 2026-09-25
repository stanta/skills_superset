---
name: ray-distributed-computing
description: Designs, implements, reviews, tunes and operates Ray clusters and applications: Ray Core tasks, actors, ObjectRefs, object store, scheduling, placement groups, backpressure, failure recovery, Ray Data/Train/Tune/Serve, KubeRay, security and observability. Use for Python distributed CPU/GPU computing, PyTorch/TensorFlow jobs and hybrid Ray + Rust/DANMA shard runtimes.
metadata:
  category: distributed-computing
  version: "1.0.0"
  related-skills: distributed-computing-architecture, rust-engineer, ml-pipeline, cloud-architect, kubernetes-specialist
---

# Ray Distributed Computing

Design Ray applications by locating state, sizing work, making failure semantics explicit, and measuring real bottlenecks. Ray is an execution and orchestration runtime, **not** a durable database, an automatically exactly-once message bus, a neural compute device, or a substitute for application-level correctness.

## Trigger and scope

Use this skill to choose Ray Core tasks versus actors; build or optimize Ray clusters; schedule CPU/GPU jobs; control memory and object movement; handle retries and checkpointing; deploy with KubeRay; debug latency and OOM; or integrate Ray Data, Train, Tune and Serve. For distributed neuromorphic workloads, use [DANMA integration](references/danma-integration.md): place one Ray actor per *shard*, not per virtual neuron.

Before implementation, inspect the repository, installed `ray.__version__`, Python/OS, deployment mode (local, VM, Kubernetes), API signatures and matching versioned Ray documentation. The online `latest` docs can change; do not copy examples from `master` / development docs into a pinned release without verification.

## Core principles

1. **Select the correct unit of execution.** Stateless bounded work -> remote task; mutable local state and affinity -> actor; large immutable results -> ObjectRef; data pipelines -> Ray Data; data-parallel ML -> Ray Train. Keep tiny events in batches inside an actor/worker. A Python actor commonly has its own worker process; a billion actors are not a practical stand-in for a billion neurons.
2. **Make state ownership explicit.** Identify who owns mutable data, which operation may write it, how an actor restarts, and where checkpoints are stored. Remote objects are immutable; an ObjectRef is not a mutable shared-memory variable.
3. **Bound work and memory.** Set maximum outstanding task refs, result batch size, actor mailbox/in-flight requests, object-store footprint, spill-disk allowance, per-tenant concurrency, retries and queue depth. Use `ray.wait()` for backpressure; process ready results in bounded batches.
4. **Treat resources as scheduling tokens.** Declare `num_cpus`, `num_gpus` and other resources explicitly. Ray logical CPUs do not cap operating-system CPU or thread use. Coordinate NumPy, BLAS, OpenMP, PyTorch and native thread pools.
5. **Separate cluster recovery from data recovery.** Actor restart recreates constructor state; retries can repeat committed side effects. Persist state externally and use stable operation IDs plus atomic effects where required.
6. **Optimize data movement first.** Prefer locality, batched task input/output, one shared ObjectRef for repeated large immutable inputs, and direct native in-process data access. Measure serialization, object-store pinning, spilling and network traffic.
7. **Secure the environment, not just the endpoint.** Put clusters in a controlled network, run trusted code, segment mutually untrusted tenants, protect dashboard/jobs/client access, and apply token/TLS/VPN controls supported by the deployed version.
8. **Prove with tests and measurements.** Benchmark local versus remote work, steady state and recovery, p50/p99 latency, cost, memory and throughput. Never claim linear scaling from a single no-failure run.

## Execution workflow

### 1. Frame workload and constraints
Record task sizes and durations, actor state footprint, input/output bytes, locality, ingress rate, required ordering, CPU/GPU/RAM, node churn, network topology, p99 SLO, durability/RPO, cost, trust boundary and minimum supported Ray version. Write down safety invariants and whether work is replayable.

### 2. Choose Ray's level in the stack
Use plain processes/asyncIO for simple single-host workloads; Ray tasks for independent coarse-grained functions; actors for shard/state affinity; Data for dataset transformations; Train for supported ML training; Tune for search trials; Serve for online serving; KubeRay for Kubernetes operations. Do not add Ray merely because the system is distributed; compare to MPI, custom Rust transport, native framework distributed training or a queue if the critical path has tiny messages.

### 3. Design task/actor/resource placement
Set explicit resource requests, actor concurrency policy, placement groups only when gang scheduling or locality is genuinely required, and stable actor ownership. A placement group reserves resources but does not provide persistence. Distinguish head/control-plane resources from worker capacity. See [core patterns](references/core-patterns.md).

### 4. Define object and memory flow
Draw the ObjectRef lineage: creator, owner, holder, consumer and expiry. Estimate live data plus copies plus heap, object-store, spilling and deserialization. Avoid repeated large argument serialization and `ray.get()` in the submission loop. See [core patterns](references/core-patterns.md) and [recipes](references/recipes.md).

### 5. Specify retry/effect boundary
Classify every operation as pure, idempotent, compensatable or non-repeatable. Specify task `max_retries`, actor `max_restarts` and actor `max_task_retries` deliberately. For writes, implement application-level dedup and durable effect logs rather than assuming exactly-once execution. Define behavior for lost owner, restarted actor, spilled/lost object, failed head, partial placement group and network partition.

### 6. Package and deploy
Pin Python and Ray versions across nodes. Prefer versioned container images for production; use `runtime_env` for development/job-specific dependencies after checking supported fields for the installed release. For multi-node Ray Train checkpoints, configure cloud/shared persistent storage. For KubeRay, choose RayJob, RayCluster or RayService for the actual workload; do not enable GCS-FT indiscriminately. See [operations](references/production-operations.md).

### 7. Observe and secure
Measure queue time, task runtime, actor restarts, failures, ref count, heap/object-store pressure, spilled/restored bytes, cross-node transfers, placement wait, network p99, resource utilization and checkpoint freshness. Use Ray Dashboard, State API/CLI, logs and metrics, supplement with application traces. Keep Ray endpoints inside controlled networks. See [operations](references/production-operations.md).

### 8. Validate and optimize
Run a single-node baseline, then two-/three-node benchmark with fixed workload. Inject worker crash after side effect before acknowledgement, actor restart, head disruption, lost object, CPU oversubscription, full spill disk, skewed shard, slow node and retry storm. Confirm correctness *before* interpreting speedups.

## Choose detailed references

- [Core patterns](references/core-patterns.md): tasks, actors, scheduling, ObjectRefs, concurrency, batching and memory.
- [Production operations](references/production-operations.md): versioning, checkpointing, security, GCS, KubeRay, observability, failure testing.
- [ML platform](references/ml-platform.md): Data, Train, Tune, Serve, PyTorch/TensorFlow boundaries.
- [DANMA integration](references/danma-integration.md): Ray orchestration versus Rust/event data plane, per-shard actor, EventID semantics and benchmarks.
- [Recipes](references/recipes.md): bounded fan-out and shard actor starter patterns.
- [Sources](references/sources.md): official Ray documentation and scope of evidence.

For system-wide consistency/consensus questions, also read `../distributed-computing-architecture/SKILL.md`; for native Rust/FFI and unsafe memory ownership read `../rust-engineer/SKILL.md`.

## Required output

Provide: workload assumptions and installed versions; chosen task/actor/data topology; object/state ownership; resource and memory budget; retry/checkpoint contract; security/deployment design; reproducible correctness tests; benchmark methodology and observed numbers (only when measured); unresolved risks and rejected alternatives. For code changes, report files changed and exact tests actually run. Never present planned tests as passed tests.

## Red flags

One actor per tiny entity; `ray.get()` immediately after every `.remote()`; unbounded refs; huge captured closures; assuming actor restart restores state; enabling retries for irreversible effects; relying on logical CPUs for physical isolation; passing entire model/dataset in `train_loop_config`; using Ray ObjectRefs as mutable neural weights; putting an addressed, low-latency event stream on the driver; exposing dashboard or jobs to the internet; asserting that Ray alone creates a PyTorch `danma:0` device.
