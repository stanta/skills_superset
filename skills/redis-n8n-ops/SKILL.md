---
name: redis-n8n-ops
description: This skill should be used when designing, implementing, reviewing, or operating Redis usage and Redis integrations with self-hosted n8n workflows, including cache design, queues, locks, rate limits, Pub/Sub, Streams, Redis Chat Memory, Redis Vector Store, n8n queue mode, Docker configuration, persistence, security, observability, and failure handling.
---

# Redis Operations and n8n Integration

## Purpose

Use this skill to design safe, observable, and production-ready Redis usage for this repository's workflow automation, advertising analytics, AI-agent, and bot-adjacent systems.

Focus on:

- Redis data modeling for cache, coordination, queue, Pub/Sub, Streams, counters, locks, and AI memory;
- Redis operational configuration for persistence, eviction, security, resource limits, and monitoring;
- n8n Redis node usage, Redis Trigger, Redis Tool, Redis Chat Memory, Redis Vector Store, and n8n queue mode;
- idempotent workflow contracts, retry safety, and bounded retention;
- Docker/self-hosted deployment patterns for n8n plus Redis.

## When to use

Use this skill when the user asks about:

- Redis best practices, Redis architecture, Redis persistence, Redis cache, Redis locks, Redis queues, Redis Streams, Pub/Sub, rate limits, or counters;
- integrating Redis with n8n workflows, n8n queue mode, Redis credentials, Redis Trigger, Redis Tool, Redis Chat Memory, or Redis Vector Store;
- caching API/report outputs in workflows;
- passing state between n8n executions or workers;
- scaling self-hosted n8n with Redis-backed execution queues;
- reducing duplicate work, adding idempotency, or coordinating long-running automations.

## Decision model

Choose the Redis pattern by workload:

1. **Cache with TTL** for expensive API/report responses that can be recomputed.
2. **Atomic counters** for rate limits, quotas, attempt counters, and lightweight metrics.
3. **Locks with TTL and owner tokens** for short critical sections only.
4. **Lists** for simple FIFO queues when at-least-once recovery is not critical.
5. **Streams with consumer groups** for recoverable event processing, replay, and pending-message inspection.
6. **Pub/Sub** only for ephemeral notifications where message loss is acceptable.
7. **n8n queue mode Redis** only for execution distribution; keep it isolated from application cache/session keys.
8. **Redis Chat Memory / Vector Store** only when retention, privacy, TTL, and index lifecycle are explicit.

## Redis-only best practices

### 1. Classify Redis data by durability and blast radius

Before adding Redis, classify every key family:

| Class | Examples | Default rule |
|---|---|---|
| Ephemeral cache | API response cache, rendered report summary | TTL required; recomputable |
| Coordination | locks, dedupe markers, rate limits | TTL required; small values |
| Queue/event | workflow tasks, webhook events | Prefer Streams for recovery |
| Session/memory | chat history, user workflow context | TTL and privacy policy required |
| Durable state | business records, billing, final reports | Do not use Redis as the only source of truth unless explicitly designed and backed up |

Treat Redis as a high-speed operational store, not a default replacement for PostgreSQL, files, or durable workflow records.

### 2. Use disciplined key naming

Use stable namespaces with environment, system, entity, identifier, and purpose:

```text
{env}:{app}:{domain}:{entity}:{id}:{purpose}
prod:fd:n8n:direct:campaign:123:summary:v1
prod:fd:locks:workflow:J7UZmwat5lTbErHb:execution:15608
prod:fd:ratelimit:yandex-direct:token-hash:minute
prod:fd:dedupe:webhook:sha256-payload
```

Rules:

- include environment prefix to avoid dev/prod collisions;
- include version suffix for serialized payload contracts;
- avoid unbounded user-provided text in keys; hash long identifiers;
- keep keys discoverable by prefix, but do not depend on production-wide `KEYS` scans;
- document every key family with owner, TTL, value shape, and cleanup behavior.

### 3. Make TTL explicit for cache and coordination keys

Every cache, lock, dedupe, session, and temporary workflow key must have a TTL.

Recommended TTL ranges:

| Use case | Typical TTL |
|---|---:|
| API response cache | 5-60 minutes |
| report run dedupe marker | 1-7 days |
| distributed lock | seconds to a few minutes |
| rate-limit bucket | matching window plus safety margin |
| n8n chat memory | product-defined session lifetime, never default infinite |
| temporary workflow payload pointer | hours to days |

Avoid writing cache keys with `SET` and no expiry unless the key is intentionally durable and covered by retention documentation.

### 4. Configure memory limits and eviction policy intentionally

Set `maxmemory` for Redis containers. Do not let Redis consume unbounded host memory.

Cache-only instances can use an eviction policy such as:

```text
maxmemory 512mb
maxmemory-policy allkeys-lru
```

