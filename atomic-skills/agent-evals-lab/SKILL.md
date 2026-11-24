---
name: agent-evals-lab
description: "Design versioned, risk-based evaluations for agent outcomes, tool actions, system state and skill comparisons."
---

# Agent Evals Lab

Assess **final outcome**, **permitted action trajectory** and **resulting system state** separately. Do not treat beautiful final text, a structural CI check or model self-rating as proof of correctness.

## Workflow

1. Freeze the requirement, initial state, available tools, action permissions, critical risks and independent expected outcome.
2. Build versioned canary, golden, chaos, adversarial and held-out cases. Prevent training/test leakage and retain provenance.
3. Prefer deterministic checks for permissions, schemas, numeric rules, side effects and mandatory orderings. Use calibrated, blinded semantic judges only when objective checks are insufficient, with human review for critical disagreement.
4. Record every attempt: pass, fail, blocked, timeout, infrastructure/grader error; never drop costly or failed runs from denominators.
5. Gate safety, correctness and completeness before comparing quality, latency, code size and tokens.
6. Turn sanitized production incidents into stable regression cases.

Use the [shared evaluation contract](references/agent-test-contract.md) for cases/results and its small deterministic pilot. The pilot validates evaluator behavior; it is **not** a model/skill performance result.

## Skill comparison

Reuse the [controlled baseline/current/candidate protocol](references/skill-comparison.md) and the [case specifications](references/simplicity-cases.json). Keep tasks, tools, limits, model settings and environment comparable; isolate state; validate actual skill loading; preserve failures and hidden evaluator-owned checks. Include negative controls where extra complexity is justified.

Describe evidence correctly as **specified**, **structurally validated**, **smoke-tested**, or **behaviorally benchmarked**. Without an authorized executable agent runner, document the unrun comparisons rather than inventing improvements.
