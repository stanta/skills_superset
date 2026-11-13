---
name: self-refinement
description: "Improve an individual LLM result through bounded candidate selection or feedback-driven revision using external checks; maps to DSPy BestOfN and Refine."
license: MIT
---

# Self-Refinement

Improve a result at inference time without confusing model self-confidence with correctness. Do not use this skill to run an unlimited autonomous improvement loop.

## When to use

Use for a draft that can be checked against a rubric, schema, executable test or retrieved evidence, or when a bounded best-of-N strategy is justified. For persistent prompt changes across tasks, use [prompt-optimizer](../prompt-optimizer/SKILL.md).

## Inputs

Require the original request/evidence, first candidate, independent checks, maximum attempts, cost/time limits and failure/abstention behavior. Confirm that tools used during attempts are read-only or safely mocked.

## Procedure

1. Validate the first candidate and preserve it. Classify defects as format, factual, completeness, constraint or execution failures.
2. Choose independent candidate sampling when selection is enough; choose iterative revision when specific feedback can guide a repair. Do not apply both by default.
3. Define a reward/check that cannot be satisfied merely by adding confident wording. Put hard safety and schema constraints before a soft quality score.
4. Generate only within the explicit attempt and usage budget. Feed minimal actionable feedback plus original evidence; do not turn a previous unsupported answer into a trusted source.
5. Validate every candidate independently. Track the best valid candidate, not automatically the newest one. Stop on a predeclared acceptance threshold, exhausted budget or repeated non-progress.
6. Recheck the selected output against original requirements and evidence. If none qualifies, return a labeled partial result, abstain or request the missing input.

## Deliverable and acceptance

Return the selected result, a concise correction summary, checks actually run, attempt count, usage and remaining limitations. Do not expose private reasoning traces or represent repeated agreement as independent evidence.

## Safety

Retries must not repeat a payment, release, notification or other side effect. Separate result generation from execution and require normal authorization after selection. Keep validators immutable and never relax a safety rule to reach the threshold.

Read [BestOfN/Refine mapping and failure handling](references/playbook.md). For release-level comparisons use [ai-regression-gate](../ai-regression-gate/SKILL.md). See [evaluation cases](evals/cases.json).