Mixed-use or queue/session instances should avoid evicting critical keys silently. Prefer:

```text
maxmemory 512mb
maxmemory-policy noeviction
```

Then fail loudly and alert before data loss. If using one Redis for multiple purposes in a small local setup, keep memory headroom and use short TTLs to reduce eviction pressure.

### 5. Separate Redis databases or instances by purpose

Prefer separate Redis instances for:

- n8n queue mode internals;
- application cache and locks;
- AI chat memory or vector indexes;
- test/dev workloads.

If separate instances are not feasible, use separate logical databases and strict prefixes, but remember that logical databases share CPU, memory, persistence, and failure blast radius.

### 6. Choose persistence based on data class

Use persistence only when Redis contains data that must survive restart.

Common configuration choices:

```text
appendonly yes
appendfsync everysec
```

Use AOF `everysec` for a practical durability/performance tradeoff. Use RDB snapshots for backup-style point-in-time recovery. Avoid assuming persistence turns Redis into a relational database; application-level idempotency and replay remain required.

For pure cache instances, persistence can be disabled if warmup cost is acceptable. For n8n queue mode, follow n8n deployment guidance and test restart behavior with active executions.

### 7. Use atomic operations instead of read-modify-write

Prefer Redis atomic commands:

- `INCR` / `INCRBY` with `EXPIRE` for counters and rate limits;
- `SET key value NX EX seconds` for lock acquisition or dedupe markers;
- Lua scripts only when multi-key atomicity is required and scripts are reviewed;
- Streams `XADD`, `XREADGROUP`, `XACK`, `XAUTOCLAIM` for recoverable processing.

Do not implement race-sensitive logic by `GET`, compute in workflow code, then `SET` without atomic guards.

### 8. Implement locks safely

Use locks only for short critical sections. Include:

- unique owner token in the lock value;
- TTL on acquisition;
- compare-token-on-release logic;
- timeout and fallback behavior;
- logs for acquisition failure and lock expiry.

Pattern:

```text
SET prod:fd:lock:report:campaign-123 <owner-token> NX EX 120
```

Never create locks without TTL. Avoid long-running locks around external APIs, browser automation, or LLM calls unless the lock TTL and renewal strategy are explicit.

### 9. Prefer Streams over Pub/Sub for workflow events that matter

Use Pub/Sub for transient fan-out notifications only. If a workflow must recover after worker restart, inspect pending work, replay messages, or guarantee at-least-once processing, use Redis Streams with consumer groups.

For Streams:

- set bounded retention with approximate max length;
- include event ID, source workflow ID, execution ID, schema version, and idempotency key in the payload;
- acknowledge only after durable side effects are complete;
- inspect pending entries and reclaim stalled messages;
- route poison messages to a dead-letter stream or durable error log.

### 10. Store compact values and avoid large payloads

Redis is not object storage. Avoid storing large files, screenshots, raw CSV exports, or full report datasets directly in Redis.

Preferred pattern:

1. Store large artifacts in files/object storage/database.
2. Store a compact Redis pointer with TTL.
3. Include checksum, size, content type, and expiration.

Example pointer value:

```json
{
  "status": "ready",
  "path": "/data/marts/J7UZmwat5lTbErHb/15608/result.parquet",
  "sha256": "...",
  "row_count": 1200,
  "expires_at": "2026-08-04T00:00:00Z"
}
```

### 11. Secure Redis by default

For production or shared environments:

- bind Redis only to private interfaces or Docker networks;
- require authentication and use ACL users with least privilege;
- enable TLS when traffic leaves a trusted host/network;
- keep Redis passwords in n8n credentials or environment variables, never workflow JSON or repository files;
- disable dangerous commands or restrict them through ACL where appropriate;
- avoid exposing Redis to the public internet;
- redact Redis URLs and credentials from logs.

### 12. Monitor Redis as an operational dependency

Track:

- memory used, memory fragmentation, maxmemory pressure, evicted keys;
- connected clients, blocked clients, rejected connections;
- command latency and slowlog;
- keyspace hits/misses by cache family;
- persistence status, AOF/RDB rewrite status, last save time;
- Stream pending counts and oldest pending age;
- n8n queue depth and worker processing latency when queue mode is enabled.

Use `INFO` for diagnostics, but avoid making production workflows parse huge `INFO` payloads repeatedly.

## Redis and n8n integration best practices

### 1. Know the built-in n8n Redis capabilities

n8n includes these relevant Redis nodes:

