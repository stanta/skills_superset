# Ray production operations, reliability and security

## Reproducible environment

- Record exact Ray, Python, OS/architecture, PyTorch/TensorFlow and KubeRay versions. Use corresponding *versioned* API docs for production upgrades; never assume development-channel APIs are released.
- Use pinned container images with build provenance for production Ray workers. Prefer `runtime_env` for iterative development or per-job variation; distinguish driver dependencies from child task/actor dependencies. Keep all Ray nodes on compatible Python/Ray versions and test rolling changes.
- Avoid passing broad local directories, virtual environments, secrets or huge model weights through `working_dir`. Use object storage/artifact registry for large datasets and models.

## Correctness, retry and checkpoints

- Ray tasks may retry after worker crash; actor restart reruns constructor, not application state. Actor method retries can re-execute already applied effects after lost acknowledgement. Configure `max_retries`, `max_restarts` and `max_task_retries` based on whether the operation is safe to replay.
- Persist checkpoints outside the actor and (for multi-node training) outside any single node. Checkpoint must include model/optimizer state, version, relevant random state, input cursor and applied-operation ledger as required by semantics. Validate restore from an actual node loss.
- Use stable logical operation IDs, dedup retention covering retry/replay horizon and atomic effect-plus-dedup where essential. Treat a timeout as an *unknown* outcome.
- Define failure for head/GCS, killed actor, interrupted job, partial placement group and object loss. Do not imply that enabling actor restarts or GCS-FT provides application-level durability.

## KubeRay and control plane

Choose the Kubernetes resource appropriate to lifecycle: RayCluster for an existing cluster, RayJob for a bounded job, RayService for continuously served applications. Size head node and isolate control-plane load. Place workers using affinities/taints as appropriate. Reserve disk for logs and object spilling; account for autoscaler lag and cold-start latency.

GCS availability requires an explicit design. Follow the Ray version's KubeRay GCS-FT guidance; the documented Redis-backed path is primarily recommended for RayService HA rather than automatically for all training jobs. A GCS recovery plan does not replace durable workload checkpoints.

## Security (not optional)

Treat Ray as trusted-code infrastructure. Use controlled networking, separate clusters for mutually untrusted tenants, Kubernetes NetworkPolicy/firewalls, secured ingress/proxy and TLS/VPN/SSH tunnel as appropriate. Do not expose Ray Dashboard, Jobs endpoint or Ray Client publicly without deliberate controls. Never place untrusted user code on the same unrestricted Ray cluster.

Ray releases at/after 2.52 introduced token authentication; verify the exact version and default before enabling it. Tokens are defense-in-depth, **not** a replacement for isolation or encryption. Store token in secret files/manager with restricted permissions; do not commit credentials or log them. Account for token lifecycle/rotation and job submitter access.

## Observability and triage

Collect per-task queue/run time, actor life-cycle/restarts, Ray job status, node CPU/RAM, object-store utilization, heap RSS, spilled/restored bytes, disk free, network TX/RX, pending references, placement-group readiness, worker logs and end-to-end application latency. Use Ray Dashboard, State CLI/API, `ray memory`, metrics/Prometheus where configured, plus application traces with correlation IDs.

Triage in order: (1) errors and head/worker status, (2) pending-resource/placement waits, (3) large live ObjectRefs and spill, (4) oversized task/actor messages and data locality, (5) oversubscribed native thread pools, (6) retries/recovery. A healthy dashboard alone is not correctness evidence.

## Tests and rollout gates

- Unit: pure worker logic, serialization, idempotency and state restore.
- Local Ray: task/actor lifecycle, ref retention, bounded fan-out and backpressure.
- Multi-node: cross-node locality, placement, object transfer, versioned runtime env, checkpoint restore and 99th-percentile latency.
- Fault injection: crash after side effect before ack; actor restart during partial update; head/GCS disruption within documented support; full spill volume; network delay/loss and large job submission bursts.
- Promotion: compare fixed seed/workload and resource cost; define rollback and observe canary workloads before scaling.

Primary docs: [Task fault tolerance](https://docs.ray.io/en/latest/ray-core/fault_tolerance/tasks.html), [Actor fault tolerance](https://docs.ray.io/en/latest/ray-core/fault_tolerance/actors.html), [Runtime environments](https://docs.ray.io/en/latest/ray-core/handling-dependencies.html), [Dashboard](https://docs.ray.io/en/latest/ray-observability/getting-started.html), [KubeRay GCS-FT](https://docs.ray.io/en/latest/cluster/kubernetes/user-guides/kuberay-gcs-ft.html), [Token authentication](https://docs.ray.io/en/latest/ray-security/token-auth.html).
