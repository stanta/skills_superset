---
name: lens-kubernetes-ide
description: Use to configure and operate Lens Kubernetes IDE safely for cluster discovery, kubeconfig contexts, read-only diagnostics, pod logs, metrics, terminal access, port forwarding, RBAC-aware collaboration and incident investigation.
---

# Lens Kubernetes IDE operations

Lens is an interactive Kubernetes operator workstation, not a source of truth or a substitute for GitOps, CI checks or RBAC. Use `kubernetes-specialist` for manifest remediation and `openshift-operations` for OpenShift SCC/Routes.

## Safe connection

1. Confirm the intended cluster/environment/context, namespace, identity and access scope outside and inside Lens. Clearly distinguish staging from production.
2. Import a minimally privileged, short-lived kubeconfig from an approved identity provider; never paste tokens/certificates into chat, tickets, screenshots, repos or personal cloud sync. Prefer federated authentication and automatic expiry/rotation.
3. Protect the workstation and kubeconfig with OS permissions, disk encryption and screen locking. Audit Lens extensions and integrations before installation and apply organization policies for telemetry, credentials and team sharing.
4. Treat dashboards and displayed RBAC as clues, not authorization. Verify actual access through Kubernetes API. Do not use a shared cluster-admin kubeconfig for routine browsing.

## Read-only diagnostic workflow

- Select cluster and namespace explicitly; inspect nodes, workloads, deployment replicas, pod phase/restarts, events, container logs (including previous crash), CPU/memory metrics, service endpoints and ingress/route path.
- Correlate logs, events, probes and rollout revisions. If metrics are absent, check metrics-server/Prometheus permissions and plumbing rather than assuming zero usage.
- Record incident timeline, namespace, object UID, image digest, deployment revision and relevant redacted events. Verify findings with `kubectl`/`oc` if the Lens UI is stale or ambiguous.

## Controlled interactive tools

- Lens terminal inherits cluster/context risk: display and recheck context before commands. Prefer read-only inspection by default. For production mutations use peer review, maintenance window, approved GitOps/CI workflow and change record.
- Port forwarding bypasses normal public ingress/route exposure and can expose internal admin interfaces on the operator workstation. Bind to loopback, use least privilege, do not share forwarded endpoints, stop sessions after diagnosis, and inspect port-forward RBAC.
- For exec/shell/debug sessions, avoid production data dumps and secret printing. Prefer ephemeral diagnostic containers only if policy and permissions allow, with an audit trail.
- Do not edit live workload YAML in Lens if GitOps owns the resource: it will drift and may be overwritten. Make changes in the repository and observe reconciliation.

## Troubleshooting checklist

Wrong cluster or credentials → kubeconfig/context/auth expiry; empty namespace → filter/RBAC; unknown metrics → metrics API/permissions; pending pod → scheduling/quota/PVC; crashloop → previous logs/probes/config; service unavailable → endpoints/network policy/DNS/TLS; OpenShift rejection → SCC and assigned UID, not a request for privileged access.

## Completion

Provide diagnosis, evidence, minimal corrective change location (repo/PR or approved emergency action), owner and post-change verification. Remove temporary port forwards and revoke temporary credentials if issued.

## Official references

- Lens docs: https://docs.lenshq.io/k8slens/
- Adding clusters: https://docs.lenshq.io/k8slens/getting-started/
- Port forwarding: https://docs.lenshq.io/k8slens/cluster/use-port-forwarding/
- Kubernetes security checklist: https://kubernetes.io/docs/concepts/security/security-checklist/
