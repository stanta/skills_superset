# Realtime Dashboard Playbook

## Protocol template

```yaml
connection:
  transport: websocket|sse|polling
  scope: tenant/profile/resource
  auth: session|single-use-ticket|bearer
  heartbeat_seconds: 30
  idle_timeout_seconds: 90
  reconnect:
    initial_ms: 1000
    multiplier: 2
    max_ms: 30000
    jitter: full
  recovery: replay_from_cursor|authoritative_refetch

event:
  schema_version: v1
  event_id: uuid
  scope_id: string
  entity_type: run|agent|task|approval|activity
  entity_id: string
  entity_version: integer|null
  sequence: integer|null
  event_type: string
  occurred_at: datetime
  durable: boolean
  trace_id: string|null
  payload: object
```

## Cache reconciliation matrix

| Event | Safe patch | Invalidate/refetch |
|---|---|---|
| Entity status with full versioned record | Detail and known lists | Aggregated summary |
| Progress/snippet | Ephemeral detail fields | Never use for durable aggregate |
| Terminal transition | Detail; remove from live list | Summary, history, task/agent views |
| Cost event | Only append if dedupe/version guaranteed | Period totals and forecasts |
| Permission/scope change | No | All affected keys and stream reconnect |
| Unknown schema/version gap | No | Authoritative refetch |

## Client invariants

- A terminal entity cannot return to nonterminal without a new explicit lifecycle identity or authoritative higher version.
- An older entity version cannot replace a newer cached version.
- Repeated event IDs have no additional effect.
- A missing live message is repaired by replay or refetch.
- An ephemeral message cannot create an audit fact.
- Tenant/profile scope is part of every cache and subscription key.
- Background refresh retains last valid data until replacement succeeds.

## Hostile-network test matrix

| Scenario | Expected result |
|---|---|
| Drop connection between persist and publish | Reconnect replay/refetch reveals durable change |
| Deliver event twice | One effective cache transition |
| Deliver versions 5, 7, 6 | Version 6 is rejected after 7 |
| Restart server and lose ephemeral hints | Durable run state remains correct; hints may disappear |
| Open ten tabs | Connections/polls stay within documented coordination budget |
| Deploy all replicas | Drained/reconnected clients recover without a thundering herd |
| Slow consumer | Memory remains bounded; client receives coalesced state or resync instruction |
| Backplane unavailable | Dashboard labels degraded live state and falls back to durable reads |
| Auth revoked while connected | Stream is closed and cache for protected scope is cleared/revalidated |
| Hidden tab for one hour | Poll/live policy follows visibility budget and reconciles on focus |

## Paperclip pattern

The local `paperclip-dashboard-analysis.md` documents a practical hybrid:

- PostgreSQL stores durable runs, events, runtime state, activity, and cost.
- REST constructs summaries and detail read models.
- One company-scoped WebSocket patches or invalidates TanStack Query cache.
- Polling and persisted incremental logs repair missed live updates.
- Reconnect uses bounded exponential backoff.
- Transcript chunks are deduplicated and retention-bounded.
- Overview polls compact previews; run/task detail receives richer live evidence.
- Cross-tab leadership prevents request multiplication.
- The process-local event bus is a known multi-replica limitation.

Use the pattern, not its exact intervals. Set cadence from product freshness SLOs and measured load.

## Multi-replica options

| Backplane | Strength | Caveat |
|---|---|---|
| Redis Pub/Sub | Simple low-latency fan-out | No replay/durability by default |
| Redis Streams | Replay and consumer groups | Operational trimming and ordering scope |
| NATS JetStream | Durable streams, replay, scalable subjects | Additional infrastructure and delivery semantics |
| PostgreSQL LISTEN/NOTIFY | Reuse existing DB, simple invalidation | Payload/throughput limits; not a durable log |
| Kafka | High throughput, durable replay | Significant operational complexity |

Select based on durability, replay, ordering scope, throughput, topology, and team operations—not popularity.

## SLO template

```markdown
| Surface | Freshness SLO | Event-to-paint p95 | Fallback cadence | Stale threshold |
|---|---:|---:|---:|---:|
| Overview | 10 s | 3 s | 15 s | 30 s |
| Active run | 2 s | 750 ms | 3 s | 10 s |
| Audit/history | 60 s | N/A | on demand | 5 min |
```

Replace example values through measurement and product requirements.

## Source repositories

All sources exceed 5 stars and/or forks:

- `paperclipai/paperclip` — hybrid durable state, WebSocket cache updates, polling fallback, and bounded transcripts: https://github.com/paperclipai/paperclip
- `grafana/grafana` — production live observability dashboards, streaming, alerting, and correlations: https://github.com/grafana/grafana
- `TanStack/query` — server-state caching, invalidation, background refetch, and deduplication: https://github.com/TanStack/query
- `nats-io/nats-server` — scalable pub/sub and JetStream durable delivery: https://github.com/nats-io/nats-server
- `redis/redis` — pub/sub, streams, TTL coordination, and cache infrastructure: https://github.com/redis/redis
- `open-telemetry/opentelemetry-specification` — trace context and telemetry semantics: https://github.com/open-telemetry/opentelemetry-specification

Role-derived guidance was refactored from `engineering-realtime-collaboration-engineer.md`, narrowed to dashboard consistency rather than collaborative document convergence.
