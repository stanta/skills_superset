---
name: gitlab-development
description: This skill should be used when designing, implementing, reviewing, or refactoring GitLab CE/Self-Managed core or UX changes, especially merge-request governance, Gitaly boundaries, server hooks, GraphQL/Vue UI, Pajamas components, feature flags, and canonical-branch enforcement.
metadata:
  category: development
  version: "1.0.0"
  last_verified: "2026-09-20"
---

# GitLab Development Best Practices

## Purpose

Extend GitLab CE/Self-Managed without creating an unnecessary deep fork. Preserve GitLab architecture, UX conventions, upgradeability, and repository integrity while integrating external governance systems.

## Use this skill when

- Editing GitLab Rails, GraphQL, Vue, or Merge Request UX.
- Adding project/group governance UI.
- Adding server hooks or canonical-branch enforcement.
- Working with Gitaly or repository operations.
- Integrating GitLab with GOSH, blockchain governance, or an external policy engine.
- Reviewing a GitLab customization for upgrade, security, accessibility, or maintainability risk.

## Core architecture rule

Prefer extension around GitLab before modification inside GitLab.

Use this order:

1. Existing GitLab APIs and webhooks/system hooks.
2. External adapter/service.
3. Server-side Git hooks for hard enforcement.
4. Thin Rails/GraphQL/UI extension.
5. New Gitaly RPC only if a required Git operation is missing.
6. Deep GitLab/Gitaly fork only as a last resort.

For consensus-governed documents keep responsibilities separate:

- GitLab = authoring, branches, Merge Requests, diff, discussion, CI, UX.
- Governance Adapter = ballot lifecycle and chain/indexer integration.
- Canonical State Agent = verified local cache and branch synchronization.
- Governance contracts = authority and consensus.
- GOSH = verifiable Git-object availability when enabled.

## Gitaly boundary

Treat Gitaly as the repository-access boundary.

- Never add application code that reads or writes Git repository storage directly from disk.
- Reuse existing Gitaly RPCs first.
- Add a Gitaly RPC only when the Git operation itself is missing.
- Keep blockchain RPC calls out of Gitaly.
- Test GitLab and Gitaly changes together.

## Governed branch pattern

For a governed branch such as main:

- Allow normal feature-branch development.
- Seal one exact candidate commit SHA before starting a ballot.
- Never vote on a moving branch or tag.
- Invalidate or supersede a ballot if the candidate commit changes.
- Bind each ballot to the canonical parent commit.
- If the canonical parent changes before execution, mark the ballot stale and require rebase/review/revote.

Use a server-side pre-receive or update hook for hard enforcement in Self-Managed GitLab.

The hook should compare the incoming target SHA with a locally cached, cryptographically verified canonical SHA.

Do not call blockchain RPCs synchronously from a Git receive hook. Maintain canonical state with a separate daemon and fail closed if verified local state is unavailable.

## Git object integrity

Treat Git object IDs as protocol data.

- Store object algorithm plus digest in new protocol schemas.
- Do not assume SHA-1 forever.
- Verify full reachable object closure before a candidate becomes ballot-ready.
- Round-trip test candidate commit H through any external Git store and require the same H after fetch.
- Preserve author, committer, parents, tree, timestamps, and object-format semantics when exact OID preservation matters.
- Do not reconstruct a commit from rendered Markdown and assume identity.

## Rails and backend rules

- Keep controllers and GraphQL resolvers thin.
- Put domain behavior in focused service classes.
- Make authorization explicit on the server.
- Keep external calls outside long database transactions and locks.
- Make webhook and indexer processing idempotent and replay-safe.
- Treat duplicate events, delayed events, chain reorg/finality, and retries as normal distributed-system conditions.
- Use append-only audit records for governance state transitions where practical.

## GraphQL

Prefer the local GitLab API convention. For new interactive governance UI, GraphQL is usually the natural fit.

Expose stable domain fields such as:

- canonicalCommit
- canonicalParent
- candidateCommit
- ballotId
- ballotState
- quorum
- approvalThreshold
- effectiveVotingPower
- delegatedVotingPower
- staleReason
- executionState

