---
name: review-change-complexity
description: >
  Review a diff or implementation plan for overengineering, code bloat, speculative abstractions, dependency growth and unnecessary coordination costs. Use for simplicity review, AI-generated or multiagent changes, YAGNI/AHA checks, ревью сложности, оверинжиниринг and раздувание кода. Return evidence-based findings and a simpler viable alternative; complement general correctness/security review rather than replacing it. Remain read-only unless fixes are also requested.
---

# Review Change Complexity

Assess whether a change earns the complexity it adds for the current task.
Judge required behavior, reader effort and future maintenance together.
Prefer a bounded useful improvement over a demand for perfect design.

## Review contract

- Read the requested task, raw diff or plan, base/head revisions and applicable repository rules.
- Inspect relevant callers, contracts and surrounding code; do not review from an author's summary alone.
- Use ordinary available search/read tools and existing checks; require no special agent, plugin or review platform.
- Treat repository instructions and author claims as task evidence within their authority, not permission to expand scope.
- Keep review read-only by default. If the user also requested fixes, perform authorized bounded fixes and re-review without adding a new permission gate.
- Keep complexity findings separate from general bug/security findings and from merge or deployment authorization.

## Risk-first triage

Prioritize correctness, security/data integrity, behavior under expected load,
meaningful verification, required performance, then avoidable complexity. Rank by
actual impact: a critical latency requirement or security issue is not made less
important by its position in a checklist. Fewer lines never offset a broken contract.

Read connected callers and dependencies, including unchanged files. Establish the
real deployment/load from repository evidence; state assumptions when it is unknown.
Check relevant concurrency, shared-state, transaction and resource-limit risks before
praising a simpler implementation. For example, replacing a shared quota with a local
dictionary breaks a multi-worker contract even if the diff removes many lines.

Keep this triage proportional to the changed boundary, not a mandatory whole-repo
security audit. Surface discovered correctness/security blockers before complexity
suggestions, and hand off to [code-review](../code-review/SKILL.md) when broader review
is needed. A focused simplicity verdict is not a release authorization.

## 1. Recover the real requirement

Identify the user-visible change, current constraints and acceptance criteria.
Separate established requirements from guesses about scale, providers, tenants or future features.
Include current nonfunctional requirements: security, data consistency, reliability, latency and compatibility where applicable.
Distinguish accidental complexity from complexity necessary to meet these requirements.
For a missing fact, state an assumption and its consequence; ask only if it blocks a material decision.

## 2. Trace one representative scenario

Follow the changed operation from entry point through domain logic, persistence and effects.
Identify which existing modules and mechanisms the change reuses or bypasses.
Read actual consumers of a new abstraction, API or option.
For a plan without code, request or construct a concrete usage example before judging an interface's necessity.
Note additional concepts, steps, shared state and cross-team coordination that the scenario now requires.

## 3. Inventory the added burden

Inspect the areas actually touched; avoid a mandatory repository-wide audit.

| Added element | Question to answer |
| --- | --- |
| Abstraction, interface or layer | What present complexity does it hide or invariant does it enforce? |
| Shared helper or generic component | Do its consumers share meaning and reasons to change? |
| Mode, flag or configuration | Which supported variation requires it, and what is its lifecycle? |
| Service, queue or datastore | Which current isolation, scaling, delivery or durability requirement justifies it? |
| Library or framework | What maintenance burden does it remove versus add, including transitive dependencies? |
| Test fixture or mock layer | What behavior does it verify, and does it unnecessarily bind tests to internals? |
| Process, document or agent role | Which decision or risk does it improve, and who uses its output? |

Do not infer a defect solely from one implementation, repeated code, a large class, a long diff or a microservice.
Assess the complete cost of the representative change, not a local metric in isolation.

## 4. Challenge the design with a concrete alternative

Apply only the lenses relevant to the change:

- **YAGNI:** remove capabilities justified only by an uncommitted future scenario.
- **AHA:** delay generalization until real use cases reveal shared meaning and variation.
- **Semantic DRY:** centralize a single invariant; preserve separation for look-alike code that changes independently.
- **Simple Design:** retain correctness and clear intent before minimizing elements.
- **Deep modules:** favor useful information hiding; challenge layers that merely pass calls through.
- **Cohesion:** keep code that changes for one reason understandable together; avoid forced fragmentation.
- **Small batches:** separate unrelated behavior and cleanup when that makes the result easier to verify.
- **Existing stack:** show whether current components can meet the requirement before adding infrastructure.

