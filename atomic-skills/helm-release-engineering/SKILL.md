---
name: helm-release-engineering
description: Use to build, review, test, package, secure, publish and upgrade Helm charts; manage chart dependencies, CRDs, values schemas, Helm rollback, OCI registries and GitOps integration on Kubernetes/OpenShift.
---

# Helm release engineering

Use alongside `kubernetes-specialist` or `openshift-operations` when the cluster requires platform-specific controls.

## Preflight

Identify Helm major/minor, cluster APIs, namespaces, chart provenance, owning GitOps controller, release history, current and target chart/app versions. Check `helm version`, `helm list -n <ns>`, `helm history <release> -n <ns>`; confirm kube context before any mutating command. Do not run Helm directly against a release owned by Argo CD/Flux unless documented break-glass procedure permits it.

## Chart design

- Keep `Chart.yaml`, `values.yaml`, `values.schema.json`, `templates/`, `charts/` and README coherent. Use semantic chart versions and separate application versions; pin dependency versions and images by immutable digest where feasible.
- Build deterministic, idempotent templates; stable names/selectors; standard Helm/Kubernetes labels; explicit selectors and API versions compatible with supported clusters. Do not derive selectors from changing chart versions.
- Validate required inputs with JSON Schema or `required`; set safe defaults. Do not put credentials or real secret values in chart defaults or command-line `--set` (exposes shell history/process arguments). Use approved secret managers such as External Secrets or SOPS with a reviewed controller.
- Model service accounts, bounded RBAC, resources, probes, security contexts, disruption budgets, topology, NetworkPolicies and configurable ingress/route according to workload requirements. Do not force CPU limits indiscriminately; size requests/limits from measurements and policy.
- CRDs in `crds/` are handled differently from templates and are not automatically upgraded/deleted with ordinary chart lifecycle. Plan CRD install/migration/rollback separately and back up custom resources.
- Use hooks only for operations that require them; jobs must be idempotent, timeout-bounded and have cleanup policy; database/schema migrations need forward/backward compatibility and separate rollback strategy.

## CI gate before deployment

```bash
helm dependency build ./chart
helm lint ./chart --strict -f values/staging.yaml
helm template my-app ./chart --namespace staging -f values/staging.yaml > rendered.yaml
kubectl apply --dry-run=server --namespace staging -f rendered.yaml
```

Check output for invalid APIs, security policy violations, unbounded resources, secret leakage, namespace collisions and unexpected cluster-scoped RBAC. Use chart unit tests and integration tests in an ephemeral cluster; test both upgrade and rollback paths. Server-side dry run requires a suitable connected cluster and permissions and may not fully simulate controllers or hooks.

## Controlled release

- Deploy through CI/GitOps with reviewed values; pin artifact/chart digest and record release metadata.
- For direct Helm releases, use version-supported rollback-on-failure semantics and `--wait`, an explicit timeout, and `--history-max`. Confirm your installed Helm CLI flags (Helm 3 vs 4 differ); do not blindly copy `--atomic`/`--rollback-on-failure` between versions.
- Confirm Deployment rollout, workload probes, metrics, traffic, migrations and smoke tests. Use `helm history`, `helm status`, `helm get manifest` and `helm get values` for incident evidence, but avoid exposing secret material in output.
- `helm rollback` restores release-managed resource manifests, not external data, CRDs or database migrations. Define application/data recovery explicitly.

## OpenShift compatibility

Do not hardcode runtime UID/GID in generic templates. Offer an OpenShift-compatible profile tested against namespace SCC; avoid blanket `anyuid` grants and unsafe fsGroup assumptions. Validate route support only when required.

## Reference links

- Official chart best practices: https://docs.helm.sh/docs/chart_best_practices/
- Upgrade command/version-specific flags: https://docs.helm.sh/docs/helm/helm_upgrade/
- Kubernetes application security: https://kubernetes.io/docs/concepts/security/application-security-checklist/