| Node | Type | Use |
|---|---|---|
| `n8n-nodes-base.redis` | regular node | `Get`, `Set`, `Delete`, `Increment`, `Info`, `Keys`, `Push`, `Pop`, `Publish`, `List Length` |
| `n8n-nodes-base.redisTrigger` | trigger | subscribe to Redis channels |
| `n8n-nodes-base.redisTool` | AI tool variant | allow AI Agent workflows to access Redis under a narrow tool description |
| `@n8n/n8n-nodes-langchain.memoryRedisChat` | LangChain memory | store chat history in Redis with configurable session TTL |
| `@n8n/n8n-nodes-langchain.vectorStoreRedis` | LangChain vector store | use Redis as a vector index for AI retrieval |

Prefer built-in nodes before community nodes. If recommending a community Redis node, verify its GitHub repository has at least 5 stars or 5 forks before adopting it into project/common skills.

### 2. Separate n8n queue-mode Redis from workflow Redis

n8n queue mode uses Redis as the broker for distributed executions. Do not mix queue-mode keys with application cache, chat memory, or vector search if avoidable.

Minimum queue-mode principle:

```text
EXECUTIONS_MODE=queue
QUEUE_BULL_REDIS_HOST=redis-queue
QUEUE_BULL_REDIS_PORT=6379
```

Rules:

- set the same encryption key and database configuration on main and worker containers;
- scale workers separately from the main/webhook process;
- keep queue Redis private and monitored;
- test restart, worker crash, and Redis restart behavior before production;
- do not use n8n queue Redis as a general workflow scratchpad.

### 3. Use Redis node operations conservatively

Use `Set` only with expiration when the value is a cache/session/temporary marker. If the n8n UI operation does not expose the exact Redis command needed, prefer a Code node with a vetted Redis client or a small internal service rather than unsafe workarounds.

Avoid `Keys` in production workflows for broad patterns. Prefer:

- known deterministic keys;
- indexed sets maintained by the workflow;
- SCAN through vetted code/service when key iteration is unavoidable.

### 4. Design n8n cache-aside workflows

Recommended cache-aside flow:

1. Build deterministic cache key from normalized inputs and schema version.
2. Redis `Get` cache key.
3. If hit: validate payload version and return cached result.
4. If miss: fetch source API/report data.
5. Validate result contract.
6. Redis `Set` with TTL.
7. Return response with `cache_status`, `cache_key_hash`, and source diagnostics.

Never cache failed authorization, malformed input, or partial upstream errors as successful results. Optionally cache transient negative results only with a very short TTL and explicit status.

### 5. Use Redis for idempotency in retryable n8n workflows

For webhook and scheduled workflows that may retry:

- create an idempotency key from source event ID, normalized payload hash, or report parameters;
- use `SET NX EX` semantics to claim work;
- store final result pointer under a separate result key;
- let duplicate executions return the existing result if complete;
- expire dedupe markers according to replay requirements.

If the built-in Redis node cannot express `SET NX EX`, implement the claim in a small service or vetted Code node.

### 6. Prefer service wrappers for advanced Redis commands

n8n's built-in Redis node is useful for simple operations but limited for advanced Redis patterns. Use a small internal API/service when workflows require:

- `SET NX EX` lock/dedupe semantics;
- `SCAN` iteration;
- Streams consumer groups;
- Lua scripts;
- JSON serialization validation;
- compare-and-delete lock release;
- Redis Cluster/Sentinel-specific behavior;
- strong observability and tests.

This keeps complex concurrency logic in normal code instead of a visual workflow canvas.

### 7. Handle Redis failures explicitly in workflows

Classify Redis failures:

| Error class | Workflow behavior |
|---|---|
| Cache unavailable | bypass cache if source API can tolerate load; emit warning |
| Queue-mode Redis unavailable | stop or fail deployment; n8n execution distribution is unsafe |
| Lock acquisition failed | return busy/duplicate/in-progress status, not a generic crash |
| Memory/noeviction error | fail fast, alert, reduce TTL/value size, increase memory |
| Serialization/version mismatch | ignore cache and rebuild; do not parse blindly |
| Auth/TLS failure | fail fast; fix credentials/configuration |

Do not silently continue when Redis is used for correctness, deduplication, locks, queues, or chat memory.

### 8. Protect AI-agent Redis access

When using `redisTool` or Redis Chat Memory:

- give the AI tool a narrow description and key prefix scope;
- never allow arbitrary key names from model output without prefix validation;
- avoid exposing secrets, credentials, raw user PII, or full private chat history;
- set `sessionTTL` for Redis Chat Memory; avoid `0` unless indefinite retention is approved;
- include tenant/user/session boundaries in keys;
- add prompt-injection tests for attempts to read unrelated keys.

### 9. Use Redis Vector Store only with index lifecycle discipline

For Redis vector indexes:

- define embedding model, vector dimension, distance metric, schema, and index name explicitly;
- version indexes when embedding model or chunking changes;
- separate dev/test/prod indexes;
- track document IDs, source checksum, ingestion version, and deletion behavior;
- validate retrieval quality with evals before relying on AI answers;
- do not mix unrelated tenants or confidential corpora in one unscoped index.

