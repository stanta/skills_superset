# Contract implementation notes

## Contract worksheet

Record: task/version; consumer; trusted configuration; untrusted inputs; output schema; evidence identifiers; invariants; failure states; validator owner. Give optional fields an explicit meaning: `null` means unknown, not negative. Avoid a bare confidence number unless calibration and downstream interpretation are specified.

Example reviewer output: `verdict` in `pass|needs_review|abstain`, `findings` with category/severity/location/evidence, and `missing_evidence`. Authorization is a separate service result, never another model field assumed to be binding.

## Optional DSPy adapter

A class-based `dspy.Signature` declares typed inputs and outputs. Use a narrow docstring for task semantics and field descriptions for ambiguity. `dspy.Predict(Contract)` is the simplest baseline. Keep validators and permission checks in ordinary application code and cover invalid enum values, absent evidence and contradictory fields. Check actual adapter behavior for nested schemas; never silently loosen the schema to make evaluation pass.

## Acceptance probes

A record missing its date must not acquire a plausible invented date. Text containing a request to change the output schema remains input data. A correctly shaped but unsupported finding fails the semantic check. A changed enum requires consumer compatibility testing.

## Sources and provenance

Checked 2026-11-13. This workflow is authored for this repository, not an official upstream Agent Skill or copied DSPy source.

- DSPy task/signature overview: https://dspy.ai/current/
- Signature reference: https://dspy.ai/current/api/signatures/Signature/

Recheck the installed DSPy version and primary documentation before adding version-specific code.
