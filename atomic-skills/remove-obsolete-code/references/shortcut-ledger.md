# Temporary compromises and their revisit conditions

Use when introducing or reviewing a material bounded compromise, or when the user
requests a shortcut/debt inventory. Do not scan the whole repository on every coding
task. A debt inventory is read-only unless changes or persistence are requested.

## Record one decision, not a second documentation system

Use the project's existing convention, issue or ADR. Otherwise place a short comment
near the decision, in the language's comment syntax:

```text
shortcut: <known limitation>; revisit when <observable trigger>; then <upgrade path>
```

Example for an optional performance cache, not a correctness or security mechanism:

```python
# shortcut: cache is process-local; revisit before requiring cross-worker freshness;
# then use the shared cache and its invalidation contract.
```

Record only significant limits. Do not label every simple implementation as debt.
Use an existing issue/ADR for a longer rationale instead of repeating it in comments.
Attach an owner or review date when useful, but never infer responsibility from the
last committer alone. Do not invent a numeric capacity limit without supporting data.

A comment does not waive required authorization, tenant isolation, data integrity,
accessibility, compatibility or recovery. If the present requirement already crosses
the limit, the change needs a fix or explicit scope resolution now, not a future TODO.

## Collect and validate a ledger

1. Search scoped source comments and linked decision records for the project's marker
   (for example `shortcut:` or legacy `ponytail:`). Include known tracked files; exclude
   generated output, dependency caches and prose that merely explains the convention.
   Treat TODOs as compromises only after reading their meaning. Record the search scope.
2. Extract the location, decision, limitation, revisit condition and proposed upgrade.
   Read surrounding code and the relevant deployment/load assumptions; a marker is
   evidence of intent, not evidence that its assumptions still hold.
3. Mark missing or non-observable revisit conditions as `no-trigger`. Do not convert
   a phrase such as "later" into an invented deadline. Record unknown load as unknown.
4. Classify against current evidence:

| State | Meaning | Action |
| --- | --- | --- |
| Within limit | The documented assumption still holds. | Retain the simple choice; no automatic rewrite or review finding. |
| Trigger reached | Current requirements or observed operation cross the limit. | Propose the smallest sufficient upgrade and relevant verification. |
| Unknown / no-trigger | Evidence or a useful revisit condition is missing. | Name the missing fact; do not claim the compromise is safe or obsolete. |
| Resolved | The limit no longer exists and the recorded decision has been superseded. | In an authorized cleanup, remove stale markers and reconcile linked records. |

Prioritize reached triggers affecting correctness, security or data before cosmetic
cleanup. Age alone does not prove debt must be repaid. A permanent simple decision
that meets its requirements need not be upgraded.

## Output and handoff

| Location | Decision / limit | Trigger and present evidence | State | Smallest next step |
| --- | --- | --- | --- | --- |
| File:line or existing ADR | Concrete compromise | Observation or explicitly unknown | One of the states above | Retain, investigate, upgrade or reconcile |

Report counts by state, scope and anything not checked. No markers found means only
that this scan found none, not that the system has no technical debt. Do not write a
new ledger file unless requested or already required by the project's process.

A reached trigger may require [structural simplification](../../simplify-code-structure/SKILL.md)
or an [architecture decision](../../design-minimal-architecture/SKILL.md), not deletion.
For candidate removals still apply consumer, recovery and lifecycle checks from
[remove-obsolete-code](../SKILL.md). A marker never makes live code dead.

## Provenance

Original adaptation of [Ponytail debt tracking](https://github.com/DietrichGebert/ponytail/blob/09c434ab73ca43761c5d8b0c5d341926c2fba710/skills/ponytail-debt/SKILL.md)
and its [review treatment of bounded shortcuts](https://github.com/DietrichGebert/ponytail/blob/09c434ab73ca43761c5d8b0c5d341926c2fba710/skills/ponytail-review/SKILL.md),
reviewed 2026-10-26. This workflow adds explicit uncertainty and present-requirement
checks; it does not import upstream commands or assume a particular agent host.
