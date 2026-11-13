# Demonstration curation

## Selection record

For each example record training ID, source permission, task version, label source, validation result, error category, token size and inclusion rationale. Keep the raw source outside the reusable skill package. Never use an evaluation case's expected answer as a production demonstration.

A compact set can include a representative success, a difficult boundary, missing evidence with abstention and a format edge case. Class balance and diversity depend on the actual task; do not turn an illustrative count into a universal requirement.

## DSPy adapter

`LabeledFewShot` uses labeled examples; `BootstrapFewShot` can collect demonstrations from successful program executions filtered by a metric. Configure the demonstration and bootstrapping limits explicitly and inspect what was retained. A weak metric can accept incorrect teacher outputs, so independently review high-risk examples. BootstrapFewShot is a prompt/demo optimizer, not model-weight training.

## Ablation

Compare no examples, labeled examples and bootstrapped examples under a fixed token/latency envelope. Test order effects and remove an example when it adds cost without reliable benefit. Group splits by source document, incident or user to reduce near-duplicate leakage. Keep generated outputs and failure reasons in the training ledger, not in test feedback.

## Source

Checked 2026-11-13. Original selection procedure informed by the DSPy optimizer interfaces:

- https://dspy.ai/current/api/optimizers/BootstrapFewShot/
- https://dspy.ai/current/api/optimizers/LabeledFewShot/

Recheck installed constructor and compile signatures before implementation.
