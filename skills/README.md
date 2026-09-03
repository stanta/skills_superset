# Hermes Dashboard Skills

This project skill pack separates dashboard work into five narrowly owned capabilities so an agent can load only the guidance needed for the current task.

## Routing matrix

| Task | Primary skill | Typical companion |
|---|---|---|
| Define audience, KPI semantics, hierarchy, filters, drill-down, and actions | `dashboard-product-architecture` | `dashboard-quality-gates` |
| Select or review charts, KPI cards, tables, color, axes, and rendering | `dashboard-data-visualization` | `dashboard-product-architecture` |
| Design agent runs, traces, tools, costs, evaluations, approvals, recovery, and audit | `ai-agent-control-plane-dashboard` | `dashboard-realtime-consistency` |
| Build WebSocket/SSE/polling/cache/reconnect/multi-replica behavior | `dashboard-realtime-consistency` | `ai-agent-control-plane-dashboard` |
| Plan tests, audit quality, or define release gates | `dashboard-quality-gates` | The skill defining the behavior under test |

## Recommended implementation sequence

1. Apply `dashboard-product-architecture` to define the audience, questions, metric contracts, surfaces, filters, states, and actions.
2. Apply `ai-agent-control-plane-dashboard` when the product includes autonomous agents, LLM traces, tools, evaluations, budgets, approvals, or operator intervention.
3. Apply `dashboard-data-visualization` to encode approved metrics and evidence truthfully.
4. Apply `dashboard-realtime-consistency` to define freshness, event schemas, cache reconciliation, polling fallback, reconnect, and replica fan-out.
5. Apply `dashboard-quality-gates` to convert all contracts into deterministic, accessibility, security, resilience, E2E, and performance checks.

## Hermes-specific use

For the current Hermes codebase:

- preserve machine/profile scope and visible write targets;
- distinguish gateway process health, active sessions, cron runs, delegated agents, model/tool execution, and observability traces;
- use the existing React 19/TypeScript/FastAPI/plugin architecture rather than introducing a separate dashboard stack by default;
- treat SQLite/session state and explicit future run/event records as durable truth;
- correlate local state with Langfuse/Nemo Relay telemetry through stable run/trace identifiers;
- retain safe polling and authoritative refetch around live WebSocket surfaces;
- keep plugin widgets permissioned, isolated, bounded, and tested.

## Evidence policy

The reference documents cite established GitHub repositories that meet the requested 5+ stars and/or forks threshold. They also incorporate the local `paperclip-dashboard-analysis.md` and refactor relevant knowledge from the existing skill catalog and `agency-agents` roles.

Treat repository-derived patterns as evidence, not immutable rules. Revalidate current versions and authoritative library documentation before implementation.

## Existing global skills to combine when needed

- `frontend-react-dev` for React architecture and implementation quality.
- `monitoring-expert` for Prometheus/Grafana infrastructure observability.
- `llm-observability-ops` and `langfuse` for telemetry instrumentation.
- `api-designer` for REST/OpenAPI contracts.
- `security` or `security-reviewer` for threat modeling and audit.
- `test-master` and `playwright-expert` for test implementation.
- `web-design-guidelines` for fresh UI guideline audits.

The project skills specialize these capabilities for dashboards; they do not duplicate full framework, observability vendor, or security implementation guidance.
