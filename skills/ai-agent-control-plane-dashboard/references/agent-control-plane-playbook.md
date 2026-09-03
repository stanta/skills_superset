# AI Agent Control-Plane Playbook

## Canonical run record

```yaml
run:
  id: string
  tenant_id: string
  agent_id: string
  task_id: string|null
  session_id: string|null
  trace_id: string
  trigger:
    type: schedule|event|user|api|retry|recovery
    actor_id: string|null
    detail: object
  status: queued|starting|running|waiting_for_tool|waiting_for_approval|retry_scheduled|succeeded|failed|cancelled|timed_out|orphaned
  liveness: healthy|slow|stalled|disconnected|unknown
  outcome: first_pass_success|recovered|unresolved_failure|policy_blocked|human_resolved|null
  started_at: datetime|null
  last_progress_at: datetime|null
  finished_at: datetime|null
  prompt_version: string|null
  config_version: string|null
  model: string|null
  provider: string|null
  release_version: string|null
  parent_run_id: string|null
  retry_of_run_id: string|null
  checkpoint_id: string|null
  usage: object
  cost: object
  error: object|null
  privacy_classification: string
```

Do not force every implementation into this exact schema. Preserve the semantic distinctions and stable identifiers.

## Event envelope

```yaml
event:
  id: string
  tenant_id: string
  run_id: string
  trace_id: string
  span_id: string|null
  sequence: integer
  type: run.status|run.progress|model.start|model.end|tool.start|tool.end|approval.requested|approval.decided|evaluation.recorded|log.chunk|cost.recorded
  occurred_at: datetime
  durable: boolean
  schema_version: string
  payload: object
```

Require deduplication identity, ordering scope, schema version, and explicit durability. Keep UI-only snippets out of the durable audit contract unless required for recovery.

## Overview metric definitions

### Agent counts

- **Enabled/ready:** eligible to receive work, even when idle.
- **Running:** has at least one nonterminal run currently executing.
- **Paused:** intentionally prevented from receiving work.
- **Error:** latest relevant run or runtime health requires investigation.

Avoid counting one agent in contradictory headline states without explaining overlap.

### Outcome trend

Separate:

- first-pass succeeded;
- failed but succeeded in a linked retry/recovery chain;
- unresolved failed;
- cancelled/timed out/policy-blocked/other.

Do not erase recovered failures; expose them in drill-down while excluding them from unresolved-failure headlines.

### Cost

Show:

- current period spend and timezone/calendar definition;
- budget and utilization;
- forecast with method and uncertainty;
- highest-cost agents/tasks/models;
- cost per successful task or quality-adjusted outcome;
- budget-triggered pauses and pending approvals.

### Quality

Separate operational success from semantic quality. A completed run may have failed task completion, groundedness, safety, schema, or user satisfaction checks.

## Run detail layout

Recommended order:

1. Identity, status, task, agent, trigger, versions, timestamps.
2. Current or terminal outcome and available actions.
3. Critical-path timeline with queue/model/tool/approval spans.
4. Input/output summary with privacy controls.
5. Tool calls and side effects.
6. Retry/recovery/checkpoint lineage.
7. Token, latency, and cost breakdown.
8. Evaluations, policy decisions, and user feedback.
9. Structured events and bounded persisted log.
10. Audit trail and links to related task/session/agent.

## Intervention contract

| Action | Preconditions | Idempotency | Evidence |
|---|---|---|---|
| Cancel | Nonterminal, authorized | Request key; repeated cancel is safe | Actor, reason, accepted time, terminal result |
| Retry | Terminal/retryable, budget/policy allowed | New run linked to original | Retry reason, changed inputs/config, lineage |
| Resume | Valid checkpoint/session | Resume key and checkpoint version | Restored state and continuation run |
| Pause agent | Authorized scope | Desired-state assignment | Reason, actor, affected queued/running work |
| Approve/deny | Pending, not expired | Decision ID unique | Reviewer, policy, reason, payload hash |
| Reassign | Task/run supports transfer | Version check | Old/new owner and context transfer |

Never report an action complete merely because the command endpoint returned success; reconcile against durable resulting state.

## Paperclip-derived architectural lessons

The local `paperclip-dashboard-analysis.md` establishes these high-confidence patterns:

- Use company/tenant-scoped control-plane surfaces and permission checks.
- Persist runs, run events, runtime state, activity/audit, and cost as durable truth.
- Build REST read models; use WebSocket to patch/invalidate client cache; retain polling and persisted-log fallback.
- Distinguish readiness (`active`) from current work (`running`).
- Show 14-day outcome activity with recovered retry chains separate from unresolved failures.
- Use one shared socket rather than one per component.
- Keep ephemeral current status/tool/snippet bounded and nonauthoritative.
- Use cheap bounded previews on overview and full transcripts on task/run detail.
- Coordinate polling across tabs and slow hidden-tab refresh.
- Treat an in-process event bus as a multi-replica risk; add a backplane or topology constraint.

## Hermes adaptation notes

Hermes currently provides a machine/profile-scoped dashboard with React 19, TypeScript, FastAPI, status/session/analytics/log/system surfaces, plugins, profile-aware management, WebSocket-backed chat/PTY, and polling. When extending it into a broader agent control plane:

- preserve profile scope in URL and API contracts;
- retain SQLite/session lineage while introducing explicit run/event/read models where needed;
- correlate Langfuse/Nemo Relay observability with local durable run identity;
- distinguish gateway process health, session activity, cron execution, subagent delegation, and model/tool outcomes;
- keep secrets/configuration mutation separate from general observability permissions;
- honor the project’s narrow-core/plugin-and-skill extension philosophy.

## Source repositories

All listed repositories exceed 5 stars and/or forks:

- `paperclipai/paperclip` — durable run model, company control plane, approvals, budgets, activity, and hybrid live updates: https://github.com/paperclipai/paperclip
- `langfuse/langfuse` — traces, sessions, prompts, cost, scores, datasets, experiments, and OpenTelemetry integration: https://github.com/langfuse/langfuse
- `Arize-ai/phoenix` — AI tracing, evaluation, datasets, experiments, OpenInference, and agent-oriented investigation: https://github.com/Arize-ai/phoenix
- `AgentOps-AI/agentops` — agent sessions, tool/LLM events, cost, errors, and monitoring integrations: https://github.com/AgentOps-AI/agentops
- `openlit/openlit` — OpenTelemetry-native LLM/agent observability and cost/quality monitoring: https://github.com/openlit/openlit
- `open-telemetry/opentelemetry-specification` — vendor-neutral traces, metrics, logs, context propagation, and semantic conventions: https://github.com/open-telemetry/opentelemetry-specification

Role-derived material was refactored from `engineering-multi-agent-systems-architect.md`. Revalidate current APIs and telemetry conventions before implementation.
