---
name: github-actions-devsecops
description: Use when creating, reviewing, debugging, or hardening GitHub Actions workflows, CI checks, release pipelines, runners, build provenance, dependency scanning, or cloud deployments from GitHub.
metadata:
  category: devops
  last_verified: "2026-09-27"
---

# GitHub Actions CI/CD and Supply-Chain Security

## Model the trust boundaries

Inspect actual workflow events, repository visibility, fork policy, runner type, job permissions, environment protections, secrets, caches, artifacts and required branch checks *before* editing YAML. Treat PR titles, comments, branch names, checkout contents, actions, dependencies and downloaded artifacts as untrusted input. Use the repository's existing tools; do not install or authorize apps without the operator's permission.

## CI pipeline design

- Run fast formatting/lint/unit checks for every eligible PR, then integration/security/compatibility checks according to risk. Give each required check a stable, unique name across workflows.
- Prefer explicit, deterministic dependencies/toolchains, reproducible builds, lockfiles, caches keyed by content and correctly scoped. Cache is an optimization, never a trust boundary or substitute for a clean build.
- Use path filters carefully: a required status must still be reported for every merge-eligible change. If using merge queue, include the `merge_group` event for required Actions checks.
- Split untrusted PR validation, trusted packaging and privileged deployment into separate jobs/workflows with explicit artifact handoff and provenance verification.
- Limit concurrency/cancel stale runs where appropriate; apply timeouts and sensible retry policy. Avoid cancelling production jobs mid-migration.
- Prefer environment-specific deployment jobs, release commit/tag verification, smoke tests, rollback instructions and human approval for production.

## Minimum permissions and untrusted contributions

1. Set workflow-level `permissions: { contents: read }` or `permissions: {}`, then grant only required job-level scopes. Explicitly review `GITHUB_TOKEN` capabilities and third-party app tokens.
2. Use `pull_request` for ordinary fork PR CI without deployment credentials. Do **not** give untrusted PR code access to secrets, write-scoped tokens, production networks or persistent privileged runners.
3. Avoid `pull_request_target` when building/testing PR code. If necessary for labeling/triage, do not check out or execute the PR head in the privileged context. Review GitHub's current event protections and avoid interpolating attacker-controlled expressions in a shell script; pass data via quoted environment variables and validate it.
4. Pin third-party actions/reusable workflows to reviewed **full commit SHAs** where supported and maintain updates deliberately. Audit transitive scripts/container images; tags alone can move. Use minimal checkout credentials and prefer `persist-credentials: false` when later steps do not need Git writes.
5. Isolate ephemeral or rigorously cleaned runners; do not run untrusted fork code on a self-hosted runner with repository/cloud access. Treat caches and artifacts crossing trust levels as untrusted.
6. Avoid echoing secrets or placing them in CLI arguments/artifacts/logs. Enable secret scanning/push protection where available; rotate on exposure.

## Deployments and provenance

- Prefer cloud OIDC federation over long-lived cloud keys. Give `id-token: write` **only** to the job that needs it, and restrict the provider trust policy by repository, ref, workflow/environment and audience where supported.
- Protect GitHub environments with reviewers and branch/tag restrictions where the plan supports them; keep production credentials out of PR-triggered jobs.
- Promote an immutable, verified build artifact rather than rebuilding from a mutable branch for each environment. Use artifact attestations/signing and digest verification where supported; document limits of guarantees.
- Gate merges on tests and security scans; triage false positives with documented ownership and expiry, not blanket disables. Keep Dependabot/security-update PRs subject to the same safe review path.
- For workflows that publish packages or releases, constrain package registry permissions, verify release tags and grant publishing tokens only for the publish job.

## Minimal unprivileged PR skeleton

```yaml
name: CI
on:
  pull_request:
  merge_group: # retain if a configured merge queue needs this check
permissions:
  contents: read
jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@<reviewed-full-commit-sha>
        with:
          persist-credentials: false
      - name: Run repository checks
        run: ./scripts/ci-checks.sh
```

This is a pattern, not a paste-ready workflow: replace the SHA and check command with verified project values; remove `merge_group` unless applicable. Never invent a pinned SHA.

## Review gates

Check the effective permissions for **each event and job**, confirm untrusted input cannot reach privileged code execution, inspect action provenance, verify required status names/trigger coverage, validate workflow syntax with repository CI, and test the failure/rollback path. Report which controls were actually configured versus merely recommended.

## Primary references

- [GitHub Actions security](https://docs.github.com/en/actions/how-tos/secure-your-work) and [secure use of pull_request_target](https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target).
- [GitHub OIDC cloud providers](https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-cloud-providers).
- [GitHub merge queue](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue).
- [GitHub security features](https://docs.github.com/en/code-security/tutorials/secure-your-organization/protect-against-threats).