### 10. Docker compose baseline for local n8n plus Redis

For local development, use a private Docker network and named volume:

```yaml
services:
  redis:
    image: redis:7-alpine
    command: ["redis-server", "--appendonly", "yes", "--appendfsync", "everysec", "--maxmemory", "512mb", "--maxmemory-policy", "noeviction"]
    volumes:
      - redis_data:/data
    networks:
      - n8n_internal
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5

  n8n:
    environment:
      - EXECUTIONS_MODE=regular
    depends_on:
      redis:
        condition: service_healthy
    networks:
      - n8n_internal

volumes:
  redis_data:

networks:
  n8n_internal:
    driver: bridge
```

For queue mode, use a dedicated Redis service such as `redis-queue` and keep application Redis separate as `redis-app`.

## Recommended architecture for this repository

For the current workspace, prefer this order:

1. **Local development:** add a dedicated Redis container beside self-hosted n8n only when a workflow needs caching, dedupe, queue mode, AI memory, or rate limiting.
2. **Workflow cache/dedupe:** use Redis as a bounded cache and idempotency layer for expensive report/API calls, with deterministic keys and TTL.
3. **Queue mode:** introduce a separate Redis only when n8n executions need worker scaling or long-running job isolation.
4. **Advanced concurrency:** implement Redis locks/Streams in a small Python/Node service and call it from n8n through HTTP.
5. **AI memory/vector use:** require explicit privacy/retention, session TTL, evaluation, and prompt-injection guardrails before enabling.

Avoid making Redis the only durable store for final advertising reports, user deliverables, or source-of-truth campaign data.

## Implementation checklist

Before implementation:

- Define Redis purpose: cache, queue, lock, rate limit, Stream, Pub/Sub, memory, or vector store.
- Decide whether data is recomputable or durable.
- Define key namespace, TTL, value schema, and owner.
- Decide eviction policy and memory limit.
- Decide whether persistence is needed.
- Decide whether built-in n8n Redis nodes are enough or a service wrapper is safer.

During implementation:

- Use deterministic keys and schema versions.
- Set TTLs on temporary keys.
- Use atomic commands for correctness-sensitive logic.
- Keep large payloads outside Redis and store pointers.
- Add error paths for Redis unavailable, auth failure, memory pressure, and malformed cached values.
- Log cache hits/misses, lock decisions, queue IDs, Stream IDs, and execution IDs.

Before production:

- Test Redis restart, n8n restart, worker crash, and duplicate execution scenarios.
- Check `INFO`, slowlog, memory usage, and key counts.
- Verify credentials are stored in n8n credentials/environment, not workflow exports.
- Verify network exposure is private.
- Verify backups/persistence if Redis contains non-recomputable data.
- Add runbook steps for clearing only namespaced keys safely.

## Validation checklist for reviews

Reject Redis/n8n designs when:

- cache keys have no TTL;
- Redis is exposed publicly;
- workflow JSON contains Redis credentials;
- broad `KEYS *` is used in production paths;
- locks have no TTL or no owner token;
- queue-mode Redis is shared with arbitrary application keys without documented blast-radius acceptance;
- Redis Chat Memory has `sessionTTL = 0` without explicit retention approval;
- AI agent tools can read/write arbitrary keys;
- large files, CSVs, screenshots, or full report exports are stored directly in Redis;
- Redis is the only copy of business-critical data without backup/replay design.

## External-source notes

Use these verified high-signal sources first:

- `redis/redis` official Redis repository, far above the 5-star/5-fork threshold.
- `redis/docs` official Redis documentation repository, far above the threshold.
- `redis/node-redis` official Node.js Redis client repository, search result shows about 17.5k stars and 1.9k forks.
- `redis/redis-py` official Python Redis client repository, use for Python service wrappers.
- `n8n-io/n8n` official n8n repository, search result shows about 188k stars and 57.7k forks.
- n8n built-in Redis nodes discovered through the local n8n MCP registry: `nodes-base.redis`, `nodes-base.redisTool`, `nodes-base.redisTrigger`, `nodes-langchain.memoryRedisChat`, and `nodes-langchain.vectorStoreRedis`.

Community Redis n8n nodes found during web research, but not adopted here because GitHub stars/forks were not verified from search snippets:

- `MatheusKindrazki/n8n-redis-anyway`;
- `vicenterusso/n8n-nodes-redis-enhanced`.

Verify each repository has at least 5 stars or 5 forks before recommending installation or adding it to common skills.

## Output style when using this skill

When responding with this skill:

1. Give a short diagnosis of the Redis use case.
2. Separate Redis-only guidance from Redis+n8n integration guidance.
3. Recommend one architecture path for this repository.
4. Include risks, failure modes, and mitigations.
5. Include a concrete implementation or review checklist.
