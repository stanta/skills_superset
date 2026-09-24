# Harness Security Boundaries

## Principle

The harness, permission broker, or tool gateway must enforce security independently of model compliance. A fully prompt-injected model must still be unable to exceed its capability envelope.

## Recommended control plane

User / untrusted content -> Agent -> Intent/policy check -> Permission broker -> Parameter validation -> Tool -> Side-effect audit log

## Required invariants

### Filesystem

- Default deny outside the task workspace.
- Never expose SSH keys, cloud config, browser profiles, password stores, wallet seeds, kubeconfig, signing keys, or unrelated user files to ordinary skills.
- Use separate read and write roots.
- Resolve symlinks and reject paths escaping approved roots.
- Prefer read-only mounts for source under review.

### Network

- Deny outbound network by default for untrusted execution.
- Allowlist destinations by hostname/service when network is required.
- Block cloud metadata and link-local targets.
- Block localhost/internal-service access unless explicitly needed.
- Log destination, protocol, bytes, and calling skill/tool.

### Shell and process execution

- Prefer command allowlists over arbitrary shell.
- Reject shell metacharacter composition when a structured subprocess API is possible.
- Limit child-process count, CPU, memory, wall time, file descriptors, and output size.
- Do not mount the Docker socket into untrusted execution environments.

### Credentials

- Inject no production secrets into untrusted admission jobs.
- Prefer short-lived, audience-bound, least-privilege tokens.
- Bind credentials to the operation and resource when possible.
- Use canary secrets during red-team execution to detect attempted access or exfiltration.

### High-impact actions

Require a fresh, parameter-bound approval for:

- deployments and infrastructure mutation;
- git push/merge/release publication;
- messages or posts sent externally;
- purchases, payments, transfers, trades, or wallet signing;
- account/permission changes;
- deletion or destructive migrations;
- credential creation/rotation/revocation.

Approval should name the exact action, target, and material parameters. Do not treat generic prior consent as authorization for changed parameters.

### Memory and persistence

- Separate memory per user, tenant, and trust domain.
- Sanitize before persistence.
- Set size and TTL limits.
- Do not persist instructions from untrusted sources as policy.
- Audit modifications to agent rule files, prompt files, MCP configuration, shell startup files, scheduled jobs, and git hooks.

### Tool/MCP integrity

- Maintain an allowlist of approved tool providers.
- Snapshot tool names/descriptions/schemas and detect changes.
- Reject duplicate/shadowed privileged tool names.
- Validate every tool argument against session/user permissions.
- Treat tool descriptions and return values as untrusted content, not policy.

## Skill risk tiers

- S0 Declarative: documentation only; no execution, write, or network capability.
- S1 Read-only: scoped repository/workspace reads; no secrets and no external writes.
- S2 Operational: scoped writes, test execution, approved package operations, or narrow external API access.
- S3 Privileged: deploy, publish, administer, sign, pay, message, or access sensitive systems. Requires strict human approval and stronger isolation.

The declared tier does not grant permissions. It only communicates intended risk; harness policy remains authoritative.
