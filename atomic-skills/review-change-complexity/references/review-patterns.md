# Complexity Review Patterns

Use these patterns to formulate evidence-based findings and recognize justified complexity.
Treat them as examples of reasoning, not name-based rules for rejecting code.

## Repeated code and wrong abstractions

Two look-alike calculations belong to separate business processes and have independent change histories. A proposed shared function adds several mode switches to preserve their differences.

Inspect whether the rule must remain identical by contract. If not, recommend keeping the processes separate or sharing only the stable common operation. Do not reject the change because it contains a particular number of switches; explain the conflicting responsibilities and change coupling.

Counter-case: the same monetary rounding rule must apply throughout one financial domain. A shared implementation can be justified immediately, even before a third caller appears.

## A single-provider adapter

A new adapter has one implementation. It centralizes provider error translation, idempotency and retry behavior that callers currently repeat.

Accept the adapter when it reduces the callers' knowledge and preserves operational guarantees. Challenge additional factories, registries or plugin discovery only if they add no current capability. One implementation is not itself evidence of waste.

## Premature infrastructure

A PR adds a message broker and workflow engine for a single synchronous operation. The task gives no durability, independent scaling or asynchronous response requirement.

Compare against an ordinary application function or existing job mechanism. Describe extra deployment, failure and consistency obligations introduced by the proposed infrastructure. If guaranteed background execution is an explicit current requirement, evaluate the simplest durable design instead of removing that requirement.

## Large but simple changes

A diff removes generated artifacts or updates imports mechanically across many files.

Inspect whether the transformation is uniform and verification covers affected consumers. Do not demand arbitrary line limits or split changes into pieces that cannot build independently merely to satisfy a small-PR slogan.

## Small but consequential changes

A few lines introduce a global registry, change a public default or redirect all writes through a new shared component.

Trace consumers and lifetime/ownership. Small line count does not establish low risk or low complexity. Identify the new global assumptions and the concrete scenario that requires them.

## Cleanup that weakens verification

A cleanup removes a stale flag and deletes a test that also checked duplicate-payment prevention. CI passes because the assertion is gone.

Require preservation of the idempotency assertion with updated setup. Distinguish retired feature coverage from still-required behavior. Recommend the narrow correction; do not insist that every historical test or flag survive forever.

## Cross-agent duplication

Two parallel tasks add separate retry utilities and incompatible representations of one existing domain concept.

Compare the real contracts before merging them. Reuse an existing suitable implementation or consolidate a shared invariant; preserve separate types if they express different domain meanings. Assign integration of the common contract to the existing responsible owner rather than introducing a new agent hierarchy by default.

## Example finding

**Location:** `notifications/provider_registry.py`, new registry and dynamic import path.

**Requirement:** Send email through the configured provider; provider replacement is outside the current task.

**Evidence:** The only caller passes a fixed key. The provider adapter already hides transport errors. The registry adds configuration validation and a dynamic import failure mode without a supported selection scenario.

**Counter-evidence:** No extension API or tenant-specific provider selection is documented. Reassess if such a current contract exists.

**Recommendation:** Instantiate the existing adapter through the application's current composition mechanism. Keep the adapter's error handling. Verify the notification behavior and configuration failure cases that remain.

## Proportional conclusion

- Return few, supported findings rather than an exhaustive smell inventory.
- Distinguish a necessary correction from an equally valid design preference.
- Avoid broad rewrite suggestions for a local diff.
- Retain uncertainty when runtime or organizational constraints are unavailable.
- Do not turn examples into hard limits on interfaces, files, dependencies, service counts or test coverage.
