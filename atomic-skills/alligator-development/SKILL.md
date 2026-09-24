---
name: alligator-development
description: This skill should be used when implementing, adapting, testing, or reviewing Agora/Optimism Alligator-style partial delegation, re-delegation, authority paths, allowances, ballot-scoped delegation graphs, voting-power provenance, and client/indexer interpretation.
metadata:
  category: development
  version: "1.0.0"
  last_verified: "2026-09-20"
---

# Alligator / Advanced Delegation Best Practices

## Purpose

Use Alligator and Agora governance as proven references for partial delegation and re-delegation, while defining explicit ballot-scoped semantics for systems that require conserved, auditable voting authority.

## Use this skill when

- Implementing fractional delegation.
- Implementing re-delegation or multi-hop authority.
- Adapting Alligator to per-ballot voting entitlements.
- Calculating effective voting power.
- Designing delegation events, indexers, or UX.
- Testing conservation, cycles, replay, or double-use.

## Start with the correct mental model

Alligator supports partial subdelegations and allowance rules. Current Agora/Optimism documentation explicitly notes that subdelegation allowances can sum beyond 100% and that effective voting power is non-trivial to derive.

Therefore:

- Do not calculate voting power by naively summing incoming edges.
- Treat allowance and consumed authority as distinct concepts.
- Treat multiple vote events from the same actor/proposal as valid possibilities.
- Keep provenance: actor, origin authority, path, and amount.

## Define target semantics before coding

Do not copy Alligator semantics blindly.

For ballot-scoped governance define:

- ballotId.
- origin participant.
- frozen entitlement.
- retained authority.
- delegated allowance/authority.
- consumption rules.
- snapshot timepoint.
- direct-vote semantics.
- cycle semantics.
- revocation semantics.
- path validation.

Document these rules before Solidity implementation. Keep a small pure reference model as the executable specification.

## Ballot scope

Scope every delegation edge explicitly to the ballot unless a separate default-delegation layer intentionally materializes defaults into the ballot snapshot.

Recommended logical key:

(ballotId, delegator, delegate, ruleId)

This allows a direct explanation of why a delegate had a given weight in a specific decision.

## Fixed-point arithmetic

Use integers only.

- Define denominator/precision.
- Define absolute vs relative allowance modes explicitly.
- Define rounding.
- Test exact boundaries.
- Never use floating point in contract or canonical tally logic.

## Conservation

For the ballot-scoped design prefer a strong invariant:

For every origin O and ballot B:

consumedAuthority(O,B) <= frozenEntitlement(O,B)

The same authority unit must not affect tally twice.

If preserving Alligator-style over-allocation of allowances, make it clear that allowances are limits, not simultaneously spendable balances, and define deterministic consumption behavior.

## Multi-hop re-delegation

Support paths such as:

Alice -> Bob -> Carol -> David

Do not recursively traverse the entire delegation graph on-chain.

Prefer path-based authorization:

1. Submit an authority path.
2. Verify each edge and rule.
3. Compute path capacity.
4. Check already consumed authority.
5. Consume only the used amount.
6. Record provenance.

Logical delegation depth may be unbounded even though one EVM transaction must remain gas-bounded.

For future optimization consider path compression, Merkle proofs, off-chain path discovery with on-chain verification, or ZK proofs.

## Cycle handling

Never let a cycle amplify authority.

Preferred semantics:

- Reject cycle-forming edges if economical.
- Otherwise require simple, non-repeating paths at vote time.
- Make cyclic edges unusable for amplification.
- Flag cycles in the indexer/UX.

Property-test that adding cycles never increases total exercisable authority.

## Direct vote semantics

Specify direct-vote behavior explicitly.

Recommended simple model:

- Casting consumes a specific amount of authority.
- Consumed authority cannot be reused.
- Origin voter may use any still-unconsumed authority directly.
- Direct voting only overrides unused delegated allowance, not already consumed votes.
- Revocation/redelegation never resets consumption.

Avoid retroactive rewriting of previously cast votes unless the constitution intentionally supports mutable ballots.

## Snapshot and clock

Freeze entitlement using one explicit governance timepoint model.

If using ERC-6372/OpenZeppelin clocks, ensure every voting-power and governor component uses the same clock semantics.