Avoid N+1 access and paginate collections.

## Frontend and UX

Follow current GitLab frontend conventions.

- Use Vue for interactive applications.
- Reuse GitLab data/state patterns; prefer GraphQL/Apollo when appropriate.
- Do not introduce Vuex into new work.
- Reuse GitLab UI components and Pajamas patterns.
- Use existing design tokens and utility conventions.
- Support dark mode.
- Keep governance UI visually native to Merge Requests.

A governance MR widget should show, in priority order:

1. Exact candidate SHA.
2. Canonical parent SHA.
3. Ballot state.
4. Quorum and threshold.
5. The user's effective authority.
6. Delegation summary.
7. Canonicalization/execution status.

Use explicit labels such as "Vote FOR commit 93ff0c18" rather than ambiguous "Approve".

## Accessibility

Target WCAG 2.2 AA.

- Support keyboard-only operation.
- Preserve visible focus.
- Never encode status by color alone.
- Provide text alternatives for icons.
- Provide an accessible table/list representation for any delegation graph.
- Announce meaningful asynchronous state changes where appropriate.

## Identity binding

Do not infer governance identity from GitLab identity.

Bind GitLab account to participant/wallet identity using a signed challenge containing:

- GitLab instance identity.
- GitLab user ID.
- participant address/key.
- nonce.
- expiry.
- purpose/domain string.

Record the verified binding and its history.

## Feature flags

Use GitLab feature-flag conventions for risky or incremental changes.

- Start disabled where appropriate.
- Prefer actor-scoped rollout by project/group/user.
- Test enabled and disabled paths.
- Define removal criteria.
- Never use a feature flag as an authorization boundary.

## Observability

Correlate at least:

- project ID
- MR IID
- candidate SHA
- canonical parent SHA
- document ID
- ballot ID
- chain transaction/event ID

Monitor stale ballots, canonical-sync lag, hook rejections, GOSH publish/fetch failures, chain/indexer lag, and identity-binding failures.

## Required tests

### Unit

Test authorization, stale-parent detection, identity binding, state mapping, and canonical comparison.

### Integration

Test GitLab webhook to adapter, candidate publication, ballot/indexer flow, chain event to sync agent, and sync agent to GitLab ref update.

### End to end

Require a golden scenario:

1. Create MR.
2. Seal candidate SHA.
3. Publish/verify the exact commit.
4. Create ballot.
5. Delegate authority.
6. Vote.
7. Finalize.
8. Advance canonical registry.
9. Advance GitLab main to the exact SHA.
10. Reject an unauthorized SHA push.

Also test duplicate webhook, chain outage, missing object, stale parent, local branch tampering, failed execution, and corrupted local canonical cache.

## Review checklist

- No direct repository-disk access.
- Existing Gitaly APIs preferred.
- No blockchain call in Git receive critical path.
- Candidate SHA immutable for a ballot.
- Stale-parent protection exists.
- External events idempotent and replay-safe.
- Server-side authorization exists.
- UI follows GitLab/Pajamas patterns.
- Accessibility covered.
- Feature-flag lifecycle defined when used.
- Governance state is auditable.

## Anti-patterns

Avoid:

- Forking Gitaly to add blockchain logic.
- Polling blockchain from pre-receive.
- Voting on branch names.
- Merging first and voting later.
- Letting a ballot follow a moving MR SHA.
- Treating local main as canonical without verified consensus state.
- Hiding critical governance state only in a graph visualization.
- Silently applying a proposal to a different canonical parent.

## Pair with

- ballot-contracts for canonical-head and ballot semantics.
- gosh-development for Git object publication/verification.
- alligator-development for delegated voting.
- security-reviewer for security-critical GitLab changes.
- ux for complex governance interaction design.

## Authoritative references

- https://docs.gitlab.com/development/gitaly/
- https://docs.gitlab.com/development/fe_guide/
- https://docs.gitlab.com/development/fe_guide/vue/
- https://docs.gitlab.com/development/feature_flags/
- https://design.gitlab.com/
