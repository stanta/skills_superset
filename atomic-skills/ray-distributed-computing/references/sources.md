# Authoritative sources and verification notes

Read the docs for the **installed** release before copying API signatures. These links were reviewed while assembling this skill in September 2026; Ray `latest` may change. This is an engineering synthesis, not a claim of benchmark results or of unverified functionality.

## Ray Core

- [Actors](https://docs.ray.io/en/latest/ray-core/actors.html)
- [Distributed objects / ObjectRefs](https://docs.ray.io/en/latest/ray-core/objects.html)
- [Scheduling resources and logical CPU semantics](https://docs.ray.io/en/latest/ray-core/scheduling/resources.html)
- [Placement groups](https://docs.ray.io/en/latest/ray-core/scheduling/placement-group.html)
- [Actor fault tolerance](https://docs.ray.io/en/latest/ray-core/fault_tolerance/actors.html)
- [Task fault tolerance](https://docs.ray.io/en/latest/ray-core/fault_tolerance/tasks.html)
- [Avoid `ray.get` in submission loops](https://docs.ray.io/en/latest/ray-core/patterns/ray-get-loop.html)
- [Bound result fetching](https://docs.ray.io/en/latest/ray-core/patterns/ray-get-too-many-objects.html)
- [Object spilling](https://docs.ray.io/en/latest/ray-core/objects/object-spilling.html)
- [Environment dependencies](https://docs.ray.io/en/latest/ray-core/handling-dependencies.html)
- [Bounded unordered map](https://docs.ray.io/en/latest/ray-core/api/doc/ray.util.map_unordered.html)

## ML, operations and security

- [Ray Train PyTorch guide](https://docs.ray.io/en/latest/train/getting-started-pytorch.html)
- [Ray Train checkpointing](https://docs.ray.io/en/latest/train/user-guides/checkpoints.html)
- [Ray Train persistent storage](https://docs.ray.io/en/latest/train/user-guides/persistent-storage.html)
- [Ray Serve production](https://docs.ray.io/en/latest/serve/production-guide/best-practices.html)
- [Ray Serve autoscaling](https://docs.ray.io/en/latest/serve/autoscaling-guide.html)
- [Ray Dashboard](https://docs.ray.io/en/latest/ray-observability/getting-started.html)
- [KubeRay GCS-FT](https://docs.ray.io/en/latest/cluster/kubernetes/user-guides/kuberay-gcs-ft.html)
- [Ray token authentication](https://docs.ray.io/en/latest/ray-security/token-auth.html)

## Boundaries of evidence

Source documentation establishes Ray's advertised API, intended semantics and caveats. Claims about DANMA scalability, batching advantage, local-gradient convergence, per-event trace cost, and Ray versus direct-Rust network performance are **hypotheses** until measured. Keep benchmark configuration, failures and negative results alongside any performance claim.
