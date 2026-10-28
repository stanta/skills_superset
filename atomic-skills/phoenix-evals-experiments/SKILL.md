---
name: phoenix-evals-experiments
description: Use to build Phoenix datasets, annotations and reproducible experiments for LLM prompt, agent, RAG, tool-calling, structured extraction and grounded evidence quality.
---

# Phoenix Evals and Experiments

Reuse [Agent Evals Lab](../agent-evals-lab/SKILL.md) for evaluation design; Phoenix is the execution and comparison environment, not the source of truth for business rules.

## Workflow
1. Establish an explicit failure taxonomy and quality measures before creating judges. Separate schema/JSON validity, entity matching, tool selection, evidence grounding, unsupported claims, completeness, latency and cost.
2. Assemble versioned datasets from sanitized real failures, synthetic edge cases and reviewed golden examples. Each case has inputs, optional reference output, tags, severity and expected behavior.
3. Prefer deterministic evaluators for schemas, IDs, exact evidence references, numerical constraints, permissions and tool contracts. Use LLM-as-Judge for subjective quality only, with documented rubric and human-reviewed calibration.
4. Run baseline and candidate against the same dataset and evaluator versions. Record prompt/model/release revisions, sampling parameters, result distributions, errors, missing cases, tokens and cost.
5. Inspect disagreements and low-confidence examples. Use human annotations to audit judge reliability; never treat a judge score as a legal, financial or data-integrity verdict.
6. Gate releases on correctness and security first, then compare task quality and operational cost. Promote confirmed regressions into the stable canary dataset.

## FD examples
- Structured brief → verified entity IDs, period, metrics and tool mapping.
- Spreadsheet cell provenance → only existing source coordinates with same-row linkage when demonstrated.
- Catalog unavailable vs not searched → distinct and accurate run outcomes.
- LangGraph restart/replay → idempotence, no duplicate tool effects.
- Unsupported metric and partial evidence → unverified, never automatically verified.

## Acceptance
- Baseline vs candidate use identical samples and rubric.
- Deterministic and judge metrics are not mixed into one unexplained score.
- Regressions and sampling/coverage limitations are visible.
- No production prompts or customer workbooks enter datasets without authorization.

## Sources
- https://arize.com/docs/phoenix/quickstart
- https://arize.com/docs/phoenix/evaluation/llm-evals/evaluator-traces
- https://arize.com/docs/phoenix/learn/datasets-and-experiments/datasets-concepts