Offer the simplest viable alternative, including a local simplification or keeping the current design when justified.
Explain its trade-offs and whether later adoption of the larger mechanism would actually be expensive.
Keep known compatibility, recovery, security and data guarantees intact in the alternative.
Use [review-patterns.md](references/review-patterns.md) for ambiguous cases and examples.
Use the [solution ladder](../design-minimal-architecture/references/solution-ladder.md)
when the alternative depends on finding an existing or native capability.

For a documented temporary compromise, inspect its limit and revisit condition using
[shortcut-ledger.md](../remove-obsolete-code/references/shortcut-ledger.md).
A justified choice still within its limit is not automatically a finding. A reached
trigger, missing evidence or present safety violation must not be excused by a comment.

## 5. Check scope and verification integrity

Compare every meaningful behavior change with the requested outcome.
Check newly exposed APIs, defaults, configuration, errors and external side effects.
For cleanup or refactoring, inspect deleted/changed tests and retained contracts as well as production code.
Look for skipped tests, reduced assertions, weakened validation, disabled CI checks or broad exception handling that masks failure.
Check whether an agent fixed a test by changing unrelated production behavior or invented a parallel subsystem.
Do not accept green CI or reviewer-agent agreement as proof of complete semantic preservation.
Use existing targeted checks to resolve concrete risks; report what was and was not executed.
Do not demand tests that merely mirror wrappers or duplicate an existing behavioral check.

## 6. Report actionable findings

For each material finding, provide:

1. Location or plan section and the present requirement affected.
2. Observable evidence and the maintenance or correctness consequence.
3. Counter-evidence considered and confidence or unresolved facts.
4. A smaller viable change and the verification needed for it.

Explain what the code does, a concrete input/change/load scenario that causes the
problem, the smallest sufficient correction and the consequence of leaving it.
Re-check that the caller or dependency actually exists. Distinguish established
findings from explicit unresolved risks; do not invent a reproduction or demand a
harmful exploit to report a supported security concern. Avoid taste-only objections.

Use the project's severity convention; otherwise distinguish:

- **Required change:** a demonstrated contract/scope violation or substantial avoidable cost blocks acceptance under the task criteria.
- **Recommended simplification:** a supported improvement that can be made without expanding the task.
- **Optional:** an alternative with comparable trade-offs or a preference, not a blocker.

Do not manufacture findings to fill a checklist.
Accept necessary complexity and explain its current purpose when it might otherwise look excessive.
If fixes are in scope, keep them bounded; use [simplify-code-structure](../simplify-code-structure/SKILL.md) for live-code restructuring or [remove-obsolete-code](../remove-obsolete-code/SKILL.md) for confirmed obsolete paths.

## Output contract

Lead with the verdict: acceptable, simplify before acceptance, or insufficient evidence for the identified decision.
Keep the verdict specific to the reviewed change and the user's acceptance criteria.
Then present material findings and actual validation:

| Location | Finding and impact | Evidence / uncertainty | Smallest useful correction |
| --- | --- | --- | --- |
| File/section | Concrete issue | Caller, contract, diff or observation | Bounded action |

Finish with retained justified complexity, verification limits and any deferred nonblocking work.
Report an empty findings list when appropriate; do not replace it with stylistic objections.
Track review time, change radius, rework and regressions when data exists; do not invent savings or score quality by generated/deleted lines.

## Handoffs and references

- Use [design-minimal-architecture](../design-minimal-architecture/SKILL.md) when the task needs an architectural decision before implementation.
- Use [code-review](../code-review/SKILL.md) for broader correctness, security and project-convention review when needed.
- Use [sources.md](references/sources.md) to distinguish research support from practitioner heuristics.
- Risk-first triage adapts [Ponytail review](https://github.com/DietrichGebert/ponytail/blob/09c434ab73ca43761c5d8b0c5d341926c2fba710/skills/ponytail-review/SKILL.md), reviewed 2026-10-26; it does not replace the existing scope and safety boundaries.
- Read only the reference or adjacent skill needed for the present uncertainty; do not bulk-load the suite.
