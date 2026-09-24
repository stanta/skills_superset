# GitLab Production Delivery Checklist

Use this as a release-platform audit.

## Source and review

- [ ] Default production-bound branch is protected.
- [ ] Direct push is disabled or tightly restricted.
- [ ] Merge Requests require appropriate review.
- [ ] CI/deployment/IaC changes have stronger ownership/review.
- [ ] Pipeline success is required before merge where appropriate.

## Pipeline

- [ ] Pipeline uses `workflow:rules`/job `rules` to avoid waste and duplication.
- [ ] `needs` expresses true DAG dependencies.
- [ ] Cache is not used as a substitute for release artifacts.
- [ ] Tests and security jobs produce machine-readable reports where useful.
- [ ] Reusable CI is versioned and pinned appropriately.

## Artifact integrity

- [ ] Production never deploys `:latest`.
- [ ] Artifact is traceable to exact commit/pipeline.
- [ ] Staging and production use the same immutable digest.
- [ ] SBOM is generated for critical artifacts.
- [ ] Signing/provenance is used for high-assurance workloads.
- [ ] Previous known-good artifact is retained for rollback.

## Runners

- [ ] General CI runner has no implicit production access.
- [ ] Shell executor is limited to trusted use.
- [ ] Privileged jobs are isolated and preferably ephemeral.
- [ ] Production deploy runner is protected/dedicated.
- [ ] Runner networks are segmented from sensitive control planes.
- [ ] Persistent caches/workspaces do not cross trust boundaries.

## Identity and secrets

- [ ] Secrets are stored outside Git.
- [ ] Long-lived cloud keys are replaced with OIDC/federation where possible.
- [ ] OIDC policies restrict project/ref/audience.
- [ ] `CI_JOB_TOKEN` trust is allowlisted/minimized.
- [ ] Production deploy identity uses least privilege.
- [ ] Signing keys are not present on general runners.

## Security

- [ ] Secret detection is enabled.
- [ ] SAST/dependency/IaC/container scans are enabled where relevant and available.
- [ ] Runtime DAST/API tests run against safe staging targets when appropriate.
- [ ] Critical findings have a defined release gate.
- [ ] Security exceptions have owner, reason, expiry, and audit trail.
- [ ] Security controls cannot be trivially removed without review.

## Deployment

- [ ] Staging exists for production-critical services.
- [ ] Staging uses production-like deployment mechanics.
- [ ] Production is protected by explicit authorization/approval.
- [ ] Concurrent deployments cannot corrupt the same target.
- [ ] Outdated pipeline jobs cannot overwrite newer deployments.
- [ ] Deployment waits for rollout readiness.
- [ ] Smoke/business synthetic tests run after rollout.
- [ ] Freeze windows exist for unusually sensitive periods if needed.

## Database and compatibility

- [ ] Migrations are backward compatible when rolling deployment/rollback requires it.
- [ ] Destructive schema removal is delayed until old code no longer depends on it.
- [ ] Rollback effect on schema/data is documented and tested.

## Observability and recovery

- [ ] Health/readiness endpoints exist.
- [ ] Logs, metrics, traces, and deployment metadata correlate to release version.
- [ ] Alerting covers user-impacting failure, not only infrastructure.
- [ ] Rollback procedure is documented and exercised.
- [ ] RPO/RTO are defined for stateful critical services.
- [ ] Restore tests are performed, not just backups.

## FinTech/Web3 additions

- [ ] CI never receives wallet mnemonic/master custody keys.
- [ ] Signing uses dedicated service/KMS/HSM where feasible.
- [ ] Payment callback signatures are verified.
- [ ] Webhook/retry behavior is idempotent.
- [ ] Duplicate message tests exist.
- [ ] Reconciliation is independently verifiable.
- [ ] Chain confirmation/finality assumptions are explicit.
- [ ] Hot-wallet/payment limits and blast-radius controls exist.

## Metrics

Track delivery-system health:

- deployment frequency;
- lead time;
- change failure rate;
- time to restore;
- pipeline duration;
- runner queue time;
- pipeline success rate;
- flaky test rate;
- deployment duration;
- rollback count.

## Maturity guide

### Level 1
CI, tests, reproducible container build.

### Level 2
Protected branch, Merge Requests, staging, registry, automated deploy.

### Level 3
Security scanning, isolated runners, short-lived identity, IaC.

### Level 4
GitOps, protected production, deployment approvals/policy controls, SBOM, signing, reliable rollback and observability.

### Level 5
Policy-as-code, supply-chain verification, progressive delivery, SLO-driven release automation, automated compliance evidence.

For FinTech/Web3 transaction systems, target Level 4 as a practical baseline and add Level 5 controls according to custody, regulatory, and financial risk.
