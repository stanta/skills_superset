# Regression decision record

## Required fields

Record baseline/candidate IDs and hashes; task/schema version; dataset/split/scorer hashes; model/runtime configuration; evaluated case IDs; run timestamps/status; thresholds/margins; critical-case failures; paired quality differences and uncertainty; cost/tail latency; artifact reload status; rollback ID; verdict/reasons; separate authorization status.

`pass`: all mandatory evidence exists and all frozen gates pass. `fail`: a hard constraint or declared comparison fails. `inconclusive`: evidence is incomplete, incompatible or too weak to support a decision. Both fail and inconclusive block automatic promotion. Never turn missing results into zeros that accidentally satisfy a threshold.

## Operational checks

An improved aggregate with one new critical failure must not pass. A cheaper candidate with unacceptable tail latency fails its latency gate. Comparing different case sets or grader revisions is not a paired regression test. Repeatedly selecting candidates using the held-out test contaminates it; create a fresh test set or independent audit.

## DSPy artifact handling

`Evaluate` supplies measurements; application code implements the release gate. Saved DSPy program state must travel with its compatible module source, dependency/model configuration and dataset/scorer provenance. Prefer inspectable state formats when supported. Loading a serialized program can execute code; only load trusted, integrity-checked artifacts in an approved environment. A successful reload alone establishes neither quality nor authorization.

## Primary sources

Checked 2026-11-13. The independent gate is repository-authored, not a DSPy built-in authorization system.

- https://dspy.ai/current/api/evaluation/Evaluate/
- https://dspy.ai/current/tutorials/saving/

Verify current save/load semantics against the installed release before implementation.
