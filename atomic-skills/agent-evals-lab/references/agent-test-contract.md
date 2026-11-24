# Shared AI-agent test case and run contract (v2)

This is the portable contract used by `tester-ai`, `agent-evals-lab`, `verification` and skill comparisons, **not** a model runner or proof of deployment readiness.

## Case: evaluator-owned, versioned and frozen before execution

- `id`, `requirement`, `initial_state`, `dataset_version`: nonblank identifiers and a referenced initial-state fixture.
- `kind`: `positive`, `negative`, `chaos` or `adversarial`; `split`: `development` or `holdout`.
- `allowed_actions`, `forbidden_actions`, `required_actions`: lists of tool names. A required action must be allowed. Specific authorization of arguments can use optional `argument_rules`: `{"tool.name":{"argument":["approved-value"]}}`. Only equality against listed scalar values is built in; use a separately reviewed check for complex authorization rules.
- `action_limits`: optional maximum invocation count per tool; `max_actions`: maximum total action count.
- `budget`: only `max_tool_calls` (count), `max_elapsed_ms` (milliseconds), and `max_cost` (same monetary unit as `usage.cost`). If a configured cost/time metric is unavailable or unverifiable, return `insufficient_evidence`, never `pass`. Record currency/price basis in the surrounding experiment manifest.
- `expected_final`, `expected_state`: externally reviewed desired output and externally observed state. Explicit `null` is valid; omission is not.
- Optional `effect_policy`: `{"action":"report.export","baseline_effect_ids":["already-committed-id"],"max_new_effects":0}`. The action may be forbidden: this can catch a hidden external side effect even if the agent trace omits that call.

## Run: record every attempt

Required identity: `case_id`, `arm` (`baseline`, `current`, `candidate`, or explicitly `synthetic`), positive integer `attempt`, `status`, `versions`, `evidence_refs`, `actions`, `usage`. Values are sanitized and provenance is retained. Version fields `model`, `agent`, `skill`, `prompt`, `tool`, `dataset`, `evaluator` must be nonblank for an evaluable run; archived unknown values may be null but then **cannot pass** the gate.

`actions` is an ordered list of `{"name":..., "args":..., "effect_id":...}` records. `usage.tool_calls` equals the observed action count; optional `elapsed_ms` and `cost` are nonnegative numeric values (nullable only if no corresponding budget applies). A completed `pass` run must explicitly include `final` and `resulting_state`; failed/blocked runs may not have completed outputs.

Valid statuses: `pass`, `fail`, `blocked`, `timeout`, `infrastructure_error`, `grader_error`, `not_run`. For incomplete infrastructure, timeout, blocker or grader failures return `insufficient_evidence` without fabricating missing final outcomes; a recorded forbidden action or exceeded hard limit is still `fail`. An ordinary `fail` is not a success.

## Independent observation (separate input to the evaluator)

A completed successful run additionally requires **evaluator-owned** `observed` with `{"state":..., "evidence_ref":"...", "effects":[...]}`. `effects` is required for cases with `effect_policy` and contains unique `{"action":...,"effect_id":...}` records from an independently read side-effect ledger. The evaluator compares effect IDs before and after, not merely call counts. A repeated idempotent API call producing no new effect ID may be correct; a new effect after an already committed export is not.

The caller must obtain observations independently (e.g. read-only database state or isolated service ledger); **do not copy them from the agent's claimed `resulting_state`**. The standalone oracle cannot authenticate a fabricated evidence reference and does not verify an external system itself. Synthetic observations in the fixtures are only evaluator regression assets.

## Verification levels

The lightweight pilot consists of `discovery/agent_eval_pilot.py`, `discovery/test_agent_eval_pilot.py`, and the two `discovery/fixtures/agent-eval-*.json` files. Run:

```bash
python -m unittest discover -s discovery -p 'test_*.py' -v
```

It uses **synthetic** good and seeded-bad traces across positive, negative, interruption/recovery and adversarial cases. These verify oracle sensitivity and malformed-input behavior, not model or skill effectiveness. The fixture's `holdout` labels are synthetic examples, not a sealed real-world evaluation set.

For actual improvement claims, follow [skill-comparison.md](skill-comparison.md): baseline/current/candidate, pinned tasks and settings, verified skill loading, isolated repeated sessions, evaluator-owned hidden checks, all failures counted, security/completeness gates ahead of cost/latency. Report `specified`, `structurally validated`, `smoke-tested` or `behaviorally benchmarked` accurately.
