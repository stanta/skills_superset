---
name: ai-regression-gate
description: "Gate changes to prompts, models, tools or AI pipelines using frozen baseline/candidate evaluations, critical-slice checks, artifact provenance and explicit pass/fail/inconclusive decisions."
license: MIT
---

# AI Regression Gate

Decide whether evaluation evidence supports promotion of a specific AI artifact. This gate consumes evaluation results; it neither tunes the candidate nor grants production authority.

## When to use

Use before promoting a changed prompt, demonstrations, model, retrieval configuration, tool policy or generated architecture. For creating the evaluation suite itself use [llm-eval-engineer](../llm-eval-engineer/SKILL.md) or the existing [agent-evals-lab](../agent-evals-lab/SKILL.md).

## Inputs

Require immutable baseline/candidate identifiers, comparable case-level results, split/scorer/configuration hashes, predeclared thresholds and non-inferiority margins, critical-case labels, cost/latency limits and rollback metadata.

## Procedure

1. Verify artifact identity and evaluation provenance. Reject mismatched datasets, missing cases, changed graders, incompatible measurement scales and stale or incomplete results.
2. Check that test cases were not used for prompt search, demonstrations, reflection or candidate selection. A contaminated holdout requires a new untouched evaluation.
3. Apply hard gates first: authorization violations, critical omissions, data leakage, schema/contract breaks and required abstention behavior. Average quality cannot compensate for a critical failure.
4. Compare paired outcomes and important slices with the declared margins. Account for repeated trials and uncertainty; insufficient sample size is inconclusive, not evidence of equivalence.
5. Check cost, tail latency, error rate and dependency/model changes. Verify a trusted artifact reload and the operational rollback path where execution is available.
6. Emit `pass`, `fail` or `inconclusive` with machine-readable reasons and evidence links. Missing mandatory evidence fails closed for automatic promotion even when the analytical verdict is inconclusive.
7. Hand the report to the independent release/authorization mechanism. Preserve approval requirements and a monitor/rollback plan; a passing evaluation is not a deployment command.

## Deliverable and acceptance

Return a decision record tying the verdict to exact artifact hashes, thresholds, slice outcomes, uncertainty and unresolved checks. Explicitly separate structural validation, executed behavioral evaluation and deployment approval.

## Safety

The candidate and optimizer cannot edit the gate, labels, tolerances or authorization policy. Do not infer an unobserved test result, bypass CI, deserialize untrusted executable artifacts or approve yourself as an independent reviewer.

Read [gate record and DSPy persistence notes](references/playbook.md) and [evaluation cases](evals/cases.json).
