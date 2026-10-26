# Reproducible comparisons of coding-agent skills

Use for evaluating a prompt/skill change, not as a mandatory step for every product
PR. Reuse the project's existing evaluation runner. This protocol and the companion
case specifications are not an executed benchmark, a new runner or permission to
run paid models. Respect the skill manifest and host permissions: where execution
or writes are unavailable, deliver a plan and clearly identify checks not run.

## 1. Freeze the question and acceptance gates

State a testable hypothesis, such as: the candidate reuses existing capabilities
more often without losing required behavior. Separate source size, human maintenance
cost and model-call cost; none is a substitute for the others. Define critical gates
and non-inferiority tolerances before seeing results. Critical safety/contract
regressions block adoption; efficiency cannot compensate for them. Absolute safety
requirements still apply even if all arms share a failure.

Use representative tasks plus negative controls where the current solution is already
minimal or a dependency/interface is necessary. Include multi-file edits, concurrency,
privacy, rollback obligations and realistic invalid inputs. Keep held-out tasks that
are not used to tune the candidate. Test only the change under study; use separate
ablations when attributing improvement to one rule.

## 2. Compare the actual agent under controlled conditions

Use these arms when meaningful:

- **Baseline:** the normal agent with the target simplicity skill disabled, retaining
  the same task, required project instructions and unrelated safety controls.
- **Current:** the current released skill or skill bundle.
- **Candidate:** the proposed revision, changing only the skill treatment.

Pin the task/fixture commit, skill commits, model identifier/version, agent version,
effort/settings, tool permissions, environment, timeout and budget. Record any provider
version that cannot be pinned. Give every arm the same tools and tests. For an agentic
claim, allow the same normal edit/test/debug loop in all arms. A generation-only trial
with shell disabled must be labeled as such and cannot establish end-to-end savings.

Use fresh disposable workspaces and isolated session state for every run. Keep user
credentials, production services and unneeded network access out. Do not modify global
agent settings or disable permission enforcement. Inspect actual prompt/skill-loading
traces or equivalent host evidence: an indexed skill is not proof of injection, and
file-read events alone may miss injected instructions. Report uncertainty if loading
cannot be verified. Prevent baseline contamination from parent rules, plugins, memory,
recent-commit context and previous outputs without removing required project controls.

Interleave/randomize arms within each task and repetition to reduce order/time effects.
A small repeated pilot (for example five runs per task/arm within an approved budget)
checks feasibility; it is not automatically powered evidence. Record seeds where
supported and residual nondeterminism. Retain every attempted run, including timeout,
refusal, crash, empty output and tool failure.

## 3. Evaluate delivered artifacts, not promises

Keep evaluator-owned hidden checks outside the agent's editable workspace. Run them
against the final files in an isolated test environment. Seed known-good and known-bad
implementations first; the evaluator must accept the good and reject the bad. A broken
scorer invalidates the affected result, not the candidate's safety requirement.

| Dimension | Preferred evidence |
| --- | --- |
| Correctness and contracts | Executed hidden checks for required outcomes, all consumers and edge cases |
| Security and data integrity | Adversarial cases for relevant boundaries, ordering, isolation and recovery |
| Completeness | Acceptance criteria implemented; no stub, omitted caller, removed guard or dropped feature |
| Test quality | Relevant behavioral assertions; targeted injected defects detected; skipped/weakened checks flagged |
| Complexity | Unnecessary concepts/dependencies plus source diff/size as diagnostic measures |
| Execution cost | Measured input/output/cache tokens, tool calls, elapsed time and attributable billed or explicitly estimated cost |

Report production code and tests separately; do not reward missing tests as reduced
bloat. If using mutation checks, report the operator set, valid mutants, equivalent
or invalid mutants excluded and both the total detection rate and rate conditional
on a runnable test. One microtest is not a universal quality gate.

Use a blinded, fixed-rubric LLM judge only for properties not adequately checked by
execution. Validate it on positive/negative examples, hide arm identity and give enough
surrounding code to judge imports and contracts. Publish rubric/model, disagreements
and manual overrides. A judge's completeness score is not a runtime or security proof.

## 4. Analyze without hiding failures

Report all-run correctness/completeness rates and failures first. Keep timeout and
missing-output counts in the denominators of delivery outcomes. Show efficiency for
successful comparable outputs separately, with its selection rule and sample count;
never reward a crash or an empty patch for low cost or few lines.

For repeated tasks, report per-task summaries before aggregation. Paired task-level
ratios and geometric means are useful for positive cost/time/size measures. Report
zero baselines, missing values and exclusions explicitly; do not add arbitrary epsilon
values to manufacture a ratio. Bootstrap at the task level (or use an appropriate
hierarchical method) rather than pretending repeated runs are independent tasks.
Show uncertainty intervals, wins/ties/losses and task-family regressions. Small pilots
may justify only a descriptive conclusion. Say "inconclusive" when the data cannot
support a superiority or non-inferiority claim.

Separate common baseline failures from candidate regressions and enforce absolute
critical gates. Do not tune thresholds or discard difficult tasks after seeing which
arm wins. Keep a held-out confirmation run after iteration. Compare lifetime maintenance
cost only when measured; do not infer it from output tokens or line counts.

## 5. Keep an auditable run record

Store one record per attempted task/arm/repetition with:

```text
run_id, task_id, arm, repetition, fixture_commit, skill_commit,
model, agent_version, settings, tool_policy, loaded_skill_evidence,
status, correctness, security, completeness, test_results,
source_size, test_size, dependency_delta, tool_calls,
input_tokens, output_tokens, cache_tokens, elapsed_seconds,
cost_value, cost_basis, artifact_refs, evaluator_version
```

Use null plus an explanation for unavailable metrics, not zero. Distinguish provider
usage from list-price estimates and actual billing. Retain redacted diffs, transcripts,
scorer output and failed attempts so scoring can be repeated offline. Never publish
secrets, private code or personal data as benchmark artifacts without authorization.

The report contains: hypothesis; pinned setup; attempts and exclusions; critical-gate
results; per-task metrics and uncertainty; counterexamples; decision; and untested
conditions. State whether the work is **specified**, **structurally validated**,
**smoke-tested**, or **behaviorally benchmarked**. Do not claim improvement from
structural CI or transfer another project's percentages to this repository.

## Starting cases and attribution

[Case specifications](simplicity-cases.json) supply prompts, fixture requirements and
expected checks. They are not executable fixtures or results. Materialize them using
the existing runner and validate its oracles before a model run; keep expected checks
hidden from the agent under test.

Inspired by the author-published [Ponytail agentic methodology](https://github.com/DietrichGebert/ponytail/blob/09c434ab73ca43761c5d8b0c5d341926c2fba710/benchmarks/agentic/README.md)
and [2026-10-07 results and limitations](https://github.com/DietrichGebert/ponytail/blob/09c434ab73ca43761c5d8b0c5d341926c2fba710/benchmarks/results/2026-10-07-agentic.md),
reviewed 2026-10-26. Those results are workload-specific, not independently reproduced
here. This adaptation requires held-out cases, explicit loading evidence, failure
accounting and the same permitted tool policy across arms.
