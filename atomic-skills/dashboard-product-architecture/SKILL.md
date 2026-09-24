---
name: dashboard-product-architecture
description: This skill should be used when defining, redesigning, or reviewing the product architecture and information hierarchy of operational dashboards, KPI dashboards, administration consoles, or control-plane UIs. Apply it to establish audience, decisions, metric semantics, scope boundaries, overview-to-detail navigation, filters, actions, empty/error/loading states, and dashboard requirements before implementation; do not use it as the primary skill for chart encoding, realtime transport, or AI-agent telemetry schemas.
---

# Dashboard Product Architecture

## Purpose

Design dashboards as decision systems rather than collections of widgets. Establish what each audience must notice, decide, investigate, and change; then translate those needs into stable information architecture, metric contracts, surface hierarchy, and acceptance criteria.

Load `references/dashboard-product-playbook.md` for detailed patterns, checklists, source provenance, and the reusable specification template.

## Boundary

- Own audience, jobs-to-be-done, decision latency, KPI hierarchy, metric definitions, filter scope, drill-down paths, action placement, extension slots, and page-state requirements.
- Hand chart selection and perceptual accuracy to `dashboard-data-visualization`.
- Hand AI run, tool, cost, evaluation, approval, and recovery semantics to `ai-agent-control-plane-dashboard`.
- Hand WebSocket, SSE, polling, cache reconciliation, resume, and fan-out to `dashboard-realtime-consistency`.
- Hand accessibility, security, correctness, resilience, and performance verification to `dashboard-quality-gates`.

## Workflow

### 1. Identify the decision contract

- Name every audience and permission boundary.
- Record the question each surface must answer in one sentence.
- Define the decision or action enabled by each metric, list, alert, and chart.
- Reject widgets that have no decision, investigation, or accountability consequence.

Use this frame:

| Field | Required answer |
|---|---|
| Audience | Who reads or acts? |
| Situation | What event or cadence brings them here? |
| Question | What must become clear? |
| Decision | What choice follows? |
| Action | What can be changed safely? |
| Evidence | Which durable facts support the display? |
| Freshness | How stale may the answer be? |

### 2. Separate surface levels

Build an explicit hierarchy:

1. **Overview** — answer whether attention is needed; show only headline health, workload, risk, cost, and blockers.
2. **Domain list/detail** — locate the affected entity and compare peers.
3. **Investigation detail** — expose events, logs, traces, provenance, and error evidence.
4. **Audit/history** — prove who changed what and when.

Preserve filter, time range, tenant/profile, and selected entity context in links between levels. Never turn the overview into an unbounded terminal, trace viewer, or raw table.

### 3. Establish metric contracts before layout

For every KPI define:

- canonical name and plain-language meaning;
- numerator, denominator, units, and aggregation;
- time basis and timezone;
- inclusion/exclusion rules;
- freshness and source of truth;
- null, partial, delayed, and corrected-data behavior;
- thresholds, target, owner, and drill-down destination.

Distinguish stock from flow, readiness from activity, attempted from completed, failed from recovered, budget from spend, and warning from incident. Do not permit a label such as “active,” “success,” or “cost” without an explicit semantic contract.

### 4. Design attention hierarchy

- Place actionable exceptions before neutral totals.
- Keep headline KPIs limited to the smallest set required for a first-screen decision.
- Group widgets by operational question, not data source or implementation team.
- Use progressive disclosure for dense evidence.
- Pair anomalies with affected scope, likely cause, owner, and next action.
- Display current filter scope and data freshness visibly.

### 5. Define dashboard state model

Specify all of the following independently:

- initial loading;
- background refresh;
- no data yet;
- no matches after filters;
- partial data;
- permission denied;
- stale data or disconnected realtime;
- recoverable request failure;
- terminal failure;
- optimistic/pending action;
- action success, rejection, timeout, and unknown outcome.

Never replace a populated dashboard with a full-screen spinner during background refresh. Preserve prior valid data and label freshness.

### 6. Design filters and navigation as product contracts

- Give every filter a clear scope and default.
- Serialize shareable context into the URL when safe.
- Preserve time range and scoped variables through drill-down.
- Distinguish global filters from panel-local filters.
- Make reset, active-filter count, and “no matches” recovery obvious.
- Keep tenant, company, workspace, or profile write targets unambiguous.

### 7. Place operational actions safely

- Keep routine, reversible actions near the relevant state.
- Require confirmation and impact explanation for destructive, expensive, credential, permission, pause, cancel, restart, or update actions.
- Expose pending, accepted, running, completed, failed, and unknown action states.
- Link every action outcome to durable audit evidence.
- Separate observation permissions from mutation permissions.

### 8. Produce requirements and handoff

Deliver:

1. Audience and decision matrix.
2. Surface map and drill-down graph.
3. Metric dictionary.
4. Widget inventory with priority and rationale.
5. Filter and URL-state contract.
6. UI-state matrix.
7. Action and permission matrix.
8. EARS-style requirements and measurable acceptance criteria.
9. Risks, open assumptions, and evidence gaps.

## Non-negotiables

- Define semantics before visualization.
- Show scope, time range, timezone, and freshness.
- Preserve context during drill-down and sharing.
- Keep overview cheap and bounded; move forensic detail to dedicated surfaces.
- Couple alerts and exceptions to investigation and action paths.
- Avoid vanity metrics, decorative charts, duplicated KPIs, unexplained thresholds, and color-only status.
- Treat extension widgets as governed contracts with budgets and permission boundaries, not arbitrary page injection.

## Quality check

Before completion, verify:

- A new operator can state system health and the next required action within seconds.
- Every headline metric has a definition, owner, source, and drill-down.
- Every critical state has a path from detection to evidence to safe action.
- Empty, stale, partial, disconnected, and failed states are designed.
- The specification does not assume a particular chart library or realtime technology.
