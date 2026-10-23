# Structural Refactoring Patterns

Select a transformation based on the responsibility and observed change cost.
Verify the behavior involved instead of matching a code smell mechanically.

## Distinguish shared knowledge from coincidental similarity

Two calculations can use the same expression while representing independent
business rules. If their owners and reasons to change differ, a shared helper
may force future edits to account for unrelated modes. Keep the rules separate
until a common concept is established.

Conversely, the same authorization rule in two paths is one invariant even
before a third use exists. Centralize it when coordinated maintenance is
required; do not use AHA to justify known inconsistent enforcement.

## Unwind a wrong abstraction

For a helper that mixes distinct responsibilities:

1. Enumerate callers and the branch each caller actually uses.
2. Capture surviving behavior at a useful public boundary.
3. Inline the relevant logic for each caller without changing semantics.
4. Remove irrelevant parameters and branches locally.
5. Re-extract only the common knowledge that now has a stable meaning.

Some parameters represent legitimate variation in one algorithm or policy.
Keep them when the abstraction remains understandable and its callers do not
need unrelated implementation knowledge.

## Check forwarding layers before collapsing them

| Layer behavior | Structural response |
| --- | --- |
| Merely forwards identical arguments and results | Consider inlining or merging after checking all consumers |
| Enforces a transaction or authorization boundary | Preserve that policy explicitly even if the wrapper changes |
| Translates external failures and retry semantics | Keep the protocol details hidden behind a useful interface |
| Exists only to mirror another class hierarchy | Look for redundant concepts and coordinated maintenance |
| Adapts a public compatibility contract | Inspect active external consumers before changing the interface |

Do not count the number of implementations as a substitute for this analysis.

## Group by a use case without duplicating invariants

Move scenario-specific orchestration together when developers repeatedly edit
the same scenario across many generic layers. Allow a simple scenario to remain
simple; introduce a domain model where the behavior requires it.

Keep shared invariants in an authoritative location. Do not copy payment,
authorization, or data-consistency rules into each slice for convenience.
Grouping by scenario is not a requirement to adopt a command bus, event store,
or separate read and write databases.

## Separate decisions from effects carefully

Extract deterministic decisions that consume explicit values and return results
or actions. Keep network, persistence, clocks, and other effects at a clear
boundary when this reduces coupling.

Check snapshot consistency and transaction semantics before moving reads
outside an operation. Check memory and latency before loading all inputs eagerly.
Preserve required side-effect order and retry behavior. A functional core is
useful only when the whole operation retains its required properties.

## Keep tests resilient to structure

Prefer assertions on required outcomes and public contracts. Update test setup
when constructors or internal collaborators change. Retain assertions that
represent required behavior, including an implementation mechanism when that
mechanism is itself a requirement, such as avoiding a prohibited external call.

Do not preserve an obsolete private call sequence merely to satisfy a brittle
mock. Do not delete a valid behavioral assertion merely because refactoring
made it fail. Resolve which requirement the check actually represents.

## Stop on a useful outcome

Choose a representative change that was previously difficult. Explain which
knowledge, coordinated edits, or indirect calls the new structure eliminates.
Keep any tradeoff explicit: additional local code can reduce cross-module
coupling, and a slightly larger module can expose a simpler interface.
