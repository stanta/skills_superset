---
name: git-history-recovery
description: Use when Git changes appear lost, an operation has conflicted or gone wrong, a commit must be undone, a branch was rewritten, or sensitive material entered version history.
metadata:
  category: development
  last_verified: "2026-09-27"
---

# Git History Recovery and Safe Undo

## Safety contract

First classify **uncommitted vs committed** and **local/private vs published/shared** changes. Inspect state before proposing an undo operation. Do not run `reset --hard`, `clean -fd(x)`, unconditional force-push, history filtering or worktree deletion without explicit informed authorization for the exact affected data. Git cannot recover every untracked or never-committed edit.

Use [git-core-workflows](../git-core-workflows/SKILL.md) for routine work and [github-pull-request-workflows](../github-pull-request-workflows/SKILL.md) when the incident affects a GitHub PR/protected branch.

## Diagnose and preserve evidence

1. Capture `git status --short --branch`, `git diff`, `git diff --cached`, `git log --graph --oneline --decorate -20`.
2. Identify ongoing operation: `git status` and, where relevant, `git reflog --date=iso -30`. Inspect the intended branch, remote refs and exact affected file paths.
3. Save a reviewed patch or make an explicitly approved backup copy/branch before destructive changes; a patch normally does **not** preserve untracked files or all binary metadata.
4. Decide whether other people/CI/deployments consumed the commit. Published history must be treated as shared even if the author is the only current editor.

## Select the least destructive remedy

| Situation | Typical remedy | Guard |
| --- | --- | --- |
| Wrong file staged, working tree content should stay | `git restore --staged -- path` | Check index diff afterwards |
| Tracked uncommitted edits should be discarded | `git restore --worktree -- path` | Explicitly confirm the exact loss |
| A pushed commit needs undoing | `git revert <sha>`; use `-m` for a merge only after identifying the correct mainline | New auditable commit, no rewrite |
| Last local, unpublished commit needs amendment | `git commit --amend` | Verify it was not shared |
| Local unpublished commits should move to a base | Rebase/interactive rebase after backup | Rewrites commit IDs |
| Merge, rebase or cherry-pick is in progress and unsafe | Matching `git merge --abort`, `git rebase --abort`, `git cherry-pick --abort` | Confirm operation and saved work first |
| Stash contains needed work | `git stash list` and `git stash show -p stash@{n}`; prefer `git stash apply` before `drop` | Applying can conflict; stash is not a durable backup |
| A branch/commit appears missing | Inspect `git reflog`; create rescue ref `git branch rescue/<case> <sha>` | Reflog expiration and GC limit recovery |

`git reset --soft` changes the current branch but preserves staged changes; `--mixed` resets the index while preserving working-tree edits; `--hard` discards tracked edits. Only use reset after classifying publication and loss. `git clean -n` is a preview, not permission to run `git clean -fd`. Be especially cautious with `-x`, which includes ignored files.

## Published history rewrite protocol

Prefer revert on shared history. If a rewrite is unavoidable (for example, to remove committed sensitive material), inventory branches, tags, forks, PRs, releases, cached copies, signatures, artifacts and all affected collaborators. Obtain explicit repository-owner approval and a coordinated freeze/re-clone plan. Preserve an incident record outside the affected repository. Rewriting IDs can invalidate signatures, reviews, links, tags, and in-flight work; do not treat a successful force-push as complete remediation.

**Leaked credential order:** revoke/rotate the secret and assess misuse **first**. Remove its live use, then coordinate history cleanup with approved tooling such as git-filter-repo if justified; address forks/caches and notify owners. A GitHub push-protection or secret-scanning alert is evidence for investigation, not proof the credential is safe.

## Recovery verification

After each operation inspect status, log/reflog, range-diff or compare against intended base, test the behavior, and verify the remote SHA independently where a remote changed. Report exactly what was recovered, what was lost/unrecoverable, and what collaborators must do.

## Primary references

- [git-reflog](https://git-scm.com/docs/git-reflog), [git-restore](https://git-scm.com/docs/git-restore), [git-reset](https://git-scm.com/docs/git-reset), [git-revert](https://git-scm.com/docs/git-revert).
- [git-rebase](https://git-scm.com/docs/git-rebase) and [git-push](https://git-scm.com/docs/git-push).
- [GitHub: removing sensitive data from a repository](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository).
- [GitHub push protection](https://docs.github.com/en/code-security/concepts/secret-security/push-protection).
