# Hybrid Ray + DANMA (distributed asynchronous neuromorphic architecture)

This is an architectural *option and benchmark hypothesis*, not proof that Ray is necessary or faster. Ray can manage Ray actors hosting sharded native runtimes while DANMA controls neural semantics and fine-grained event transport.

## Responsibility split

| Plane | Ray responsibility | DANMA responsibility |
| --- | --- | --- |
| Control | Actor launch/restart, resource placement, job packaging/operations | Stable neuron/shard IDs, edge ownership, route/version mapping, migration protocol |
| Compute | Reserve coarse actor CPU/RAM; start Rust runtime via FFI/service | Compact neuron arrays, CSR/delta connections, event queues, SIMD/CPU workers |
| Data | Coarse batches/config/checkpoint handles or optional RPC envelopes | Hot-path signals, directed inter-shard communication and batched feedback |
| Training | Launch experiments; optionally run standard Ray Train baseline | Forward activation ledger, atomic local backward, optimizer/weight ownership |
| Recovery | Recreate actor after crash | Durable shard checkpoint, replay/dedup, epoch/fencing, delayed-feedback policy |
| Observability | Actor/task/node health, cluster placement | Per-neuron EventID trace, edges, weights, late/duplicate feedback |

**No one-Ray-actor-per-neuron design.** Put thousands/millions of compact neurons per Rust shard and a bounded number of shard actors per physical node. Keep an explicit maximum on actors and Ray calls. Compare Ray actor RPC batch transport to direct QUIC/TCP between shards; use gossip/DHT for membership/discovery only, not guaranteed addressed delivery.

## Neural protocol boundary

Forward message: trace ID, local activation EventID, source/target shard and neuron, graph/weights version, bounded payload, hop/route TTL and deadline. Feedback message: target activation EventID, **logical contribution ID**, authenticated source/edge identity, gradient/target kind, forward-time version, expiry. Distinct downstream branches may legitimately contribute feedback to one activation; deduplicate per contribution, not merely per EventID.

Mark the per-activation effect and weights update atomically in the shard owner. Retain processed-contribution IDs or enforce an epoch-based replay fence after ledger expiry. Define fan-in aggregation, partial-gradients at TTL, stale-version treatment, and policy for graph edge replacement. Exact mathematical backpropagation is a *testable property*, not guaranteed by protocol correctness. Track timing and versions to reproduce experiments.

## Option evaluation

A. Ray Core cluster with Rust shard actor and Ray-batched messages. Least new infrastructure, possible RPC/object-store overhead.

B. Hybrid Ray for shard placement / lifecycle, Rust direct socket transport for the event data plane. More complex routing and migration, potential lower hot-path overhead.

C. Native Rust cluster with independent placement/membership. Maximum control, highest operational engineering burden.

Keep the same neuron/synapse model, dataset, TTL, dedup and checkpoint semantics for all variants; otherwise benchmark differences are uninterpretable.

## Three-node acceptance experiment

Start with 3 CPU hosts, fixed graph and event stream; run baseline single-node Rust; run A/B (and C only if justified). Measure events/s, bytes/event, p50/p99 end-to-end forward/backward latency, CPU%, peak RSS, object-store/spill, recovery time, convergence/validation loss and result reproducibility. Add fork/join, duplicate feedback, delayed TTL expiry, hot shard, lost ack after effect and one-node failure. Record SLOs and pass/fail thresholds **before** observing results.

Related project skill: `../../distributed-computing-architecture/references/asynchronous-graph-computation.md`. Do not claim that Ray alone implements a PyTorch `PrivateUse1` backend or TensorFlow PluggableDevice; the DANMA device adapter is a separate project.
