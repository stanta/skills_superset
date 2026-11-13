---
name: multi-step-reasoning
description: "Compose complex LLM tasks into minimal typed stages with evidence handoffs, stage tests and end-to-end evaluation; maps to DSPy Module and predictor composition."
license: MIT
---

# Multi-Step Reasoning

Decompose a task only when explicit stages improve correctness, observability or control. More steps and more agents are not intrinsically better reasoning.

## When to use

Use when a single call mixes incompatible tasks, loses evidence or has untestable intermediate decisions. A straightforward transformation with a reliable single-call baseline should remain single-step.

## Inputs

Obtain the final acceptance criteria, available evidence/tools, typed input/output contracts, baseline failures, latency/cost limits and execution permissions. Identify which work is deterministic and should not use a model.

## Procedure

1. Start with the smallest adequate baseline. Map the observed failure to a distinct responsibility such as extraction, retrieval, calculation, verification or presentation.
2. Draw a minimal dependency graph. Give each stage typed inputs, outputs, invariants and error/abstention behavior. Keep policy/authorization checks outside generated reasoning.
3. Pass only necessary evidence and stable source IDs between stages. Separate observations, hypotheses and verified results; never upgrade an intermediate guess into a fact.
4. Unit-test each stage and all handoff contracts. Add end-to-end cases for error propagation, missing evidence and contradictory intermediate results.
5. Execute independent stages concurrently only when allowed tools, state ownership and budgets make it safe. Bound loops and total nested calls; preserve failure statuses.
6. Evaluate the composed pipeline against the single-call baseline. Ablate stages to identify what actually helps; remove a stage that adds cost without useful evidence.
7. Return the final result with a concise decision/evidence summary and unresolved issues. Explanatory text is not proof that the computation or tool action occurred.

## Deliverable and acceptance

Provide the stage graph, contracts, minimal implementation plan, stage/end-to-end tests and measured trade-offs or an explicitly unrun experiment. Keep source provenance intact across the whole graph.

## Safety

Do not request or disclose private chain-of-thought. Use structured intermediate artifacts and short justifications suitable for auditing. Do not delegate permissions or production actions merely because a planner proposes them.

Read [DSPy composition patterns](references/playbook.md). Handoff to [task-contract-designer](../task-contract-designer/SKILL.md) for schemas and [llm-eval-engineer](../llm-eval-engineer/SKILL.md) for measurement. See [evaluation cases](evals/cases.json).
