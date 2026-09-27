---
name: github-pull-request-workflows
description: Use when contributing to or administering GitHub repositories through issues, branches, pull requests, reviews, protected branches, CODEOWNERS, merge policies, or releases.
metadata:
  category: development
  last_verified: "2026-09-27"
---

# GitHub Collaboration and Repository Governance

## Scope

GitHub adds identity, authorization, policy and CI to Git. First inspect repository permissions, default branch, CONTRIBUTING, PR template, CODEOWNERS, rulesets, existing checks and open PRs. Follow the target project's established conventions rather than assuming access or globally changing settings. Use [git-core-workflows](../git-core-workflows/SKILL.md) for local Git, [git-history-recovery](../git-history-recovery/SKILL.md) for undo, and [github-actions-devsecops](../github-actions-devsecops/SKILL.md) for CI security.

## From issue to merge

1. Clarify the issue, acceptance criteria, owner and linked evidence; check for duplicate issues/PRs. For code, agree on tests and operational rollback before implementation.
2. Fork if direct push is unavailable or inappropriate; otherwise create a small task branch. Sync from verified upstream and avoid touching unrelated work.
3. Open a **draft PR** early when collaboration or design feedback will reduce rework. Target the intended base, use a descriptive title, link issues, describe *why* and *what*, document tests, risk, screenshots where useful, and rollout/rollback when relevant.
4. Keep the diff narrowly scoped. Resolve threads with explanations and verified updates. Request relevant maintainers or CODEOWNERS; do not self-approve as a substitute for independent review.
5. Convert to ready only when implementation, documentation, tests and security impact have been checked. Re-run checks after conflicts, base updates and review-driven changes; stale approvals may need re-approval under rules.
6. Merge only with required reviews, required checks, conversations resolved, intended branch and permission verified. Choose squash, merge commit or rebase-merge to match repository history policy. Delete the feature branch only after merge and after confirming no active worktree/dependent PR needs it.

## Review discipline

Review actual diffs **and** their context, focusing on correctness, security, compatibility, migration, test quality and operational effects. Give actionable feedback tied to lines and impact; distinguish blockers from optional improvements. For sensitive files, request the relevant domain owner. Avoid treating “green CI” as proof of sound design or treating automated review as an independent human approval.

## Governance checklist for maintainers

- Protect default/release branches with GitHub branch protection or repository rulesets appropriate to plan and repository type. Consider required PRs, review count, CODEOWNER approvals, status checks, resolved conversations, signed commits, linear history and restrictions on force pushes/deletions. Keep bypass permissions minimal and audited.
- Give CI checks **unique, stable names**; identify the trusted GitHub App/source for required statuses where useful. A check marked skipped/neutral may satisfy some required-status configurations: choose workflows so important gates actually run.
- Place CODEOWNERS on the PR base branch in a supported location, ensure owners have write access, and protect CODEOWNERS itself. CODEOWNERS alone requests review; required code-owner approval needs an enforced rule.
- For busy branches, consider merge queue, if available to this repository/plan, and ensure required GitHub Actions also handle `merge_group`; otherwise queued checks may never report.
- Minimize repository and organization roles, protect release/tag creation where necessary, require reviewed deployment environments and keep a security disclosure route (for example SECURITY.md/private advisories).
- Enable and triage available Dependabot, secret scanning/push protection and code scanning features; availability depends on repository visibility, account plan and configuration. Rotate compromised secrets; do not merely dismiss alerts.
- Treat new contributors and PR comments as untrusted; verify links, scripts and workflow changes before running them with privileged credentials.

## Release and maintenance

Tag the *verified* release commit according to project policy; publish release notes covering compatibility, migrations and rollback. Protect release publishing permissions, build from the intended ref, keep provenance/artifact checks where supported, and document any manual deployment approval. For incident fixes use a focused hotfix branch/PR and backport with explicit ancestry verification; never patch history without an agreed recovery process.

## Done means verified

Check the merged commit on the intended base branch, status of required gates, resulting release/tag if applicable and links to resolved issues. If permissions or protections block an action, report the exact blocker rather than claiming the repository was changed.

## Primary references

- [GitHub flow](https://docs.github.com/en/get-started/using-github/github-flow) and [pull request reviews](https://docs.github.com/en/pull-requests/reference/pull-request-reviews).
- [Protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches) and [rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets).
- [CODEOWNERS](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners) and [merge queue](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue).
- [GitHub security features](https://docs.github.com/en/code-security/tutorials/secure-your-organization/protect-against-threats).
