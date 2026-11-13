# Bounded prompt search

## Choose the editable surface

Keep architecture and task semantics fixed for a prompt experiment. Record which predictor names may change and compare the optimized program, not only the prettiest resulting instruction. Use a small demonstration baseline before expensive search.

DSPy MIPROv2 searches instruction/demo configurations; supply explicit trainset and valset rather than assuming its internal split matches the project's leakage policy. GEPA uses evaluation feedback to propose changes. Its feedback metric has additional context arguments beyond a basic evaluation metric; inspect the installed signature and use a compatible score/feedback object. Do not pass a feedback dictionary to a numeric aggregation path without an adapter.

## Budget and persistence

A trial cap is not a currency cap. Enforce a separate application/provider usage ceiling and stop when remaining budget cannot cover another evaluation. Keep a ledger for task, proposal, reflection and judging calls. Re-running cached predictions is not a new stochastic trial.

Save a JSON program state where supported, together with the Python module source, dependency lock, model configuration, dataset/scorer hashes and artifact checksum. State alone is not a complete deployment. Restore only trusted artifacts and test a clean reload before promotion.

## Failure probes

Reject a winner that learned a test answer, removed an abstention state or reduced a critical slice while raising the average. With no improvement, keep the baseline and report the search cost. No paid run is implied by reading this skill.

## Primary sources

Checked 2026-11-13; locally authored workflow, not an upstream skill.

- https://dspy.ai/current/diving-deeper/gepa-in-depth/
- https://dspy.ai/current/api/optimizers/MIPROv2/
- https://dspy.ai/current/api/optimizers/BootstrapFewShot/
