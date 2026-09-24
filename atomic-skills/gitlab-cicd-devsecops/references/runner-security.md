# GitLab Runner Security

## Runner is a trust boundary

A GitLab job executes user-controlled code. Treat runner placement, executor choice, network access, credentials, caches, and mounted sockets as security architecture.

## Executor guidance

### Shell executor

GitLab documents high security risk for shell executors because jobs execute directly on the runner host with the runner user's permissions and can access host/network state.

Use shell only for:

- trusted repositories;
- trusted users;
- dedicated hosts;
- narrowly scoped operational jobs.

Do not use a broadly shared shell runner for untrusted Merge Requests.

### Docker executor

Prefer non-privileged containers.

Hardening options include:

- non-root job user;
- reduced Linux capabilities;
- no host PID namespace;
- no unnecessary host mounts;
- no Docker socket mount unless explicitly accepted as a privileged trust boundary.

### Privileged Docker / Docker-in-Docker

Privileged mode can effectively disable container isolation and enable host compromise.

If privileged build is unavoidable:

- dedicate the runner to that purpose;
- allow only trusted/protected refs;
- run on isolated ephemeral machines;
- avoid production credentials;
- destroy the instance after use;
- keep the runner network away from sensitive control planes.

Prefer rootless BuildKit, Buildah, Podman, or a remote build service when they meet requirements.

## Runner pools

Recommended separation:

```text
general-build
  - no production network
  - no production secrets

security-scan
  - scanner tooling
  - limited write permissions

integration
  - isolated service dependencies

production-deploy
  - protected
  - narrowly scoped production access

signing
  - strongest isolation
  - dedicated identity/HSM/KMS integration
```

Use tags to make job intent explicit and ensure project settings prevent arbitrary workloads from reaching protected runner pools.

## Ephemeral execution

Prefer one job per disposable VM/pod for high-risk workloads.

GitLab Docker Autoscaler supports one-job-per-instance patterns. Ephemeral instances reduce cross-job persistence and simplify cleanup after privileged builds.

## Network segmentation

General runners should not be able to reach:

- production databases;
- Vault root/admin endpoints;
- cluster-admin Kubernetes APIs;
- hypervisor/control-plane management networks;
- signing/HSM management interfaces.

Use firewall/security-group rules in addition to GitLab-level permissions.

## Credentials

Do not preload general runner hosts with broad cloud credentials.

Prefer:

- GitLab OIDC ID token;
- cloud workload identity/federation;
- Vault-issued short-lived credentials;
- scoped `CI_JOB_TOKEN` for GitLab-to-GitLab access.

Bind identity policies to stable project/group identifiers and protected refs where possible.

## Cache and workspace hygiene

Assume a compromised job will inspect everything reachable.

- Avoid cross-project writable caches containing sensitive content.
- Do not cache secret files.
- Do not share persistent workspaces across trust zones.
- Clear credentials and temporary signing material.
- Use explicit artifact boundaries between jobs.

## Production deployment runner

A production deploy runner should normally be:

- protected;
- isolated from general CI;
- restricted to production deployment jobs;
- authenticated with short-lived credentials;
- least-privileged in Kubernetes/cloud;
- monitored and audited.

It should not also run arbitrary lint/test jobs.

## Runner review checklist

- What code can schedule jobs here?
- Can fork/MR code reach this runner?
- Is the executor isolated from the host?
- Is privileged mode enabled?
- Is Docker socket mounted?
- Is the runner persistent or ephemeral?
- What network ranges can it reach?
- What cloud/Kubernetes identity does it have?
- What secrets can jobs request?
- Can one project observe another project's cache/workspace?
- Are production and signing workloads physically/logically separated?
