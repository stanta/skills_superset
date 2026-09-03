---
name: ai-agent-control-plane-dashboard
description: This skill should be used when designing, reviewing, or extending dashboards and operator consoles for AI agents, LLM applications, autonomous workflows, and multi-agent systems. Apply it to define run/trace/tool state, health and recovery semantics, cost and token controls, evaluation signals, approvals, audit lineage, human intervention, privacy-safe evidence, and overview-to-run investigation surfaces; do not use it for generic KPI dashboards without agent execution semantics.
---

# AI Agent Control-Plane Dashboard

## Purpose

Design an operator control plane that makes agent execution observable, governable, recoverable, and auditable. Model agent behavior as durable runs and structured evidence, not as transient chat messages or a process-local “online” badge.

Load `references/agent-control-plane-playbook.md` for the canonical entity model, metrics, surface map, Paperclip-derived lessons, and source provenance.

## Boundary

- Own agent/run/step/tool/evaluation/approval/cost/audit semantics and operator workflows.
- Use `dashboard-product-architecture` for cross-domain audience, hierarchy, filters, and layout specification.
- Use `dashboard-data-visualization` for chart choice and perceptual quality.
- Use `dashboard-realtime-consistency` for transport, cache, replay, fallback, and scale.
- Use `dashboard-quality-gates` for verification and release gates.
- Use broader LLM observability skills when instrumenting a vendor platform; keep this skill focused on the operator product model and control plane.

## Core model

Model at least:

```text
Tenant/Profile
├── Agent definition and runtime state
├── Task/Issue/Conversation
│   └── Run/Turn/Heartbeat
│       ├── Step/Span
│       ├── Model generation
│       ├── Retrieval
│       ├── Tool call
│       ├── Structured event/log chunk
│       ├── Usage/cost event
│       ├── Evaluation/score
│       └── Approval/intervention
└── Activity/Audit record
```

Give every entity stable identity, timestamps, scope, status, lineage, version metadata, correlation IDs, and retention/privacy classification.

## Workflow

### 1. Define operator personas and control boundaries

Cover at least:

- operator/on-call: health, incidents, cancel/retry/recover;
- product/quality: outcomes, evals, user impact, regressions;
- finance/owner: spend, budget, model/provider allocation;
- security/auditor: actor, tool, permission, input/output handling, policy evidence;
- developer: trace, prompt/model/tool version, error cause, latency decomposition.

Separate read, investigate, export, approve, cancel, retry, pause, resume, edit configuration, and manage credentials permissions.

### 2. Define unambiguous state machines

Separate agent readiness from current execution:

- readiness: enabled, paused, disabled, degraded, error;
- run lifecycle: queued, starting, running, waiting_for_tool, waiting_for_approval, retry_scheduled, succeeded, failed, cancelled, timed_out, orphaned;
- liveness: healthy, slow, stalled, disconnected, unknown;
- outcome: succeeded first pass, recovered after retry, unresolved failure, policy-blocked, human-resolved.

Document legal transitions, terminal states, timeout rules, retry lineage, and how stale or lost worker state is reconciled. Never collapse readiness, activity, liveness, and last outcome into one status.

### 3. Establish durable evidence

Persist and expose:

- run trigger and task/session context;
- start, progress, finish, cancellation, and recovery timestamps;
- prompt/config/model/tool/version identifiers;
- sequenced structured events and spans;
- bounded/redacted request and response evidence;
- tool inputs/outputs or privacy-safe summaries;
- token, latency, usage, and cost records;
- error code, cause, exit/signal, and retry lineage;
- approval request, decision, actor, reason, and expiry;
- audit events for every control-plane mutation.

Treat ephemeral current tool/snippet/presence as acceleration only. Do not use it as the sole audit or recovery source.

### 4. Design surfaces by operator question

1. **Fleet/company/profile overview:** Is the scoped system healthy and within budget? Show active/running/error/paused, workload, blocked tasks, pending approvals, spend/budget, outcome trend, and recent incidents.
2. **Agent list/detail:** Which agent is affected? Show readiness, liveness, current/recent runs, model/config version, budget, tools, error streak, and interventions.
3. **Task/session detail:** What is the agent trying to accomplish? Show user/task context, handoffs, approvals, outputs, and linked runs.
4. **Run/trace detail:** What exactly happened? Show critical path, steps/spans, model/tool calls, retries, transcript/log, latency/cost breakdown, evals, and diagnostics.
5. **Quality/evaluation:** Is behavior improving? Show task completion, trajectory/tool correctness, groundedness/safety/policy scores, dataset/prompt/model versions, and release comparison.
6. **Audit/governance:** Who changed or approved what? Provide immutable attribution, scoped export, and retention controls.

Keep overview previews bounded. Route forensic reading to run/trace detail.

### 5. Define agent-specific metrics

Include only metrics with explicit action paths:

- workload: queued/running/waiting/stalled;
- outcomes: first-pass success, recovered, unresolved failure, cancellation, timeout;
- latency: queue, time-to-first-event, model, tool, approval wait, end-to-end percentiles;
- cost: per run/task/user/agent/model/provider, budget utilization, forecast, cost per successful task;
- autonomy: tool calls, handoffs, retries, human intervention rate, approval wait;
- quality: completion, groundedness, policy/safety, schema validity, user feedback, regression delta;
- reliability: stale run rate, reconnect/resume success, duplicate/lost event indicators;
- provenance: prompt/model/config/dataset/release version coverage.

Avoid “number of tokens” or “number of runs” as headline success metrics without outcome and cost context.

### 6. Design investigation and intervention

For every incident, support:

```text
Signal → affected scope → run/task → critical step/tool/model → evidence
       → root-cause hypothesis → safe action → audit confirmation
```

Define cancel, retry from checkpoint, resume, reassign, pause agent, revoke tool, approve/deny, and mark resolved behavior. Require idempotency keys, explicit impact, bounded retry, permission checks, and unknown-outcome reconciliation.

### 7. Integrate evaluations with operations

- Attach deterministic and model-based scores to run/session/release versions.
- Link score regressions to representative traces and datasets.
- Distinguish online telemetry from curated offline evaluation.
- Promote confirmed production failures into regression datasets.
- Keep evaluator/model versions visible.
- Prevent an aggregate score from hiding a zero-tolerance policy or security failure.

### 8. Preserve privacy and security

- Store redacted/hash/surrogate identifiers where full content is unnecessary.
- Classify prompts, retrieved documents, tool payloads, files, secrets, and PII separately.
- Make raw-content access permissioned and audited.
- Sanitize rendered model/tool output and downloaded exports.
- Apply tenant/profile scope to REST, streams, WebSocket/SSE, exports, and cache keys.
- Never render untrusted agent output as executable markup.

### 9. Deliver the control-plane specification

Produce:

1. Entity and state model.
2. Event/span and audit schemas.
3. Surface map and operator journeys.
4. Metric dictionary and evaluation taxonomy.
5. Permission/action matrix.
6. Durability, retention, privacy, and export policy.
7. Realtime/fallback requirements.
8. Failure/recovery requirements and runbooks.
9. EARS requirements and acceptance tests.

## Non-negotiables

- Durable state is truth; realtime is acceleration.
- Every run is traceable across task, agent, model, prompt/config version, tool, cost, and outcome.
- Recovered failures remain visible without inflating unresolved-failure headlines.
- Every mutation is permissioned, idempotent where retryable, and audited.
- Partial, stale, disconnected, and unknown states are explicit.
- Operator actions never depend on ephemeral UI-only data.
