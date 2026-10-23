# Architecture Decision Patterns

Use these patterns to test a proposal against current requirements. Select the
smallest relevant example; do not combine them into a mandatory architecture.

## Require a concrete reason for additional machinery

| Proposal | Start with | Escalate when | Check the hidden cost |
| --- | --- | --- | --- |
| Split a service | Cohesive in-process modules | Independent release, scaling, ownership, or isolation is actually required | Network errors, observability, consistency, contracts, on-call burden |
| Add a broker | The existing synchronous or scheduled mechanism, if it meets requirements | Durable asynchronous work, retries, backpressure, or delivery semantics require it | Idempotency, ordering, poison messages, recovery, operations |
| Add a generic engine | The current concrete use cases | Known independent consumers need stable shared semantics | Configuration language, debugging, versioning, special-case branches |
| Add another store | Existing storage capabilities | Its constraints demonstrably prevent required behavior or acceptable cost | Synchronization, backups, migrations, access control |
| Add an adapter | A direct boundary call or a small adapter | The adapter hides a real protocol, error policy, authorization, or contract | Pass-through surface, leakage, unnecessary configuration |

Do not equate fewer runtime units with a cheaper system. For example, mandatory
tenant isolation can justify separate deployments before traffic becomes large.
Conversely, separate teams do not automatically require a service for each
technical layer; inspect the actual release and ownership boundaries.

## Compare a proposed abstraction with adding it later

For a single external integration, describe the work needed to introduce a
second provider later. Keep a small boundary now if it hides current protocol
details. Defer a plugin registry and provider-neutral configuration language
until actual variants require them. Accept a broader interface now when it is
already simpler for current callers and does not add unused behavior.

## Investigate expensive commitments early

| Choice | Useful evidence before committing |
| --- | --- |
| Public event or API shape | Consumer contracts, versioning, active clients, compatibility obligations |
| Data partitioning or identity model | Invariants, isolation, access paths, migration and recovery feasibility |
| Specialized dependency | Required capability, maintenance state, operational fit, replacement cost |
| Local implementation detail | Existing idioms and relevant tests; often choose and revise directly |

Delay decisions only while the delay preserves viable alternatives. Do not use
"decide later" to ignore a migration lead time or a required release constraint.

## Choose the first vertical slice

Pick one meaningful operation with input validation, domain behavior, persistent
effects, and an observable result. Exercise its delivery and failure path using
the current platform. Keep any stubbed external behavior explicit. Extend the
slice after learning where complexity is actually needed.

Do not interpret the skeleton as the final design or an exemption from required
authorization, data correctness, or recovery behavior.

## Keep an ADR proportional

For a significant decision, record: problem and constraints; feasible options;
selected option; costs and consequences; implementation boundary; evidence or
condition that would trigger reconsideration. Keep this near the code using the
repository's existing convention. Record ordinary choices in the change
description when a separate ADR adds no value.

## Separate facts from heuristics

Describe a measured bottleneck as measured. Label projected traffic, future
consumer demand, and expected maintenance savings as assumptions. Do not claim
that a preferred architecture will provide a percentage improvement without
comparable measurements. Check whether the next representative change or release
actually requires less coordination after the design has been used.
