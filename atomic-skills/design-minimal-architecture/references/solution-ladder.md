# Executable solution ladder

Use after understanding the task, not instead of reading code. Apply it to the
current decision; a small fix does not require a repository-wide architecture audit.

## Establish the full impact surface

Read the relevant entry point, implementation and tests. Identify affected callers,
exports, configuration, fixtures and stored/public representations. Inspect dynamic
registrations and external consumers when applicable. State actual load and important
unknowns. Required security, accessibility, compatibility, data integrity and recovery
are part of sufficiency even when the ticket does not repeat them.

## Choose the first sufficient option

| Order | Agent action | Evidence for accepting the option |
| --- | --- | --- |
| 1. Avoid unnecessary work | Separate the requested outcome from speculative features, knobs and extension points. | The outcome is already satisfied, or the omitted capability is outside scope. Never silently omit a requested requirement. |
| 2. Reuse the project | Search the affected area for an existing helper, component, service or supported pattern; read its contract and a real caller. | The mechanism implements the needed semantics and fits the project's boundaries. Name its path. |
| 3. Use built-ins | Check the standard library or native platform capability. | Supported versions, error behavior, accessibility and other required semantics fit. Prefer an appropriate house component when it already wraps that capability. |
| 4. Reuse an installed dependency | Check manifests and actual usage before invoking an existing package. | Its supported API solves the task without unsuitable coupling, licensing or operational assumptions. |
| 5. Keep simple logic direct | Use a clear expression or small local function rather than speculative generalization. | A reader can understand it without decoding a clever one-liner; edge cases remain handled. |
| 6. Add the minimum sufficient implementation | Add only the missing responsibility, with necessary tests and affected consumers. | Earlier options fail a named requirement; the new code or dependency earns its maintenance cost. |

The order is a search heuristic, not a prohibition on specialist libraries. Do not
replace maintained cryptography, authentication or a complex parser with homemade
code to avoid a dependency. An existing abstraction with one implementation may
still enforce a useful policy. Do not preserve an unsafe legacy pattern merely to
follow local convention; report it and keep remediation within authorized scope.

For a meaningful choice, record the selected step, evidence and exception in a few
sentences. Do not produce six empty checklist entries for a trivial change. Stop
searching once sufficiency is established; do not keep exploring to optimize line count.

## Finish the whole change

Include required callers, fixtures, tests, documentation and compatibility work.
A smaller diff that leaves a consumer broken is not a complete solution. Preserve
validation and error handling when moving or merging code. New nontrivial logic
needs verification of its actual risks: prefer an existing behavioral test when it
already covers the change; add targeted cases where it does not. One test is not a
quota or a sufficient ceiling for payments, concurrency or authorization.

For a bounded temporary compromise, use the
[shortcut ledger](../../remove-obsolete-code/references/shortcut-ledger.md).
Report what was deliberately omitted, what checks actually ran, what remains
unverified and any material risk. Do not invent savings against code never written.

## Examples and counterexamples

- Date input: reuse the project's accessible input with the browser's date support
  when it meets the requested UX and target platforms; do not build a calendar by default.
- Money: retain the project's decimal/currency rules; fewer lines using floating-point
  arithmetic are not an equivalent alternative.
- Shared rate limiting: a process-local dictionary is not sufficient when the current
  deployment has multiple workers and requires a shared quota.
- Rename: update the untouched serializer and dynamic registration as well as the
  function declaration. Impact scope is not scope creep.

## Provenance and limits

Original adaptation of the decision sequence and complete-change emphasis in
[Ponytail's core skill](https://github.com/DietrichGebert/ponytail/blob/09c434ab73ca43761c5d8b0c5d341926c2fba710/skills/ponytail/SKILL.md),
reviewed 2026-10-26. This is a contextual engineering heuristic, not a measured
performance claim. No Ponytail hooks, persistent modes or host adapters are installed.
