---
name: dashboard-quality-gates
description: This skill should be used when planning, implementing, auditing, or release-gating quality for dashboards and AI-agent control planes. Apply it to metric correctness, accessibility, security and tenant isolation, realtime resilience, visual integrity, performance, browser compatibility, export safety, and end-to-end operator workflows; use it after dashboard semantics and architecture are defined rather than as a substitute for product design.
---

# Dashboard Quality Gates

## Purpose

Convert dashboard requirements into executable checks and release evidence. Verify not only that panels render, but that numbers are correct, scope is isolated, live updates reconcile, actions are safe, visualizations remain truthful, and operators can complete critical tasks with assistive technology and under failure.

Load `references/dashboard-test-playbook.md` for the risk matrix, scenario catalog, acceptance template, and source provenance.

## Boundary

- Own verification strategy, test portfolio, release thresholds, evidence, and defect classification.
- Consume metric and surface contracts from `dashboard-product-architecture`.
- Consume visual specifications from `dashboard-data-visualization`.
- Consume agent/run semantics from `ai-agent-control-plane-dashboard`.
- Consume live protocol guarantees from `dashboard-realtime-consistency`.

## Workflow

### 1. Build a risk inventory

Classify risk across:

- decision correctness and metric calculation;
- tenant/profile authorization and data leakage;
- privileged/destructive actions;
- agent run/retry/approval/audit behavior;
- stale, partial, delayed, duplicate, and reordered data;
- accessibility and keyboard/screen-reader workflows;
- visualization honesty and color dependence;
- performance at production cardinality and update rate;
- browser, viewport, theme, locale, timezone, and export behavior;
- plugin/extension isolation;
- secrets, PII, prompts, tool output, and CSV/formula injection.

Assign severity and release threshold before tests are written.

### 2. Validate metric contracts deterministically

For every headline metric:

- create fixed fixtures for numerator, denominator, inclusion/exclusion, timezone boundary, late data, retry/recovery, nulls, and duplicates;
- compare API/read-model output to an independent expected calculation;
- test empty input separately from zero;
- test calendar and rolling windows;
- test high cardinality and overflow/rounding;
- test recovered versus unresolved failures;
- verify displayed labels, units, freshness, and drill-down totals reconcile.

Do not approve a dashboard using screenshots alone.

### 3. Verify API, authorization, and audit

- Test every tenant/profile/resource endpoint and stream with authorized, unauthorized, stale, revoked, and cross-scope identities.
- Verify mutation permissions independently from read permissions.
- Test pagination, filtering, rate limits, validation, and problem responses.
- Verify cancel/retry/approve/pause actions are idempotent or version-guarded.
- Confirm every privileged action produces durable, attributable audit evidence.
- Test CSV/export injection neutralization and row/size limits.

### 4. Verify realtime consistency under hostile conditions

Automate:

- connection loss before/after persistence;
- duplicate, reordered, delayed, and missing events;
- server restart and ephemeral-state loss;
- reconnect/resume or authoritative refetch;
- terminal-state regression protection;
- hidden tab and multi-tab coordination;
- slow consumer and bounded buffers;
- multi-replica producer/client mismatch;
- deploy drain and reconnect storm;
- fallback polling and stale-state labeling.

Assert final durable correctness, not merely that a message arrived.

### 5. Test operator journeys end to end

Cover at least:

- identify an exception from overview and drill to root evidence;
- preserve tenant/profile/time/filter context through navigation and refresh;
- inspect a run, model/tool steps, cost, retry lineage, and evaluation;
- approve/deny, cancel, retry, pause/resume with confirmation and audit;
- recover from no data, partial data, API failure, disconnected live updates, and unknown action outcome;
- search/filter/sort/export evidence;
- switch profile/tenant without cache leakage;
- use plugin widgets without breaking host surfaces.

Prefer role/label/user-visible assertions over implementation details.

### 6. Audit accessibility

Combine automation and manual verification:

- landmarks, headings, skip links, page title, language, and semantic tables;
- full keyboard operation and visible focus;
- modal focus trap/restore and escape behavior;
- status announcements without live-region spam;
- text alternatives and data-table fallback for charts;
- contrast across themes and forced/high-contrast modes;
- color-independent state and chart meaning;
- zoom/reflow at 200–400%, narrow viewport, long text, and localization;
- reduced motion;
- screen-reader walkthrough of critical operator journeys.

Target WCAG 2.2 AA unless a stricter requirement is specified.

### 7. Audit visual and interaction integrity

- Verify axes, baselines, scales, units, legends, tooltips, thresholds, and uncertainty against the visual spec.
- Snapshot only stable visual contracts; avoid brittle full-page snapshots as the sole evidence.
- Test loading, empty, no-match, partial, stale, error, disabled, pending, success, failure, and unknown states.
- Verify responsive layouts, overflow, clipping, sticky elements, and chart resizing.
- Test light/dark/system themes and long/translated content.

### 8. Measure performance and resource use

Define budgets for:

- API p50/p95/p99 and query count;
- summary payload and incremental event/log bytes;
- event-to-paint latency;
- initial route load and interaction latency;
- long-task and frame budgets;
- memory growth during long live sessions;
- sockets/polls per tab and across tabs;
- hot-tenant concurrent runs and transcript rendering;
- export generation and database load.

Use realistic data and sustained tests, not only a warm single-user trace.

### 9. Test security-specific rendering and extensions

- Render hostile model/tool/log/plugin strings and verify inert output.
- Test XSS, URL injection, unsafe links, formula injection, oversized payloads, and secret/PII redaction.
- Verify CSP, iframe/plugin sandbox boundaries, and plugin failure isolation where applicable.
- Confirm authentication for WebSocket/SSE upgrades and revalidation after revocation.
- Verify no protected cache remains after logout or scope switch.

### 10. Produce release evidence

Deliver:

1. Risk-based test plan.
2. Requirement-to-test traceability matrix.
3. Fixtures and independent metric oracle.
4. Automated unit/integration/E2E/resilience/performance suites.
5. Manual accessibility and exploratory charters.
6. Defects with severity, evidence, and remediation.
7. Release scorecard with explicit pass/fail thresholds.
8. Production canaries, dashboards, alerts, and rollback criteria.

## Release blockers

Block release for:

- cross-tenant/profile data or event leakage;
- incorrect headline metrics or misleading visual encoding;
- unaudited privileged actions;
- unsafe raw agent/tool output rendering;
- inaccessible critical action or investigation path;
- terminal state corrupted by stale live events;
- unbounded memory/queue growth under expected load;
- inability to recover correctness after reconnect/restart;
- hidden zero-tolerance policy/evaluation failure.

## Non-negotiables

- Name the bug each test catches.
- Keep deterministic assertions for formulas, state transitions, authorization, and schemas.
- Test failure and degraded paths at least as rigorously as happy paths.
- Never weaken expected results to make a failing test pass.
- Promote confirmed production incidents into regression fixtures.
