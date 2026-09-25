# Ray Core: tasks, actors, objects, scheduling and performance

## Selection matrix

| Need | Choose | Avoid |
| --- | --- | --- |
| Independent bounded pure computation | `@ray.remote` function | Actor per call |
| Persistent state, process affinity or a large in-memory native runtime | Ray actor | Shipping full state in every task |
| Immutable result consumed by several tasks | `ObjectRef`, optionally `ray.put` once | Repeatedly serializing a large argument |
| Gang scheduling or locality of related workers | Placement group, explicit strategy | Treating a reservation as execution or checkpoint |
| Tiny high-rate messages inside one node | Native Rust/C++ in-process queue/batch | One Ray RPC per tiny message |
| General durable event processing | Dedicated log/stream plus Ray consumers where useful | Treating actor mailbox as persistent queue |

## Tasks and concurrency

- Launch independent tasks first, collect their ObjectRefs, then wait/consume; calling `ray.get()` in the submission loop serializes the work.
- Keep outstanding task count and returned bytes bounded. Use `ray.wait(refs, num_returns=...)` to drain completed tasks and issue more only when capacity permits.
- Separate *running concurrency* (resource requests) from *pending work* (application backpressure). Benchmark batch size against Python serialization overhead and tail latency.
- Beware nested `ray.get()` / waiting inside a task holding scarce CPU resources: it can starve the child work. Prefer passing refs as dependencies or explicitly freeing enough resources.
- Pass large immutable common data through a shared reference rather than implicit closure capture; avoid repetitive `ray.put()` for the same data.

## Actors and scheduling

- Use actors for mutable long-lived state and initialization cost, not as a transparent lightweight object class. Give each actor an explicit CPU/resource reservation; defaults are non-obvious (actors historically require 1 logical CPU to schedule but 0 while running).
- Default actor method processing is sequential. Async actors multiplex I/O on an event loop; CPU-heavy work blocks that loop. Threaded actors permit concurrency but require locks around state. Do not block an async actor with synchronous `ray.get()`/`ray.wait()`; await compatible references instead.
- Actor constructor/state is re-created on restart. Snapshot externally and restore explicitly. Owner death and detached-actor lifetime need an intentional policy.
- Use placement groups when multiple related actors must be scheduled together or near one another; `PACK` favors locality and `SPREAD` favors failure-domain distribution. Measure both: one optimizes network distance, the other blast radius. Handle partially recovered groups.
- Treat Ray CPU and memory resources as scheduling/admission hints, not hard OS isolation. Set `OMP_NUM_THREADS`, Torch intra-/inter-op threads and native Rust thread pools consistently.

## Objects, heap and spilling

Ray task results and `ray.put` values are immutable remote objects. An ObjectRef can pin an object for as long as references survive; watch for refs held in driver lists, closures, actors and serialized containers. NumPy arrays can be read zero-copy from local shared memory, but this does not mean inter-node transfers are zero-copy or that returned arrays are writable.

Budget three distinct tiers: Python/native heap, Ray object store/shared memory, and spill disk. When the working set exceeds object-store capacity, Ray can spill objects to disk; spilling protects capacity but can hurt latency and disk endurance. Set and monitor spill directory quotas and restore traffic. Use `ray memory` and memory dashboard while tracking actual RSS.

## Failure contract

Set retry options deliberately; the semantics of pure tasks differ from actor methods with side effects. A failed or unreachable call can have run successfully before its acknowledgement was lost. An ObjectRef is not by itself a durable checkpoint. Store the external side effect + processed logical operation ID atomically when strict idempotence is required. Maintain per-shard epoch/fencing if old and new owners might run concurrently.

## Performance review questions

Measure useful work per remote call, bytes moved per completed result, number of live refs, per-node spill rate, scheduler wait, actor queue age, cross-node locality, p50/p99 latency, retries, state reconstruction time and cost per successful job. Compare the identical workload with a local thread/process implementation; do not claim acceleration when overhead dominates.

Primary docs: [Actors](https://docs.ray.io/en/latest/ray-core/actors.html), [Objects](https://docs.ray.io/en/latest/ray-core/objects.html), [Resources](https://docs.ray.io/en/latest/ray-core/scheduling/resources.html), [Placement groups](https://docs.ray.io/en/latest/ray-core/scheduling/placement-group.html), [Get-loop anti-pattern](https://docs.ray.io/en/latest/ray-core/patterns/ray-get-loop.html), [Batch-result anti-pattern](https://docs.ray.io/en/latest/ray-core/patterns/ray-get-too-many-objects.html), [Object spilling](https://docs.ray.io/en/latest/ray-core/objects/object-spilling.html).
