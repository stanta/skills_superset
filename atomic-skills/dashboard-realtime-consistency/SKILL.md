---
name: dashboard-realtime-consistency
description: This skill should be used when designing, implementing, debugging, or reviewing live dashboard data delivery and consistency across REST, WebSocket, SSE, polling, caches, tabs, replicas, and reconnects. Apply it to durable-vs-ephemeral state classification, event envelopes, cache patch/invalidation, replay or refetch recovery, backoff, visibility-aware polling, fan-out backplanes, backpressure, and event-to-paint SLOs; do not use it for collaborative text editing unless that is the actual product requirement.
---

# Dashboard Realtime Consistency

## Purpose

Deliver low-latency dashboard updates without making an unreliable live connection the only source of truth. Design for loss, duplication, reordering, reconnect, stale caches, hidden tabs, slow consumers, server restarts, and multiple replicas.

Load `references/realtime-dashboard-playbook.md` for the protocol template, failure matrix, Paperclip-derived pattern, and source provenance.

## Boundary

- Own transport choice, event protocol, reconnect, resume/refetch, cache reconciliation, polling, cross-tab coordination, backpressure, and fan-out topology.
- Defer dashboard semantics and hierarchy to `dashboard-product-architecture`.
- Defer agent entity/state semantics to `ai-agent-control-plane-dashboard`.
- Defer visual rendering choices to `dashboard-data-visualization`.
- Coordinate verification with `dashboard-quality-gates`.

## Default architecture

Prefer:

```text
Durable facts → query/read-model API → client cache → UI
       └──────→ live event publication → WebSocket/SSE cache patch/invalidate
Query/read-model API ← visibility-aware polling and reconnect reconciliation
```

Use realtime as acceleration. Recover correctness from durable APIs, persisted logs/events, or replayable streams.

## Workflow

### 1. Classify each datum

Record:

| Class | Examples | Guarantee |
|---|---|---|
| Durable fact | run status, approval, audit, cost | Persisted, queryable after restart |
| Derived read model | dashboard summary, rates | Rebuildable from facts; freshness defined |
| Ephemeral hint | current tool, typing/presence, transient snippet | TTL, lossy, never authoritative |
| Command state | cancel/retry request | Idempotent request plus durable outcome reconciliation |

Never let ephemeral fields overwrite terminal durable facts.

### 2. Choose transport by semantics

- Use WebSocket for bidirectional commands or dense multiplexed updates.
- Use SSE for server-to-client streams with browser-native reconnect where one-way delivery suffices.
- Use polling for low-frequency summaries, fallback, constrained networks, and reconciliation.
- Use incremental range/offset APIs for append-only logs.
- Use an external pub/sub or durable stream for multi-replica fan-out when process-local events are insufficient.

Document proxy, authentication, authorization, heartbeat, connection drain, and maximum payload behavior.

### 3. Define the event envelope

Include:

- schema version;
- event ID and deduplication identity;
- tenant/profile scope;
- entity type and ID;
- event type;
- server timestamp;
- ordering sequence or cursor where required;
- payload version or entity version;
- durability/replay classification;
- trace/correlation ID.

Avoid using wall-clock timestamps alone for ordering. Define whether ordering is global, tenant-scoped, stream-scoped, or entity-scoped.

### 4. Choose patch versus invalidation

Patch cache only when the event contains a complete, versioned, unambiguous update and can be applied idempotently. Invalidate/refetch when:

- aggregates depend on multiple entities;
- permissions or scope may have changed;
- an event is partial;
- event ordering is uncertain;
- business rules are server-owned;
- client schema may be stale.

Guard terminal states from regression and reject older entity versions. Reconcile after reconnect even if replay is supported.

### 5. Design reconnect before connect

- Use exponential backoff with jitter and a cap.
- Reset backoff only after stable success, not a momentary open.
- Authenticate reconnect through a safe session/ticket mechanism.
- Track last sequence/cursor when replay exists.
- If replay is unavailable, refetch authoritative snapshots and resume incremental logs.
- Surface disconnected and stale states without erasing valid cached data.
- Pause or slow retries while offline/hidden when appropriate.

### 6. Coordinate polling and tabs

- Centralize one connection per tenant/profile browser context when practical.
- Deduplicate identical polling intervals and requests.
- Elect a leader or use BroadcastChannel/shared coordination across tabs for expensive resources.
- Prevent older distributed results from replacing newer cache values.
- Slow/pause noncritical polling in hidden tabs.
- Keep a safety-net cadence during live connection health, and shorten fallback cadence when live delivery is unavailable.

### 7. Bound data and backpressure

- Limit queued events per client.
- Coalesce superseded progress/presence updates.
- Batch cache updates and rendering.
- Bound transcript/log chunks by count and bytes while preserving offsets.
- Drop-and-resync rather than allowing unbounded memory growth.
- Rate-limit reconnects and commands.
- Define maximum sockets, messages/sec, bytes/sec, and hot-scope fan-out.

### 8. Scale across replicas

For multiple server replicas, define:

- how an event produced on replica A reaches a client on replica B;
- backplane technology and delivery semantics;
- subscription scope and authorization;
- ordering/deduplication behavior;
- deploy drain and reconnect hints;
- sticky-session assumptions, if any;
- degraded mode when the backplane fails.

Do not assume a process-local event emitter works across replicas.

### 9. Instrument realtime quality

Measure:

- event-produced to persisted;
- persisted to published;
- published to received;
- received to cache-applied;
- cache-applied to painted;
- connection success/churn;
- reconnect and resume success;
- replay gap/refetch frequency;
- duplicate/out-of-order/stale-drop counts;
- polling fallback traffic;
- queue depth, dropped/coalesced events, and per-client bytes.

Define SLOs by surface. Overview may accept seconds; a run detail may require subsecond progress.

### 10. Deliver protocol and tests

Produce:

1. State classification table.
2. Transport and topology diagram.
3. Event schemas and ordering guarantees.
4. Cache patch/invalidation matrix.
5. Reconnect/resume/refetch algorithm.
6. Polling and cross-tab strategy.
7. Backpressure and retention budgets.
8. Multi-replica design.
9. Security scope.
10. Hostile-network/load test plan and SLOs.

## Non-negotiables

- Design for at-least-once and missing-message realities unless stronger guarantees are proven.
- Make updates idempotent and stale-aware.
- Preserve durable terminal state over ephemeral progress.
- Keep UI useful while disconnected; label freshness.
- Authenticate and authorize every stream by target scope.
- Test reconnect storms, replica mismatch, duplicate/reordered messages, server restart, tab multiplication, and slow consumers.
