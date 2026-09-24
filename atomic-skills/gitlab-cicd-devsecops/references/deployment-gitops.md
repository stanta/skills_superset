# GitLab Deployment and GitOps

## Environments

Represent deployment targets as GitLab Environments, for example:

```text
review/*
development
staging
production
```

Use `deployment_tier` where appropriate.

Keep production credentials and permissions separate from staging.

## Staging parity

Staging should use the same delivery mechanism and immutable artifact as production.

Keep equivalent:

- image/binary;
- Helm/Kubernetes manifests or deployment templates;
- ingress/service model;
- secret retrieval pattern;
- observability;
- migration process.

Scale, credentials, external integrations, and data can differ.

## Protected production

Where supported, protect the production environment and restrict who may deploy.

GitLab deployment approvals are Premium/Ultimate and can require additional approval before deployment to a protected environment.

Even without that feature, preserve the control objective with:

- protected branch/tag;
- protected runner;
- manual non-optional production job;
- separate deployment project;
- explicit reviewer/owner process.

## GitOps

For Kubernetes, prefer pull-based GitOps for mature production environments.

GitLab currently recommends using both Flux and the GitLab Kubernetes agent (`agentk`) for GitOps workflows.

A strong pattern:

```text
application repo
  -> CI builds immutable OCI artifact
  -> deployment repo change updates digest
  -> review/merge
  -> Flux reconciles cluster
  -> GitLab agent provides GitLab/cluster integration and visibility
```

Git is desired state; the cluster is actual state.

Avoid letting both CI `kubectl apply` and Flux independently own the same objects.

## Deployment serialization and stale jobs

Use `resource_group` for simple single-target deployment serialization.

Also ensure an older pipeline cannot complete after a newer pipeline and revert the target unintentionally.

## Rollout verification

A deployment is not complete when `kubectl apply` returns zero.

Verify:

1. rollout completion;
2. readiness/health;
3. smoke tests;
4. critical dependency connectivity;
5. one or more business-critical synthetic paths;
6. error/latency/restart metrics.

## Zero-downtime application behavior

Design workloads for:

- readiness probes;
- liveness/startup probes as appropriate;
- graceful shutdown;
- connection draining;
- rolling updates;
- sufficient replicas/PDBs;
- backward-compatible schema transitions.

For high-risk services, consider canary or blue/green rollout.

## Database migrations

Prefer expand -> migrate -> contract.

Example:

1. add new schema in a backward-compatible way;
2. deploy code that can use old and new forms;
3. backfill/migrate data;
4. switch reads/writes;
5. remove old schema in a later release.

Do not make rollback impossible with an immediate destructive migration.

## Rollback

Rollback by known-good immutable version:

```text
current digest -> previous known-good digest
```

For GitOps, use a reviewed revert or version update and let Flux reconcile.

Do not rebuild an old commit and assume the result is identical.

## Deployment freeze

Use freeze windows for events where change risk exceeds benefit, such as:

- financial close;
- high-value launch;
- major marketing event;
- migration/failover window;
- holiday staffing constraints.

Freeze is risk management, not a substitute for reliable delivery.

## Observability after deployment

Track both technical and business health.

Technical:

- error rate;
- latency;
- restarts;
- saturation;
- DB latency;
- queue lag;
- dependency errors.

Business examples for payment systems:

- orders/minute;
- payment success rate;
- webhook lag;
- reconciliation mismatch rate;
- blockchain confirmation delay.

## DORA-oriented feedback

Measure:

- deployment frequency;
- lead time for changes;
- change failure rate;
- time to restore service.

Use metrics to improve the system, not to rank individual developers.
