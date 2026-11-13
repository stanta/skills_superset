---
name: model-cost-optimizer
description: "Reduce total LLM task cost through measured model/prompt comparisons, caching and bounded routing while preserving predefined quality, safety and latency constraints."
license: MIT
---

# Model Cost Optimizer

Minimize cost per acceptable task outcome, not advertised cost per token. Model selection is an explicit experiment around DSPy or another runtime, not a built-in promise of automatic cheapest-model discovery.

## When to use

Use when an existing AI task has measured usage/cost and a quality contract. Do not recommend a cheaper model based only on its name, benchmark score or remembered pricing.

## Inputs

Require the baseline and workload distribution, frozen evaluation cases, mandatory quality/safety thresholds, latency limits, allowed providers/data regions, current price sources and optimization budget.

## Procedure

1. Measure input/output tokens, retries, tool calls, judge/refinement costs and end-to-end latency. Separate cold/warm cache behavior and billable versus estimated usage.
2. Build a small candidate matrix of allowed models and prompt/demo configurations. Verify current availability, capabilities, pricing units and data-handling constraints.
3. Test each candidate under equivalent conditions. Model changes may require separate prompt calibration on train/validation, not unrestricted use of the test set.
4. Reject candidates violating hard quality, critical-slice, safety or latency constraints before ranking costs. Treat an underpowered evaluation as inconclusive.
5. Consider prompt trimming, batching, safe caching or a simple routing cascade only when measurements justify it. Preserve tenant/privacy boundaries in cache keys and storage.
6. Include fallback probability and duplicate work in expected cost. Evaluate the full cascade, including router errors and outages, rather than only its cheapest path.
7. Calculate optimization break-even under explicit workload assumptions. Save a versioned configuration and rollback path; deploy only through normal approval.

## Deliverable and acceptance

Return the candidate matrix, quality/error slices, latency distribution, current price assumptions, cost per successful task and keep/change/inconclusive recommendation. Report currency and measurement date. Do not invent savings or claim equivalence from a few favorable examples.

## Safety

A low price does not authorize sending private data to a new provider. Bound experiments and use approved endpoints. Do not reduce safety checks, hide failed attempts or substitute stale cached facts to appear cheaper.

Read [cost accounting and DSPy mapping](references/playbook.md). Use [llm-eval-engineer](../llm-eval-engineer/SKILL.md) and [ai-regression-gate](../ai-regression-gate/SKILL.md). See [evaluation cases](evals/cases.json).
