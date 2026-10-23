---
name: simplify-code-structure
description: >-
  Simplify working code by repairing premature abstractions, leaking module
  boundaries, duplicated business rules, pass-through layers, and excessive
  coupling while preserving required observable behavior. Use for structural
  refactoring, AHA, semantic DRY, deep modules, vertical slices, functional core,
  code bloat, упрощение кода, лишние абстракции, and чрезмерная связанность.
  Do not turn a local refactor into a framework rewrite or dead-code purge.
---

# Simplify Code Structure

Reduce the effort needed to understand and change an identified part of the
system. Keep the public behavior and required properties intact. Choose a
structural change because it removes a demonstrated cost, not to satisfy a
preferred number of classes, layers, parameters, or lines.

## Define a bounded refactor

1. Read the task, repository guidance, affected code, consumers, and tests.
2. Name the specific difficulty: scattered knowledge, accidental shared logic,
   leaking internals, pass-through layers, or tangled side effects.
3. Trace one representative use case and identify which changes currently
   propagate across unrelated components.
4. State the allowed scope and expected improvement. Resolve context from the
   repository; ask only when a missing requirement changes the safe action.
5. Treat analysis-only requests as analysis. For implementation requests, make
   and verify the authorized change rather than stopping at recommendations.

Read [refactoring patterns](references/refactoring-patterns.md) for ambiguous
cases before choosing a transformation.

## Establish behavior that must survive

Record the relevant public inputs, outputs, errors, side effects, and contracts.
Include transaction boundaries, authorization, ordering, idempotency, concurrency,
compatibility, and performance when they are part of the current requirements.

- Reuse relevant existing tests and executable examples.
- Add focused characterization tests when a concrete behavioral uncertainty
  prevents safe refactoring; avoid tests that merely mirror the new structure.
- Identify known failing checks before editing so pre-existing failures remain
  distinguishable from regressions.
- Keep requested behavior changes explicit and separable from structural work.
  Report newly discovered unrelated defects rather than silently expanding scope.
- Do not treat passing tests as proof of every contract; inspect uncovered
  consumers, state transitions, and boundary behavior where the change touches them.

## Diagnose the responsibility, not the shape

| Symptom | Question to resolve |
| --- | --- |
| Similar code in several places | Does one rule require coordinated changes, or are separate rules coincidentally alike? |
| A shared helper gains modes | Are the variants one stable concept or different responsibilities forced together? |
| Many tiny classes or wrappers | What meaningful knowledge or policy does each interface hide? |
| A small feature touches many layers | Would grouping along the use case reduce unrelated coupling? |
| Business rules require extensive mocks | Can deterministic decisions be separated from external effects? |
| A reusable utility has many dependents | Does it centralize a real invariant or spread accidental coupling? |

Do not classify a parameter, conditional, single implementation, or repeated
fragment as a defect by itself. Read its actual callers and reasons to change.

## Select the smallest useful transformation

### Apply AHA and semantic DRY

1. Keep one authoritative representation of knowledge that must change together.
2. Allow similar but independently changing behavior to remain separate.
3. If a shared abstraction mixes unrelated variants, inline it into its callers,
   remove the branches irrelevant to each caller, then reassess common knowledge.
4. Extract a shared abstraction when the real invariant and variation are clear.
   Use the rule of three as a reminder to learn, never as a required count.
5. Avoid introducing unused options or inheritance to predict future consumers.

### Improve information hiding

- Give a module a clear responsibility and a small interface that hides actual
  complexity. Make necessary internal details private to that responsibility.
- Remove or combine forwarding layers only after checking for policies such as
  access control, transactions, retries, observability, and compatibility.
- Keep an interface with one implementation when it provides a useful boundary.
  Do not add one solely to make a diagram symmetrical or enable a mock.
- Avoid replacing class fragmentation with a module that owns unrelated concepts.

### Align structure with change

- Group a use case's collaborating logic when it reduces changes across unrelated
  layers. Preserve shared domain invariants and required cross-cutting policies.
- Select a simple transaction script or richer domain model per actual need;
  do not impose a generic repository or framework on every scenario.
- Move deterministic decisions into pure functions where useful, leaving I/O
  in a clear shell. Preserve transaction consistency, side-effect ordering,
  concurrency semantics, and resource limits across that boundary.
- Prefer language and project idioms that make intent discoverable. Check whether
  callers can predict behavior without learning implementation details.

## Implement and verify incrementally

1. Make one coherent structural change with its affected callers and checks.
   Separate mechanical moves from behavior changes when that aids review.
2. Use existing refactoring tools for reliable mechanical edits where available.
   Inspect dynamic lookup and external consumers before changing public names.
3. Run the relevant tests and other required checks after the change. Add broader
   verification only to address a concrete remaining risk or repository gate.
4. Preserve checks for surviving requirements. Adjust fixtures when dependencies
   change, but do not remove or weaken a test merely to obtain a green result.
5. Review the diff for changed contracts, duplicated invariants, unnecessary
   helpers, new dependencies, and abandoned intermediate scaffolding.
6. Stop when the identified difficulty is resolved. Leave unrelated cleanup and
   speculative redesign outside the change.

## Report the result

State the structural problem, what changed, which behavior was preserved, and
what verification ran. Include any material uncertainty or unverified contract.

Compare the representative use case before and after: knowledge needed, boundaries
crossed, coordinated edits, and review effort. Label anticipated savings as
expected; do not claim measured improvement from shorter code alone.

Treat AHA, DRY, simple design, CUPID, and deep modules as complementary contextual
heuristics. Consult [sources](references/sources.md) for attribution and limits.

## Route the next task

- Use [design-minimal-architecture](../design-minimal-architecture/SKILL.md) when
  the decision concerns services, technologies, or system-wide boundaries.
- Use [remove-obsolete-code](../remove-obsolete-code/SKILL.md) when proving that
  behavior, a flag, or a dependency can be retired is the main difficulty.
- Use [review-change-complexity](../review-change-complexity/SKILL.md) for an
  independent review of the finished diff. Load only the relevant skill.
