---
name: gitlab-cicd-devsecops
description: Design, implement, review, and harden GitLab CI/CD delivery systems, including .gitlab-ci.yml, CI/CD Components, runners, protected environments, deployment approvals, GitOps, OIDC, secrets, security scanning, software supply-chain controls, rollback, and production release governance. Use for GitLab CI/CD, GitLab Runner, GitLab Self-Managed/CE delivery, DevOps, DevSecOps, deployment, release engineering, Kubernetes delivery, Flux GitOps, or production pipeline reviews.
metadata:
  category: devops
  version: "1.0.0"
  last_verified: "2026-09-20"
---

# GitLab CI/CD and DevSecOps

## Purpose

Build GitLab delivery systems where source, review, testing, security, artifact creation, deployment, and rollback form one auditable chain.

The default target is:

```text
Merge Request
  -> validation and tests
  -> security checks
  -> merge to protected default branch
  -> build immutable artifact once
  -> staging
  -> verification
  -> controlled production approval
  -> production
  -> health/smoke checks
  -> observability and rollback
```

## Use this skill when

- Creating or refactoring `.gitlab-ci.yml`.
- Designing reusable GitLab CI/CD Components.
- Securing GitLab Runner infrastructure.
- Separating build, test, staging, and production permissions.
- Implementing protected environments or deployment approvals.
- Moving from static cloud keys to GitLab OIDC ID tokens.
- Integrating SAST, secret detection, dependency, container, IaC, DAST, or API security testing.
- Implementing GitOps with GitLab, the Kubernetes agent, and Flux.
- Designing immutable release, rollback, SBOM, signing, or provenance workflows.
- Reviewing a GitLab pipeline for DevSecOps, reliability, or software supply-chain risk.

## Do not use this skill for

- Modifying GitLab Rails, Gitaly, GraphQL, Vue, or GitLab internals: use `gitlab-development`.
- Generic non-GitLab infrastructure design: use `devops-engineer`, `kubernetes-specialist`, or `terraform-engineer`.
- Application code security review unrelated to delivery: pair with `security-reviewer`.

## Core rules

1. **Merge through review.** Production-bound changes flow through Merge Requests and a protected default branch.
2. **Build once, promote the same artifact.** Staging and production must receive the same immutable image/binary digest.
3. **Prefer short-lived identity.** Use GitLab OIDC ID tokens for cloud/Vault federation instead of long-lived access keys when supported.
4. **Isolate runners by trust boundary.** General CI must not implicitly inherit production network or credential access.
5. **Treat pipeline code as privileged code.** Changes to CI, deployment, infrastructure, and signing logic require stronger review.
6. **Make production a protected capability.** Use protected environments, approvals, protected runners, or equivalent controls supported by the GitLab tier.
7. **Fail closed on critical controls.** Tests, required security gates, artifact integrity, migration safety, and deployment verification must block release when required.
8. **Rollback by version, not rebuild.** Keep prior known-good immutable artifacts deployable.
9. **Everything important is reproducible from Git.** Avoid manual production drift and undocumented SSH changes.
10. **Preserve auditability.** A release should answer: who changed it, which commit built it, which pipeline produced it, which digest ran, who approved it, and what verification passed.

## Recommended workflow

1. Identify the GitLab offering/tier and deployment target.
2. Map trust zones: developer/MR, build, security, staging, production, signing.
3. Define branch and Merge Request controls.
4. Define pipeline DAG with `workflow:rules`, `rules`, and `needs`.
5. Build an immutable artifact identified by commit SHA and preferably digest.
6. Add repository, dependency, container, and IaC security controls appropriate to the tier.
7. Deploy the same artifact to staging and run smoke/integration/runtime security checks.
8. Gate production using protected environment/approval controls where available.
9. Authenticate deployment through short-lived identity where possible.
10. Serialize or otherwise guard production deployment concurrency.
11. Verify rollout and business-critical synthetic paths.
12. Keep a tested rollback path and observe post-deployment health.

## Reference routing

| Topic | Reference | Load when |
|---|---|---|
| Pipeline architecture | `references/pipeline-design.md` | Designing jobs, DAGs, components, artifacts, rules, caches |
| Runner security | `references/runner-security.md` | Runner pools, Docker/DinD, shell executor, network isolation |
| Deployment and GitOps | `references/deployment-gitops.md` | Environments, Kubernetes, Flux, rollout, migrations, rollback |
| DevSecOps and supply chain | `references/security-supply-chain.md` | OIDC, secrets, scanners, policies, SBOM, signing |
| Production baseline | `references/production-checklist.md` | Audits, readiness reviews, FinTech/Web3 hardening |

## Expected output

For implementation tasks, provide:

- pipeline architecture and trust boundaries;
- concrete `.gitlab-ci.yml` or CI/CD Component snippets;
- runner requirements and tags;
- secrets/identity model;
- staging and production deployment strategy;
- security gates and severity policy;
- rollback and post-deploy verification;
- tier-dependent notes when a GitLab feature is not universally available.

## Tier-aware behavior

Never assume every GitLab feature is available in every tier.

Current verified examples as of 2026-09-20:

- CI/CD Components and OIDC ID tokens are available across Free, Premium, and Ultimate.
- Deployment approvals for protected environments are Premium/Ultimate.
- Merge request approval policies for security/compliance are Ultimate.
- Individual application-security features have different tier requirements; verify the current feature page before promising availability.

When a paid feature is unavailable, preserve the control objective with a simpler mechanism: manual protected deploy jobs, separate deployment projects, CODEOWNERS/review convention, external scanners, or policy checks in CI.

## Anti-patterns

Avoid:

- `:latest` in production.
- Rebuilding a release after staging verification.
- Shared shell runners for untrusted projects.
- Privileged Docker-in-Docker on a broadly shared runner.
- Long-lived cloud-admin credentials in CI variables.
- Production database or cluster-admin access on general build runners.
- Direct push to the production branch as a deployment mechanism.
- Editing production manually over SSH without reconciling Git.
- Deleting a leaked secret without revoking/rotating it.
- Security scans that can be silently removed from a Merge Request without compensating governance.
- Rollback procedures that depend on rebuilding old source.
- Two production deployments mutating the same target concurrently without serialization or progressive-delivery coordination.

## Pair with

- `devops-engineer` for broader infrastructure and platform engineering.
- `kubernetes-specialist` for workload, networking, Helm, and cluster design.
- `terraform-engineer` for IaC implementation.
- `security-reviewer` for threat modeling and vulnerability review.
- `gitlab-development` when changing GitLab itself rather than using GitLab as the delivery platform.

## Authoritative references

- https://docs.gitlab.com/ci/
- https://docs.gitlab.com/ci/components/
- https://docs.gitlab.com/runner/security/
- https://docs.gitlab.com/ci/environments/
- https://docs.gitlab.com/ci/environments/deployment_approvals/
- https://docs.gitlab.com/ci/secrets/id_token_authentication/
- https://docs.gitlab.com/ci/cloud_services/
- https://docs.gitlab.com/user/application_security/detect/
- https://docs.gitlab.com/user/application_security/policies/
- https://docs.gitlab.com/user/clusters/agent/gitops/
