---
name: design-minimal-architecture
description: >-
  Choose the simplest sufficient architecture for current requirements and justify
  new services, layers, dependencies, stores, queues, or extension mechanisms.
  Use for architecture proposals, MVP design, modular-monolith versus services
  decisions, evolutionary design, or requests about overengineering, architecture
  bloat, YAGNI, KISS, оверинжиниринг, лишние слои, and упрощение архитектуры.
  Do not expand a routine local fix into a system-wide redesign.
---

# Design Minimal Architecture

Minimize the cost of understanding, changing, and operating the system while
meeting its actual requirements. Treat simplicity as a property of the whole
solution, including data, operations, coordination, and failure handling.

## Establish the decision

1. Read the task, relevant repository guidance, existing design decisions, and
   implementation around the affected use case before proposing components.
2. State the current problem, intended outcome, and scope in a few sentences.
3. Separate confirmed requirements, observed constraints, and assumptions.
   Preserve required security, data integrity, compatibility, availability,
   latency, recovery, and isolation properties as present requirements.
4. Identify the available evidence: current load, incidents, costly changes,
   release dependencies, measured bottlenecks, and known consumers.
5. Resolve missing facts from available code and context. Ask only when the
   answer materially changes correctness or an expensive commitment; otherwise
   state a bounded assumption and choose an appropriately reversible step.

For an analysis request, return a decision with evidence. For an implementation
request, carry the chosen change through the authorized implementation and
verification. Do not treat this skill as permission to deploy or delete data.

## Inspect before adding

- Find existing modules, platform capabilities, dependencies, and similar use
  cases. Prefer an appropriate existing mechanism when it already fits.
- Trace a representative request and data mutation through the current system.
  Record which boundaries and owners a typical change must cross.
- Name the actual pain: speculative functionality, coordination, leaking
  internals, repeated invariants, operational overhead, or another specific cost.
- Avoid inferring a need for distributed services from code size, imagined
  future popularity, or the number of agents available to write code.

## Run the solution ladder

Before adding a capability, follow the [executable ladder](references/solution-ladder.md):
avoid unnecessary work, reuse the project, check built-ins, reuse installed
capabilities, keep simple logic direct, then add the minimum missing implementation.
Stop at the first option that meets the complete current contract. Identify affected
callers, tests, fixtures, configuration and public/persisted formats before choosing.
Record a meaningful choice with its evidence and any exception, not a line-count quota.

For a material temporary compromise, record its limit, observable revisit condition
and upgrade path using the [shortcut ledger](../remove-obsolete-code/references/shortcut-ledger.md).
A compromise already outside its limit cannot be deferred as future work. Do not
introduce a new ledger process for ordinary permanent simple decisions.

## Compare the sufficient alternatives

Compare the simplest feasible option with the proposed additional machinery.
Add another option only when it changes the decision materially.

| Question | Evidence to provide |
| --- | --- |
| What requirement does the option satisfy? | A current use case, constraint, or demonstrated pain |
| What does it add? | Interfaces, state, runtime units, dependencies, configuration, or coordination |
| What does it remove or hide? | A concrete burden on callers, operators, or future changes |
| What does ownership cost? | Testing, deployment, upgrades, diagnosis, failures, and maintenance |
| What does postponing it cost? | A plausible later migration, including data and consumers |
| What would change the choice? | Observable demand, constraint, or measured threshold |

Do not turn uncertain estimates into a numeric architecture score. Distinguish
measured facts from expectations and explain the deciding tradeoff.

## Choose boundaries that earn their cost

1. Keep required domain invariants and changeable implementation details behind
   clear boundaries. Prefer a small interface that hides substantial complexity.
2. Use cohesive modules or a modular monolith where they satisfy current needs.
   Introduce a separate process or service for a demonstrated need such as
   independent release, workload scaling, isolation, or separate ownership.
3. Preserve real isolation requirements even when an in-process alternative has
   fewer components. A distributed design is appropriate when its benefits pay
   for network failures, consistency, operations, and coordination costs.
4. Justify every new layer by the responsibility or knowledge it encapsulates.
   Inspect pass-through wrappers; retain those that enforce an actual contract.
5. Justify new technologies against the current stack and its operating skills.
   If replacing a capability, include how the old path will be retired.
6. Add extensibility for known variation. Keep a simple seam when it cheaply
   enables change; avoid unused modes, speculative integrations, and framework
   machinery for requirements that have not materialized.

Use [decision patterns](references/decision-patterns.md) for borderline cases
involving services, dependencies, extension points, and irreversible choices.

## Make the decision evolvable

- Defer a commitment while useful alternatives remain open and the delay does
  not jeopardize a known requirement. State the latest useful decision point.
- Investigate hard-to-reverse data models, public contracts, and isolation
  decisions early enough to avoid an emergency migration.
- Use a bounded spike only to resolve a named uncertainty. Define what evidence
  ends it; do not silently promote experimental scaffolding into production.
- Preserve the ability to refactor through clear boundaries and relevant tests.
  YAGNI does not justify neglecting the ability to change the code safely.

## Deliver and verify a small slice

1. Choose a coherent, reviewable increment with one observable purpose.
2. For a new system, exercise a thin end-to-end path through its real entry
   point, domain behavior, data, and delivery process before building a platform.
3. Include new interfaces with a real consumer or a concrete required contract.
   Identify external behavior that remains simulated or unverified.
4. Reuse existing verification. Add an architectural fitness check only for a
   required property and concrete risk, such as a prohibited dependency cycle,
   compatibility contract, performance limit, or isolation boundary.
5. Record a short ADR for a consequential choice; include context, alternatives,
   decision, consequences, and revisit conditions. Do not require one for a
   routine implementation choice.
6. Check the implemented boundaries and behavior against the decision. Report
   actual verification separately from proposed future checks.

## Return the decision

Report the problem and selected design first, followed by:

- why the simplest alternative is sufficient or where it fails;
- which new entities earn their cost and which assumptions remain deferred;
- the required properties preserved and the verification performed;
- the next coherent increment and observable conditions for reconsideration.

Use representative change effort, release coordination, and operating burden to
assess the result. Treat counts of lines, classes, and services as diagnostic
signals, not optimization targets. Present these practices as contextual
heuristics; consult [sources](references/sources.md) for their evidence limits.

## Route the next task

- Use [simplify-code-structure](../simplify-code-structure/SKILL.md) for local
  abstraction and module-boundary changes that preserve behavior.
- Use [remove-obsolete-code](../remove-obsolete-code/SKILL.md) when the main task
  is proving obsolescence and retiring code, flags, or dependencies.
- Use [review-change-complexity](../review-change-complexity/SKILL.md) for an
  independent assessment of a concrete diff. Load only the relevant skill.
