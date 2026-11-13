---
name: llm-eval-engineer
description: "Build reproducible task-level LLM evaluations: leakage-safe datasets, scoring functions, error slices, repeated trials and DSPy Evaluate adapters."
license: MIT
---

# LLM Evaluation Engineer

Create the measurement contract needed before optimizing an AI component. Reuse the project's existing evaluation runner; do not build a benchmark platform just to score one task.

## When to use

Use for a new task metric, an unreliable judge, missing baseline, train/test leakage or a proposed DSPy optimization. For organization-wide agent evaluation operations, use the existing [agent-evals-lab](../agent-evals-lab/SKILL.md). For deciding whether an already evaluated candidate may ship, use [ai-regression-gate](../ai-regression-gate/SKILL.md).

## Inputs

Obtain the task contract, baseline artifact, representative authorized data, expert labels/rubric, failure severity and call/cost limits. Without labels or an adequate judge, deliver a measurement plan and evidence gap rather than an improvement claim.

## Procedure

1. Define the unit of evaluation and observable success. Separate correctness, evidence support, abstention, safety, cost and latency; hard failures must not be averaged away.
2. Create stable case IDs and provenance. Deduplicate before splitting; group related users, documents or incidents together. Use chronological splits when evaluating future-facing tasks.
3. Freeze train, validation and held-out test manifests. Optimizers may use train/validation only; test cases and labels never enter prompts, demonstrations or reflection feedback.
4. Prefer deterministic validators where possible. Calibrate any model judge against human-reviewed examples, blind candidate identity and test answer-order/verbosity bias.
5. Run baseline and candidate on identical allowed inputs, permissions and budgets. Retain timeouts, malformed outputs, refusals and tool errors in denominators with explicit statuses.
6. Report per-case outcomes, important slices, sample sizes and uncertainty. Use repeated trials for stochastic behavior and a paired comparison where applicable.
7. Save the dataset, rubric, model, configuration, code and dependency identifiers. Record cache policy and actual usage; seeds alone do not guarantee reproducibility.

## Deliverable and acceptance

Produce an evaluation specification, case manifest, scorer, baseline report and reproducible run instructions. State whether checks were designed, structurally validated, smoke-tested or behaviorally executed. A small passing dataset is not a safety guarantee.

## Safety

Use only authorized/redacted data and approved endpoints. Cap paid model calls explicitly. An optimizer cannot edit the judge, labels, test split or hard safety policy to increase its score.

Read [evaluation implementation](references/playbook.md) and [case specifications](evals/cases.json) as needed. Use [task-contract-designer](../task-contract-designer/SKILL.md) if success is not yet well defined.
