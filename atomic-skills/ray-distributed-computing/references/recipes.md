# Ray starter recipes (verify against installed Ray version)

## Bounded fan-out without serial `ray.get`

~~~python
import ray

@ray.remote(num_cpus=1, max_retries=1)
def transform(batch):
    # Keep this operation pure/idempotent and sufficiently coarse-grained.
    return sum(batch)

def run_bounded(batches, window=16):
    if window < 1:
        raise ValueError("window must be positive")
    pending = []
    total = 0
    for batch in batches:
        if len(pending) >= window:
            ready, pending = ray.wait(pending, num_returns=1)
            total += sum(ray.get(ready))
        pending.append(transform.remote(batch))
    while pending:
        ready, pending = ray.wait(pending, num_returns=1)
        total += sum(ray.get(ready))
    return total

if __name__ == "__main__":
    ray.init()
    print(run_bounded([[1, 2], [3, 4]], window=2))
~~~

The window bounds *in-flight references*, not running concurrency; `num_cpus` controls Ray scheduling. For very large results, process/discard each batch promptly; cap input batch size.

## A coarse shard actor, not a neuron actor

~~~python
import ray

@ray.remote(num_cpus=2, max_restarts=1, max_task_retries=0)
class ShardActor:
    def __init__(self, shard_id: int):
        self.shard_id = shard_id
        # Load a versioned Rust shard checkpoint or initialize a test shard.
        self.state = {"processed": set(), "total": 0}

    def process_batch(self, contributions: list[tuple[str, int]]):
        for contribution_id, value in contributions:
            if contribution_id not in self.state["processed"]:
                self.state["processed"].add(contribution_id)
                self.state["total"] += value
        return self.state["total"]

# TEST DEMONSTRATION ONLY: this in-memory set is lost after actor restart.
# For production, atomically persist effect + dedup ledger and restore it in __init__.
~~~

Do not interpret actor `max_restarts` as persistence or retry-safe side effects. Use a durable per-shard checkpoint and write-ahead/effect boundary; validate recovery with crash injection.

## Minimal benchmark contract

Run (1) local Python/Rust baseline, (2) Ray local cluster, (3) 2–3 node Ray cluster, and if evaluating DANMA (4) direct Rust transport with same workload. Warm up each variant; fix graph/data/seed; measure distribution over multiple runs; report environment, node CPU/RAM, Ray version, batch size, live ObjectRefs, p50/p99, throughput, network bytes and failure recovery. Never report an estimated speedup as measured.
