# Shared AI-agent test case and run contract (v1)

One source of truth for `tester-ai`, `agent-evals-lab`, `verification` and skill comparisons. This is a **portable record contract**, not a new runner or a substitute for real agent execution. Use the host's existing test framework and keep business-oracle rules independent of the agent under test.

## Case (versioned and frozen before execution)

- `id`: stable case identifier; `kind`: `positive`, `negative`, `chaos` or `adversarial`.
- `requirement` and `initial_state`: externally reviewed expected behavior and starting state (or a versioned fixture reference).
- `allowed_actions`, `forbidden_actions` and `required_actions`: tool/action names; use action-specific argument assertions in an evaluator when permissions depend on arguments.
- `action_limits`: map of sensitive action names to maximum allowed call counts.
- `expected_final` and `expected_state`: observable outcome and side-effect state; do not require an identical trajectory unless a mandatory ordering/approval constraint demands it.
- `max_actions` and `budget`: predeclared call, latency or cost bounds appropriate to the case.
- `dataset_version` and `split`: immutable dataset revision and `development` / `holdout` membership; keep holdout hidden from the candidate agent.

## Run (one record for **every** attempt)

`case_id`, `arm` (`baseline` / `current` / `candidate` or explicitly `synthetic`), `attempt`, `status`, `final`, `resulting_state`, `actions`, `evidence_refs`, `versions` and `usage`. `actions` are ordered objects with `name` and optional sanitized `args` and `effect_id`. Retain failures, refusals, empty outputs and timeouts.

Valid statuses: `pass`, `fail`, `blocked`, `timeout`, `infrastructure_error`, `grader_error`, `not_run`. A reported `pass` is **not authoritative**: independent deterministic assertions must also pass. Missing cases, versions, required evidence or partial results cannot authorize a release. Distinguish evaluator failure from agent failure and keep both visible.

`versions` must identify the actual model, agent runtime, skill revision, prompt/program, tool contract, dataset and evaluator. Unknown values are `null` with an explanation, never fabricated identifiers. `usage` records tool calls, elapsed time and available token/cost figures (nullable). Redact private data, secrets and raw customer files from evidence.

## Pilot and reporting

The dependency-free pilot lives in `discovery/agent_eval_pilot.py` and `discovery/test_agent_eval_pilot.py`, using `discovery/fixtures/agent-eval-pilot.json`. Execute:

```bash
python -m unittest discover -s discovery -p 'test_*.py' -v
```

It deliberately includes known-good and seeded-bad **synthetic trace replays** for positive, negative, interruption/recovery and prompt-injection cases. This verifies that the evaluator rejects wrong tool choices, duplicate effects and bad outcomes; it does **not** show a real model or skill is better.

For behavioral comparisons use [skill-comparison.md](skill-comparison.md): frozen baseline/current/candidate, matching permissions/settings, isolated sessions, randomized/interleaved runs, hidden held-out checks, all attempts retained, critical correctness/security gates before efficiency comparisons. Claim a gain only after a real controlled agent runner executes these arms and the independent evaluator has passed its own seeded-positive/negative checks.
