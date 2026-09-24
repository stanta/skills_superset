---
name: gosh-development
description: This skill should be used when developing or integrating GOSH as a verifiable on-chain Git/object layer, including git-remote-gosh, repository contracts, version pinning, object verification, branch protection, GOSH governance boundaries, and GitLab-to-GOSH synchronization.
metadata:
  category: development
  version: "1.0.0"
  last_verified: "2026-09-20"
---

# GOSH Development Best Practices

## Purpose

Integrate GOSH safely as a verifiable Git-object layer while keeping Git semantics, version compatibility, licensing, consensus boundaries, and key management explicit.

## Use this skill when

- Working with GOSH repositories or smart contracts.
- Integrating git-remote-gosh.
- Publishing or fetching candidate commits.
- Verifying Git objects before governance voting.
- Reviewing GOSH branch protection or native governance.
- Connecting GOSH to GitLab or an external ballot engine.

## First rule: identify the exact GOSH component

Before editing or embedding code:

1. Identify repository, tag/commit, contract version, and toolchain.
2. Read the current license of that exact component.
3. Pin the version in deployment/configuration.
4. Do not assume every GOSH-related repository has the same license or compatibility.

Treat license review as part of architecture if code will be distributed commercially.

## Recommended role in the governance stack

Use:

- GitLab for authoring and review.
- GOSH for verifiable Git-object storage and retrieval.
- Ballot/Alligator-derived contracts for authority and voting.
- CanonicalHeadRegistry for the authoritative document commit.
- Sync Agent for local reproduction.

Do not create two uncoordinated consensus engines for the same transition.

If EVM governance selects the canonical commit, avoid also requiring a separate GOSH SMV decision unless disagreement semantics are formally defined.

## Version pinning

Pin:

- GOSH release/tag/commit.
- contract version and ABI/code hashes where relevant.
- git-remote-gosh version.
- Ever Solidity/TVM toolchain version.

Never depend on "latest" in production.

For upgrades:

1. Read migration notes.
2. Verify repository addressing.
3. Test remote-helper compatibility.
4. Test old/new object compatibility.
5. Re-run exact OID round-trip tests.
6. Re-run canonical-object availability tests.

## Git remote helper boundary

Treat git-remote-gosh as an integration boundary.

- Configure explicitly.
- Keep wallet credentials outside repositories.
- Mount secrets/config separately.
- Check helper version at startup.
- Classify errors into retryable and non-retryable.
- Never log or commit seed phrases/private keys.

## Exact Git OID preservation

The exact candidate commit is the governance object.

Before ballot activation:

1. Create candidate commit in primary Git workflow.
2. Publish the exact commit to GOSH.
3. Fetch it from a clean verifier environment.
4. Require identical Git OID.
5. Verify all reachable trees, blobs, and required parents.
6. Only then mark candidate as available for voting.

Never vote on a mutable branch, URL, rendered document, or PR/MR ID alone.

## Object-closure verification

Verify:

- commit exists.
- parent commits required by policy exist.
- root tree exists.
- reachable trees exist.
- reachable blobs exist.
- external/submodule/LFS content rules are explicit.

If the governed document depends on external content, the commit hash alone may not guarantee complete availability. Prefer self-contained governed content or separately hash and anchor required external artifacts.

## Understand native GOSH governance separately

GOSH native DAO/SMV semantics are not automatically equivalent to ballot-scoped delegated governance.

Before reusing native governance, map:

- source of voting power.
- Karma or other modifiers.
- proposal creation rules.
- expert tags.
- proposal lifecycle.
- branch-protection behavior.
- execution semantics.

Never treat two systems as equivalent merely because both use "votes".

## Contract-development rules

GOSH uses TVM/Ever Solidity concepts, not EVM semantics.

- Do not copy Solidity/EVM assumptions blindly.
- Pin compiler/toolchain.
- Preserve authorization boundaries.
- Treat asynchronous cross-contract messaging and failure paths as protocol logic.
- Avoid assuming Ethereum-style atomicity across multiple messages.
- Preserve versioning/migration discipline for core contract changes.

## Separate availability from governance finality

A commit being available in GOSH proves object availability/verifiability according to GOSH rules.

It does not prove:

- electorate eligibility.
- delegation validity.
- quorum.
- ballot success.
- canonical-head update.
- external chain finality.

Track these states independently:

- available commit
- candidate commit
- approved commit
- canonical commit
- local checkout

## Build a narrow adapter

Keep GOSH calls out of GitLab business code.

Expose a small adapter such as:

- publishCommit(repo, oid)
- verifyCommit(repo, oid)
- verifyObjectClosure(repo, oid)
- fetchCommit(repo, oid)
- getPinnedVersion()
- health()

Return structured outcomes such as AVAILABLE, MISSING_OBJECT, OID_MISMATCH, VERSION_UNSUPPORTED, AUTH_FAILED, NETWORK_UNAVAILABLE, or CONTRACT_ERROR.

Make publication idempotent. Use Git OID as a natural idempotency key where possible.

## Key management

Separate:

- developer/test keys.
- CI keys.
- production service wallet.
- governance participant wallets.

Use secret management, least privilege, and rotation. Never reuse voter keys for sync/publishing services.

## Required tests

### Integration

- Initialize test DAO/repository.
- Push exact commit via remote helper.
- Fetch/clone into clean environment.
- Verify same OID.
- Verify reachable object closure.
- Retry duplicate publication safely.

### Governance integration

1. GitLab creates H.
2. Adapter publishes H to GOSH.
3. Independent verifier fetches H.
4. Verifier confirms H and object closure.
5. Ballot for H activates.
6. Governance succeeds.
7. Canonical registry selects H.
8. Independent sync node fetches H from GOSH and materializes it.

### Negative

Test wrong version, missing blob, wrong repository, unavailable key, incompatible helper, network partition, duplicate publication, OID mismatch, and accidental native SMV triggering.

## Observability

Record:

- pinned GOSH version.
- repository identifier.
- Git OID.
- publication/fetch operation identifier.
- verification duration.
- object-closure failures.
- helper exit status.
- service wallet identity, never secret material.
- retry count.

Alert if current canonical commit cannot be fetched for a sustained interval.

## Review checklist

- Exact GOSH component and license checked.
- Version/ABI/toolchain pinned.
- Secrets outside Git.
- Exact OID round-trip tested.
- Object closure verified before ballot activation.
- Native SMV not accidentally a second authority.
- Availability not confused with finality.
- Adapter is idempotent.
- Upgrade compatibility tested.
- Independent node can fetch canonical commit.

## Anti-patterns

Avoid:

- Depending on latest GOSH contracts.
- Assuming EVM and TVM semantics match.
- Voting before object availability verification.
- Voting on a branch name.
- Mixing two independent governance outcomes.
- Treating a GOSH branch as canonical without consulting the canonical registry.
- Assuming all GOSH repositories use the same license.

## Pair with

- gitlab-development for authoring/workflow integration.
- ballot-contracts for canonical-head semantics.
- alligator-development for delegated voting.
- security-reviewer for contract and key-management review.

## Authoritative references

- https://docs.gosh.sh/on-chain-architecture/gosh-smart-contracts/
- https://docs.gosh.sh/on-chain-architecture/organizations-gosh-dao-and-smv/
- https://docs.gosh.sh/working-with-gosh/gosh-web/repository/
- https://docs.gosh.sh/working-with-gosh/git-remote-helper/
- https://github.com/gosh-sh/gosh
