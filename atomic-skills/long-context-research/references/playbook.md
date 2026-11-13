# Large-corpus investigation

## Evidence ledger

Use records containing question/subquestion, claim, source ID/version, passage location, supporting or conflicting evidence, verification status and unresolved dependencies. For exhaustive requests, track document coverage and deterministic counts rather than relying on summaries. Quantities should be computed from validated records, not estimated by the model.

## Optional DSPy RLM

`dspy.RLM` exposes large inputs as variables to a code-driven inspection loop, with model subqueries available for focused semantic work. Check `max_iters`, `max_llm_calls`, `max_output_chars`, `sub_lm` and the interpreter interface against the installed release. Limit outer, nested and fallback extraction costs at the application level. A fallback answer after iteration exhaustion must not be reported as exhaustive coverage.

The documented default PythonInterpreter uses a sandbox; `LocalInterpreter` is not an equivalent security boundary. Verify actual filesystem/network/tool authority, resource limits and dependency support. Tools intentionally exposed to the interpreter may themselves perform privileged operations, so wrap them with server-side policy. Do not execute arbitrary local code merely to make an RLM example work.

## Failure probes

Check a relevant passage near the end of a corpus, two conflicting versions, a forged instruction inside a document, inaccessible evidence and exhaustion before all sources are inspected. Report uncertainty rather than replacing missing passages with invented citations.

## Primary source

Checked 2026-11-13. Original workflow with optional DSPy integration:

- https://dspy.ai/current/diving-deeper/rlm/

For broader recursive-context architecture, reuse the adjacent `rlm-roec-context-reasoning` skill instead of duplicating it.
