# Task evaluation playbook

## Minimum run record

Record `run_id`, artifact hash, task/schema version, dataset/split hashes, scorer version, model/provider revision, decoding options, tool permissions, dependency versions, cache mode and timestamp. Per case retain ID, prediction or error status, score components, hard-failure flags, source IDs, latency and usage. Do not retain sensitive raw content merely because a trace facility supports it.

## Metric design

For extraction, score required fields and unsupported additions separately. For a reviewer, report critical-miss rate and false-positive rate, not accuracy alone. For retrieval, distinguish evidence availability from answer faithfulness. For abstention, measure both justified refusal and avoidable non-answering. Missing predictions and infrastructure failures require visible accounting; an incomplete run cannot pass a release gate.

DSPy `Evaluate` can run a program against a development set and metric. Match the metric return type to the installed API. Keep a numeric evaluation wrapper separate from an optimizer's score-plus-feedback adapter. Verify aggregate scale before comparing a percentage with a normalized score.

## Comparison

Declare non-inferiority margins and critical slices before seeing results. Use paired case IDs and repeated runs; summarize uncertainty using a suitable paired bootstrap or an explicitly justified alternative. With insufficient evidence, return inconclusive rather than selecting the highest noisy point estimate. Keep test labels unavailable to optimization.

## Sources

Checked 2026-11-13; original repository workflow with an optional DSPy adapter.

- Evaluate: https://dspy.ai/current/api/evaluation/Evaluate/
- GEPA metric interface: https://dspy.ai/current/diving-deeper/gepa-in-depth/

Use the project's existing runner and the adjacent `agent-evals-lab` comparison protocol rather than duplicating infrastructure.
