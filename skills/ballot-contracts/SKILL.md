---
name: ballot-contracts
description: This skill should be used when designing, implementing, auditing, or testing security-critical voting and ballot smart contracts, especially exact-Git-commit ballots, electorate snapshots, quorum and thresholds, signatures, timelocks, stale-parent protection, delegated authority consumption, and CanonicalHeadRegistry execution.
metadata:
  category: security
  version: "1.0.0"
  last_verified: "2026-09-20"
---

# Voting / Ballot Contract Best Practices

## Purpose

Design ballots that bind the electorate, exact proposed state, decision rules, and canonical parent so a successful vote can safely authorize one precise Git state transition.

## Use this skill when

- Building ballot/governor contracts.
- Designing electorate snapshots.
- Implementing quorum/threshold logic.
- Adding vote/delegation signatures.
- Updating a CanonicalHeadRegistry.
- Reviewing governance upgrade/timelock roles.
- Auditing delegated-voting conservation or stale-parent safety.

## Core principle

Every ballot must bind:

- who can decide.
- exactly what state is proposed.
- under which rules.
- against which current canonical parent.
- when entitlement is snapshotted.
- how execution changes canonical state.

Never vote only on human-readable text, a mutable URL, a branch, or a PR/MR number.

## Ballot manifest

Seal a canonical manifest before activation.

Recommended consensus-critical fields:

- documentId
- repositoryId
- candidate Git OID
- canonical parent Git OID
- Git object/hash algorithm
- electorateRoot or electorateId
- total eligible authority
- rulesetId/rulesetHash
- proposal type
- snapshot timepoint
- voting start/end
- quorum
- approval threshold
- execution delay
- availability attestation/reference if required

Changing any consensus-critical field requires a new ballot.

## Exact Git state

Vote on algorithm + immutable Git OID.

Do not vote on:

- branch.
- tag.
- URL.
- MR/PR number.
- rendered HTML/Markdown.
- file path without content identity.

Also bind the candidate to the canonical parent.

## Stale-parent protection

Concurrent proposals may start from A:

A -> B
A -> C

If B executes first, C must not silently become B -> C.

Execution must require:

currentCanonicalHead == ballot.canonicalParent

Otherwise mark/revert as STALE and require rebase, review, and revote.

Treat this as a critical invariant.

## Git hash representation

Do not hard-code bytes20 just because SHA-1 is common.

Represent:

- algorithm identifier.
- digest bytes.

Validate digest length for the selected algorithm.

## Electorate snapshot

Freeze:

- eligible participants.
- entitlement per origin.
- total eligible authority.
- snapshot timepoint.

Do not compute quorum from a live mutable membership table after voting starts.

For ballot-scoped authority, prefer explicit entitlement/checkpoint or Merkle-root semantics rather than a freely transferable ERC-20 unless transferability is intentionally part of governance.

## Reuse audited governance primitives where semantics fit

Prefer OpenZeppelin Contracts 5.x Governor extensions rather than rewriting standard lifecycle logic.

Relevant modules include:

- Governor
- GovernorVotes
- GovernorVotesQuorumFraction
- GovernorCountingFractional
- GovernorCountingOverridable
- GovernorPreventLateQuorum
- GovernorTimelockControl
- GovernorTimelockAccess
- GovernorSettings
- GovernorStorage

Do not force ballot-scoped delegated authority into ERC20Votes if the authority model differs.

## Governance clock

Use one consistent timepoint model.

ERC-6372 can describe whether the governance clock is block-number, timestamp, or another monotonic source.

Do not mix clock modes between snapshots, quorum, governor, and UI assumptions.

## Delegation versus vote counting

Keep modules conceptually separate:

1. entitlement/origin authority.
2. delegation/redelegation.
3. authority consumption.
4. vote counting.
5. proposal outcome.
6. execution.

Do not hide graph mutation inside tally code.

## Fractional concepts

Distinguish:

- fractional delegation: split authority among delegates.
- fractional voting: split used authority among FOR/AGAINST/ABSTAIN.

OpenZeppelin GovernorCountingFractional addresses the latter, not the full former.

Define consumption carefully if both are enabled.

## Vote consumption

Recommended high-integrity semantics:

- Every cast consumes a specified amount of remaining authority.
- Consumed authority cannot be reused through another path.
- Revocation/redelegation affects only unconsumed authority.
- Vote changes are disabled unless explicitly modeled and proven safe.

## Quorum and threshold

Define separately:

- quorum denominator.
- whether abstain counts toward quorum.
- approval threshold denominator.
- snapshot source.
- per-proposal-type variations.
- rounding.

Use integer/fixed-point math only.

Consider late-quorum protection so decisive participation at the final moment does not prevent meaningful response.

## Rulesets / proposal types

Version and hash rulesets.

A ruleset may define:

- electorate.
- quorum.
- approval threshold.
- voting delay/period.
- late-quorum extension.
- execution delay.
- delegation allowed/disabled.
- emergency/cancel powers.

Ballot must bind the exact ruleset version.

## Timelock

Use a timelock where an execution delay is part of governance.

If using TimelockController:

- Governor should normally be the proposer.
- Minimize extra proposers/cancellers.
- Ensure a reliable executor exists.
- Document every privileged bypass.

Zero delay may be valid for immediate constitutional state changes, but make it explicit.

## CanonicalHeadRegistry

Keep the registry minimal.

Responsibilities:

- store current canonical Git OID by document.
- verify authorized governance execution.
- enforce stale-parent match.
- update exactly to ballot candidate.
- emit canonical transition event.

Do not put document bodies, delegation graphs, UI metadata, or arbitrary admin mutation in the registry.

Suggested event concept:

CanonicalHeadChanged(documentId, oldOid, newOid, ballotId, effectiveTimepoint)

## Execution semantics

Execution should atomically:

1. verify ballot outcome/queue state.
2. verify current head equals ballot parent.
3. update canonical head to candidate.
4. record execution.
5. emit event.

Do not update GitLab directly from the contract. Off-chain sync agents materialize the state selected by consensus.

## Object availability

Before ballot activation require independent evidence that the candidate commit and required reachable objects are retrievable from the designated verifiable Git store.

Availability proof is separate from governance approval.

Never canonize an unrecoverable commit.

## EIP-712 signatures

For signed vote/delegation actions use typed structured data.

Bind:

- chain ID/domain.
- verifying contract.
- ballot/proposal ID.
- action type.
- amount/choice.
- nonce.
- expiry.

Prevent replay across ballots, chains, contract instances, and nonce epochs.

Prefer battle-tested OpenZeppelin EIP-712 utilities.

## Lifecycle

Use explicit states such as:

DRAFT
SEALED
PENDING
ACTIVE
SUCCEEDED
DEFEATED
QUEUED
STALE
EXECUTED
CANCELLED

Do not use "passed" as a synonym for canonical. SUCCEEDED is not EXECUTED.

## Cancellation and break glass

Define who can cancel and at which lifecycle stages.

Possible rules:

- proposer cancels before activation.
- governed guardian cancels before execution.
- parent mismatch makes ballot stale.
- emergency council can pause only under explicit constitutional rules.

Cancellation must never rewrite historical votes.

## Upgrades are constitutional events

If proxies are used:

- identify proxy admin.
- prefer governance/timelock control.
- test storage layout and semantic preservation.
- preserve historical ballots and consumed authority.
- emit upgrade events.
- maintain recovery plan.

A unilateral multisig upgrade key is a constitutional root of trust and must be documented.

## Denial-of-service and gas

Avoid O(N electorate) work during creation, voting, finalization, or execution.

Use snapshots, Merkle proofs/checkpoints, events, and indexers.

For delegated paths, make gas proportional to the supplied path and bound transaction size operationally.

## Required invariants

Use Foundry unit, fuzz, and invariant tests.

### Ballot immutability

Sealed consensus-critical manifest fields cannot change.

### Parent safety

Execution requires current head == ballot parent.

### Exact transition

Execution changes head only to ballot candidate.

### Single execution

A ballot cannot execute twice.

### Supply conservation

Consumed authority never exceeds frozen eligible authority.

### No double counting

One authority unit cannot influence tally twice.

### Snapshot immutability

Post-snapshot eligibility changes do not alter ballot entitlement.

### Tally consistency

FOR + AGAINST + ABSTAIN equals consumed cast authority for the chosen counting model.

### Signature replay safety

An accepted signature cannot change state twice.

### Stale safety

A stale ballot cannot mutate canonical state.

### Upgrade preservation

Upgrade cannot change historical outcomes or resurrect consumed authority.

## Test matrix

Include:

- zero voters.
- one voter.
- max entitlement.
- fractional fixed-point boundaries.
- threshold exactly equal / one unit below / one above.
- quorum reached at end.
- late quorum.
- abstain semantics.
- duplicate vote.
- multiple delegated paths.
- cycle attempt.
- expired/replayed/wrong-domain signature.
- concurrent ballots from same parent.
- stale execution.
- missing candidate object.
- execution retry.
- timelock role misconfiguration.
- upgrade/migration.

Differential-test delegated/tally logic against a pure off-chain reference model.

## Review checklist

- Exact candidate Git OID bound.
- Exact canonical parent bound.
- Hash algorithm explicit.
- Electorate and total power snapshotted.
- Ruleset/version immutable.
- Delegation cannot create or double-use authority.
- Quorum and abstention semantics explicit.
- Late quorum considered.
- Signature nonce/expiry/domain separation correct.
- Stale execution blocked.
- Canonical registry privileged surface minimal.
- Timelock roles cannot bypass governance unexpectedly.
- Upgrade authority documented.
- Events support independent reconstruction.
- No O(N electorate) execution path.
- Fuzz/invariant testing planned.
- External audit planned before production.

## Anti-patterns

Avoid:

- Voting on mutable refs.
- Ignoring canonical parent at execution.
- Quorum from mutable live membership.
- Floating-point thresholds.
- Treating SUCCEEDED as canonical.
- Hidden admin write access to canonical head.
- UI/indexer as tally authority.
- Looping over all voters to finalize.
- Unaudited signature code.
- Upgrades that reset consumed authority.
- Editing proposal content after sealing.

## Pair with

- alligator-development for fractional multi-hop delegation.
- gosh-development for candidate object availability.
- gitlab-development for MR/canonical branch integration.
- security-reviewer and test-master before production.

## Authoritative references

- https://docs.openzeppelin.com/contracts/5.x/api/governance
- https://docs.openzeppelin.com/contracts/5.x/governance
- https://eips.ethereum.org/EIPS/eip-5805
- https://eips.ethereum.org/EIPS/eip-6372
- https://github.com/voteagora/optimism-governor
