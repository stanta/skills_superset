# Minimal staged programs

## Example decomposition

A document-answer task might use `retrieve -> extract supported facts -> deterministic calculation -> compose answer -> verify citations`. This is an example, not a required architecture. Collapse stages when one typed call meets the acceptance criteria. Do not create an agent persona for work a normal function can perform.

For every edge define field names, units, source IDs, trust level and error handling. An upstream timeout must not become an empty value interpreted as a negative finding. A downstream stage must be able to abstain when evidence is absent.

## Optional DSPy implementation

A `dspy.Module` can compose predictors and ordinary Python control flow. `Predict` is the simple baseline; `ChainOfThought` is a strategy option, not a correctness guarantee or authorization mechanism. Use typed outputs and verified artifacts for audit rather than depending on private provider reasoning. Verify async/parallel APIs in the installed release before using them.

Measure end-to-end success as well as per-stage scores: individually accurate stages can still fail through incompatible assumptions. Compare with the simpler baseline under the same input, permission and budget constraints. Record retries and nested calls in total latency/cost.

## Sources

Checked 2026-11-13; original decomposition workflow.

- https://dspy.ai/current/api/modules/Module/
- https://dspy.ai/current/api/modules/ChainOfThought/
- https://dspy.ai/current/getting-started/composing-modules/

Use ordinary host capabilities when DSPy is absent; no multi-agent runtime is required.
