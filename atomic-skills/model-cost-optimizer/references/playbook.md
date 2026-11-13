# Cost-quality comparison

## Accounting

For a fixed workload, cost per successful task is total billable cost divided by the number of tasks meeting the frozen acceptance criteria. Include failed attempts and fallbacks in the numerator. With zero successes, mark the quantity undefined/infinite rather than reporting zero.

For a two-stage cascade, estimate cheap-stage cost plus fallback probability times the full fallback cost, adding routing, retrieval and verification costs. Validate this estimate with actual traces and tail latency. A router's uncertainty score needs calibration; a confident error can bypass the fallback.

Break-even requests equal one-time optimization cost divided by per-request savings only when savings are positive and the workload/pricing assumptions remain valid. Distinguish measured, provider-billed and estimated values. Refresh price references at execution time; this skill intentionally embeds no model price table.

## DSPy integration

Use `dspy.LM` and scoped model configuration to compare explicitly chosen models. Optimizers can adapt instructions/examples for a candidate model; they do not automatically enforce price, data residency, latency or safety constraints. Persist the selected model and configuration with the program artifact. Benchmark cache-enabled and cache-disabled conditions separately.

## Primary sources

Checked 2026-11-13. Cost formulas and gate design are this repository's engineering procedure.

- https://dspy.ai/current/api/models/LM/
- https://dspy.ai/current/diving-deeper/gepa-in-depth/

Consult current provider pricing and the installed DSPy API only when running an actual experiment.
