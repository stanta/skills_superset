---
name: test-driven-development
description: "Test-first development of behavior changes while preserving existing code, evidence and unrelated user work."
---

# Test-Driven Development

## Safety and applicability

Prefer RED → GREEN → REFACTOR for a new feature or defect fix. **Never delete existing code, user changes or git history merely because tests were written later.** Tests-first is a means to produce evidence, not a license to discard work.

Read the requirement, current diff, connected callers and existing tests. Choose the cheapest meaningful layer: unit for pure rules, contract for interfaces, integration for stateful dependencies, thin E2E for critical journeys.

## Workflow

1. **Define the oracle.** Record a concrete input, independently sourced expected behavior, constraints and a bug the test should catch. Never derive the expectation solely from current implementation.
2. **RED.** Run a focused behavioral check and observe the expected failure; distinguish it from setup/import errors. Existing incident reproductions and failing regression checks count as RED evidence.
3. **GREEN.** Implement the smallest safe change, asserting observable outcomes and effects instead of a mocked return value.
4. **REFACTOR.** Remove duplication or unnecessary abstractions only with the relevant tests remaining green.
5. **VERIFY.** Run focused and regression checks. Record commands, outputs, skipped checks, versions and limitations before claiming success.

For **legacy code** where tests follow implementation, add characterization tests protecting required existing behavior. When safe, demonstrate that tests detect a controlled defect/mutation or relevant prior revision. Do not delete working code to manufacture a RED phase. If a failure cannot be reproduced, document the gap and use appropriate alternative verification.

## Guardrails

- Cover success, boundary, error, unauthorized and recovery paths proportionate to risk.
- Never weaken assertions, mutate fixtures, skip tests or swallow exceptions solely to obtain green output.
- Avoid tests that assert only mock wiring, identical generated expectations or implementation details.
- Keep expected outcomes in reviewed specifications or evaluator-owned checks for critical agent behavior.
- Mutation/property-based checks help challenge the oracle; exclude equivalent mutations from diagnostic conclusions.
- Do not add test frameworks, helpers or generic layers without current need.
- Ask for input only when an unknown requirement blocks a material decision; preserve unrelated work.

Use [verification-before-completion](../verification-before-completion/SKILL.md) to verify completion claims and [tester-ai](../tester-ai/SKILL.md) for agent-specific tests.