If delegation may change during voting, define how already-consumed authority constrains later changes.

## Events are protocol data

Emit enough events to reconstruct:

- delegation creation/update/revocation.
- ballot ID.
- allowance rule.
- authority consumption.
- vote provenance.
- direct vote.
- invalidation/cancellation.

Clients must not infer critical state only from transaction calldata.

Version event schemas carefully.

## Client/indexer rules

Do not assume one voter + one proposal = one vote event.

Aggregate by:

- ballot/proposal.
- authority origin.
- actor/voter.
- path/proxy.
- consumed amount.

Expose both actor and origin.

Example UX:

17.42 total
3.00 own
9.25 directly delegated
5.17 re-delegated

Always provide expandable provenance paths.

The indexer is for convenience and explanation; the contract remains authoritative.

## Proposal-type modularity

Keep delegation mechanics separate from proposal policy.

Ballot/proposal type may define:

- quorum.
- approval threshold.
- voting delay/period.
- late-quorum extension.
- delegation allowed or disabled.
- operational path-length limit.
- execution delay.
- direct-vote rule.

Do not hard-code constitutional thresholds into delegation contracts.

## Privileged roles and upgrades

Minimize privileged bypasses.

- Separate upgrade authority from normal governance.
- Prefer timelocked/governed upgrades.
- Document emergency powers.
- Emit events for break-glass actions.
- Never allow an administrator to silently rewrite historical tallies.

Before upgrade:

- replay real delegation graphs.
- preserve consumed authority.
- preserve historical ballot interpretation.
- version event/indexer changes.
- verify semantic, not only storage-layout, compatibility.

## Required invariants

Use Foundry fuzz/invariant testing.

### Conservation

Consumed authority never exceeds frozen origin entitlement.

### No double use

One authority unit cannot contribute twice to tally.

### Path bound

Authority exercised through a path is bounded by every edge/rule and remaining origin authority.

### No cycle amplification

Cycles cannot increase effective power.

### Revocation safety

Revoking unused delegation cannot create authority elsewhere.

### Snapshot immutability

Post-snapshot membership/balance changes do not alter entitlement.

### Replay protection

Signed operations cannot replay across ballots, chains, contract instances, or nonces.

### Upgrade preservation

Upgrade cannot resurrect consumed authority.

## Differential testing

Maintain an independent reference model in Python/TypeScript.

Generate random DAGs and adversarial graphs, then compare on-chain results against the reference model.

Include complex re-delegation patterns because production Optimism governance has already required fixes/improvements around advanced delegation allowance calculations.

## Gas and DoS

Protect against:

- unbounded arrays.
- global graph traversal.
- duplicate path entries.
- huge event payloads.
- O(N electorate) work at vote/finalize time.
- pathological deep paths.

Make cost depend on the submitted path, not the full graph.

## Review checklist

- Target semantics documented separately from stock Alligator.
- Ballot scope explicit.
- Fixed-point arithmetic/rounding explicit.
- Conservation and no-double-use enforced.
- Multi-hop verification does not globally traverse the graph.
- Cycle behavior specified and tested.
- Direct-vote behavior specified.
- Snapshot/clock fixed.
- Events reconstruct state.
- Multiple vote events supported by clients.
- Upgrade authority minimized.
- Reference model exists.
- Fuzz/invariant tests cover random graphs.
- Indexer is non-authoritative.

## Anti-patterns

Avoid:

- Summing incoming edges as voting power.
- Assuming allowances are <=100%.
- Floating point.
- Global recursive graph traversal.
- Letting redelegation reset consumed authority.
- Letting an indexer define tally.
- Copying Optimism privileged-role assumptions without constitutional review.
- Treating a branch/ref as the authority scope.

## Pair with

- ballot-contracts for proposal lifecycle and tally.
- security-reviewer for contract review.
- test-master for invariant/fuzz/regression planning.
- gitlab-development when exposing delegation in GitLab UI.

## Authoritative references

- https://github.com/voteagora/optimism-governor
- https://github.com/voteagora
- https://gov.optimism.io/t/final-governor-update-proposal-2-improvements-to-advanced-delegation-allowance-calculations/8164
- https://eips.ethereum.org/EIPS/eip-5805
- https://eips.ethereum.org/EIPS/eip-6372
