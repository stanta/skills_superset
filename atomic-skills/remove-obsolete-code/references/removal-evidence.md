# Removal Evidence

Use this reference when a candidate's reachability or retirement is uncertain.
Make the decision over an explicit supported consumer boundary, not over an unqualified claim that code is unused everywhere.

## Evidence by candidate type

| Candidate | Evidence to inspect | Common false positive | Safe completion |
| --- | --- | --- | --- |
| Private function or class | All callers in the relevant compilation/module graph; dynamic registration if applicable | Reflection or indirect dispatch bypasses text references | Remove the private element and run affected checks |
| Plugin or handler | Entry-point metadata, registries, name-based loaders, deployment config | No direct import exists because discovery is dynamic | Remove only after registration and supported use are retired |
| Public API or export | Contract versions, external consumer inventory, deprecation policy, old clients | No caller exists in this repository | Plan retirement separately unless the consumer boundary is already closed |
| Background job | Scheduler configuration, supported calendars, operational runbooks, recovery requirements | A yearly job has zero events in a monthly log window | Establish that the job's obligation ended |
| Temporary feature flag | Final targeting in every supported environment/cohort, completed experiment, rollout and rollback status | The default value differs from production targeting | Retain the final path, simplify branches and update dependent config/tests |
| Kill switch or entitlement | Operational purpose, policy/entitlement contract, incident procedures | A switch has never been toggled | Retain if it remains part of an active control or obligation |
| Package dependency | Runtime and development imports, scripts, plugins, generated code, package metadata | A compiler plugin is absent from application source | Update the manifest and reproducible lockfile using the project workflow |
| Serialized field or name | Readers/writers, queued messages, stored objects, version compatibility | No current source writer exists but older data still contains it | Preserve compatibility or perform an explicitly scoped migration |
| Migration file | Fresh install and supported upgrade paths, migration checksums/history | The migration ran long ago | Preserve historical migrations unless an established baselining policy permits replacement |
| Test or fixture | The retained behavior it proves, equivalent coverage, actual consumers | A test references the retired flag while asserting still-required behavior | Rewrite setup if needed; remove only assertions for retired contracts |

## Proportional evidence

- Accept complete static evidence for a genuinely private, non-dynamic symbol when the relevant build boundary is known.
- Use production telemetry as supporting evidence only with its time range, sampling and environment coverage recorded.
- Use ownership confirmation to resolve lifecycle intent; do not treat it as a substitute for inspecting code and compatibility.
- Investigate counter-evidence before editing: active configuration, exported names, required runbooks, old messages and recovery references.
- If sufficient evidence cannot be obtained, record a precise prerequisite and leave the candidate intact.
- Do not demand every possible evidence source when a smaller, complete argument establishes safety.

## Worked decisions

### Completed rollout with retained behavior

A release record establishes that `checkout_v2` is permanently enabled for all supported deployments. The rollback window is closed. Both branches calculate tax through a shared function, and a test of refund idempotency still matters.

Remove the flag and the old checkout branch. Keep the shared tax function. Rewrite the refund test's flag setup while retaining its idempotency assertion. Follow callers before deleting flag-related arguments.

### Apparent dead plugin

`plugins/archive_export.py` has no imports, but a deployment config contains `handler: plugins.archive_export:run`.

Retain the plugin. Treat the configuration as a real consumer; examine its lifecycle rather than using text import count as the deletion criterion.

### Constant operational control

`disable_payments` has been false for a year. An incident runbook uses it to stop new charges during a provider outage.

Retain the switch. Its value history does not invalidate its recovery purpose. Cleanup of obsolete comments or unused helpers can proceed independently.

### Dependency with indirect use

An application never imports a package that is declared in a build tool's plugin list.

Retain the package while the plugin is required. If the toolchain has already migrated, verify the new build and remove the stale declaration and dependency together.

## Review boundaries

Do not remove production records, audit evidence or required observability under a source-code cleanup instruction.
Do not use an expected line-count reduction as acceptance criteria.
Report whether a candidate is removed, retained for a known consumer, or deferred for missing information; avoid ambiguous claims that everything unused was removed.
