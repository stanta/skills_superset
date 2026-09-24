# Dashboard Product Playbook

## Core principle

A dashboard is an intentionally constrained answer to an operational question. Measure success by decision quality and time-to-action, not panel count.

## Surface specification template

```markdown
# Surface: <name>

## Audience and permissions
- Primary audience:
- Secondary audience:
- Read scope:
- Mutation scope:

## Primary question
<one sentence>

## Decisions and actions
| Signal | Decision | Action | Permission | Audit evidence |
|---|---|---|---|---|

## Headline metrics
| Metric | Definition | Time basis | Freshness | Source | Threshold | Drill-down |
|---|---|---|---|---|---|---|

## Filters and URL state
| Filter | Scope | Default | URL key | Preserved on drill-down? |
|---|---|---|---|---|

## States
Loading, refreshing, empty, no matches, partial, stale, disconnected,
permission denied, request failed, mutation pending/failed/unknown.

## Performance budget
- Initial summary payload:
- Maximum widgets above fold:
- Refresh cadence:
- Maximum rows/marks before aggregation:
```

## Dashboard hierarchy patterns

### Strategic

Use for outcome, risk, trend, and resource allocation. Prefer a low update cadence and strong metric governance. Suppress raw operational noise.

### Tactical

Use for team/process throughput, queues, quality, bottlenecks, and budget. Provide filters, comparisons, and drill-down to entities.

### Operational

Use for immediate health, incidents, work in progress, approvals, and recoveries. Prefer exception-first layout and explicit actions.

Do not mix these levels without a visual hierarchy and a clear audience reason.

## Metric dictionary template

| Field | Meaning |
|---|---|
| `metric_id` | Stable machine-readable identifier |
| Display name | User-facing label |
| Question | Decision question it answers |
| Formula | Exact calculation |
| Grain | Per event, run, user, tenant, day, etc. |
| Aggregation | Sum, count, rate, percentile, distinct count |
| Window | Calendar, rolling, session, lifecycle |
| Timezone | UTC or explicit local zone |
| Source | Authoritative durable record/read model |
| Freshness SLO | Maximum expected delay |
| Corrections | Late/retried/recovered data handling |
| Owner | Team responsible for correctness |
| Target | Desired value or range |
| Threshold | Warning/critical policy |
| Drill-down | Evidence surface |

## Information hierarchy checklist

- Put “requires action” and “blocked” before healthy totals.
- Show a concise state label beside every ambiguous number.
- Use direct labels and explanatory subtitles where metric names can be misread.
- Provide comparisons only when the baseline is meaningful.
- Prefer one overview card linked to detail over duplicate versions of the same KPI.
- Show last updated time and disconnected/stale state without hiding prior facts.
- Keep tables for lookup, ranking, and evidence; keep charts for patterns and change.

## Anti-patterns

### Widget warehouse

Symptom: each stakeholder adds a panel and nothing is removed. Remedy: require a decision contract and owner for every widget.

### KPI without denominator

Symptom: “success rate” changes because the definition of attempts changed. Remedy: display and document numerator, denominator, exclusions, and recovery semantics.

### Overview as forensic viewer

Symptom: raw logs and transcripts dominate the first screen. Remedy: show bounded previews and route to investigation detail.

### Hidden scope

Symptom: users act on the wrong tenant/profile/time range. Remedy: make scope persistent, URL-addressable, and visually explicit around mutations.

### Empty-state ambiguity

Symptom: “0” may mean healthy, no telemetry, no permission, or broken query. Remedy: separate numeric zero from no-data, partial-data, and error states.

## EARS requirement examples

1. **Ubiquitous.** The dashboard shall display the active tenant/profile and time range on every scoped surface.
2. **State-driven.** While summary data is refreshing, the dashboard shall retain the last valid values and indicate refresh state.
3. **Unwanted behavior.** If a metric source exceeds its freshness SLO, the dashboard shall mark the metric stale and shall not present it as current.
4. **Event-driven.** When a critical exception appears, the dashboard shall provide a context-preserving path to the affected entity and evidence.
5. **Optional feature.** Where dashboard extensions are enabled, the host shall enforce permission, payload, render, and failure-isolation contracts.

## Sources and provenance

Use these established GitHub repositories and project sources as evidence. Each exceeds the required threshold of 5 stars and/or forks:

- `grafana/grafana` — variables, time context, dynamic dashboards, drill-down links, alerts, and metrics/logs/traces correlation: https://github.com/grafana/grafana
- `apache/superset` — dashboard-scoped native filters, cross-filtering, drill-down, chart caching, and shareable embedded state: https://github.com/apache/superset
- `paperclipai/paperclip` — company-scoped agent control-plane hierarchy and durable-state/realtime split: https://github.com/paperclipai/paperclip
- `incluud/accessible-astro-dashboard` — landmarks, skip links, focus visibility, and accessible dashboard shell: https://github.com/incluud/accessible-astro-dashboard

Project-specific interpretation is grounded in `paperclip-dashboard-analysis.md` and the Hermes dashboard documentation. Revalidate repository behavior and version-specific implementation before coding.
