---
name: openshift-operations
description: Use for OpenShift Container Platform operations, oc workflows, namespaces/projects, Routes, Operators/OLM, SCC admission, image compatibility, cluster upgrades and OpenShift-specific Helm/GitOps deployment troubleshooting.
---

# OpenShift operations

Apply this skill when a task specifically concerns Red Hat OpenShift rather than generic Kubernetes. Combine with `kubernetes-specialist` for common workload architecture and `helm-release-engineering` for charts.

## Discover before changing

1. Identify OpenShift version, cluster type (managed/self-managed), operator ownership, namespace/project, RBAC scope and maintenance window. Never assume cluster-admin.
2. Read-only baseline: `oc whoami`, `oc config current-context`, `oc version`, `oc get clusterversion`, `oc get co`, `oc get nodes`, `oc get events -n <project> --sort-by=.lastTimestamp`.
3. Classify operation as application-level, operator-managed, cluster-wide or control-plane change. For production changes provide risk, backup/restore path, rollback and explicit approval. Prefer GitOps-managed manifests to ad-hoc edits.

## OpenShift application deployment

- Use `oc project <name>` only after confirming current context and intended destination. Prefer dedicated service accounts and namespace RBAC. Keep infrastructure and application privileges separate.
- Use Deployment/Service/Route when an OpenShift Route is appropriate; configure TLS termination and redirect policy deliberately, with certificate ownership documented. Prefer Ingress if portability or existing ingress controllers require it.
- Check image pull credentials, image architecture, registry trust, storage class, quotas and LimitRanges before rollout.
- Make container images arbitrary-UID compatible: writable application directories must support the namespace-assigned UID (commonly group-writable group 0), avoid privileged ports, never require fixed `runAsUser: 1000` or root unless policy explicitly allows it.
- Start with the namespace's default restricted policy. `restricted-v2` commonly assigns UID from project range, drops ALL capabilities and disallows privilege escalation; verify actual SCC and version rather than assuming admission behavior. Avoid granting `anyuid` or `privileged` as a workaround. If an exception is unavoidable, use a reviewed narrowly scoped custom SCC bound only to a dedicated service account.
- Keep RBAC, Kubernetes Pod Security admission and OpenShift SCC conceptually distinct. An SCC is an OpenShift admission mechanism, not a substitute for namespace RBAC or network policies.
- Operators own their managed resources: use supported CRs/OLM channels and approved upgrade paths rather than patching reconciled Deployments.

## Helm charts in OpenShift

1. Check chart securityContext, init containers, permissions, volume ownership, capabilities, hooks and route/ingress support; test under restricted-v2 with a fresh project.
2. Avoid hardcoded UID/GID/fsGroup or manual SELinux labels when OpenShift should allocate them; verify actual security policies.
3. `helm lint`; `helm template` with environment-specific values; policy-check the rendered resources; `oc apply --dry-run=server -f <rendered-file>` where permitted.
4. Deploy by approved CI/GitOps pipeline; inspect `oc describe pod`, events and SCC admission errors before considering policy changes. Chart installation does not grant permission to bypass SCC.

## Cluster operations and upgrades

- Before changing cluster configuration, examine ClusterOperators, MachineConfigPools, node conditions, upgrade compatibility, backup state and disruption budgets. Follow vendor's version-specific upgrade path and etcd backup procedure.
- Validate operators and application SLOs after change. Distinguish application rollback (Helm/GitOps) from cluster-version rollback; do not promise unsupported cluster downgrades.

## Incident workflow

`oc get pods -n <project> -o wide` → `oc describe pod <pod> -n <project>` → `oc logs <pod> -n <project> --previous` → inspect events, probes, quotas, SCC, image pulls, Routes, Services, endpoints, DNS, NetworkPolicy and PVC state. Document evidence and root cause before remediation. Do not restart or delete failing production pods merely to clear symptoms.

## Acceptance checks

- Correct cluster/context/project and least-privilege identity verified.
- SCC admission succeeds without overprivileged exception; Routes/TLS, connectivity and NetworkPolicy verified.
- Readiness, rollout, logs, metrics, alerts and rollback/restore tested; GitOps state matches live resources.

## Authoritative references

- Red Hat OpenShift documentation (select the cluster's version): https://docs.redhat.com/en/documentation/openshift_container_platform/
- SCC guidance: https://docs.redhat.com/en/documentation/openshift_container_platform/4.22/html/authentication_and_authorization/managing-pod-security-policies
- Kubernetes application security checklist: https://kubernetes.io/docs/concepts/security/application-security-checklist/
