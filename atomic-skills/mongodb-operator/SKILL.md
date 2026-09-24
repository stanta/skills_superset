---
name: mongodb-operator
description: This skill should be used when designing, reviewing, or troubleshooting MongoDB usage in application code, including schemas, indexes, query paths, collection growth, persistence failures, and operational safeguards in repositories that use MongoDB for bot state, memory, queues, or checkpoints.
---

# MongoDB Operator

## Overview

Operate MongoDB-backed application flows with attention to correctness, index quality, write semantics, and recovery behavior. Focus on collections, query patterns, queue durability, memory retrieval, checkpoint persistence, and operational hygiene.

## When to use

- Change collection schemas, indexes, or query patterns in app code.
- Troubleshoot slow Mongo queries, missing indexes, or persistence inconsistencies.
- Review queue durability, memory-item storage, or checkpoint collections.
- Prepare migrations or collection-level cleanup.
- Debug local or production Mongo connectivity issues that affect bot behavior.

## Core workflow

### 1. Inventory the data paths

- Identify read-heavy, write-heavy, and lifecycle-critical collections.
- Separate user profile data, message history, queue documents, memory items, and checkpoint data.

### 2. Align indexes with query shapes

- Design indexes from actual filters, sorts, and uniqueness guarantees.
- Review queue claim/release flows and retrieval filters for index support.
- Revisit TTL or archival policies where data retention matters.

### 3. Protect write semantics

- Check idempotency for payment and queue workflows.
- Prefer atomic claim/update patterns for work queues.
- Avoid partial updates that can corrupt user profile or checkpoint continuity.

### 4. Treat retrieval and memory as data products

- Validate document shape and metadata completeness for memory items.
- Monitor collection growth and retrieval latency.
- Keep embedding/vector-related collections and indexes explicit.

### 5. Document recovery paths

- Specify fallback behavior when Mongo is unavailable.
- Define what is lost under in-memory fallback or failed writes.

## Repository guidance

Prioritize these files:

- `bot/database.py`
- `bot/memory_system.py`
- `bot/messaging.py`
- `bot/graph/workflow.py`
- `docs/Database.md`
- `docs/Development.md`
- `docker-compose-dev.yml`

## Non-negotiables

- Align indexes with real query paths.
- Preserve atomicity in queue claim/release patterns.
- Distinguish transient data from durable user state.
- Test fallback behavior when Mongo is unavailable.
- Record operational assumptions for local and production environments.

## Deliverables

When using this skill, produce:

1. Collection and query inventory.
2. Index recommendations.
3. Write-path risk notes.
4. Recovery/fallback notes.
5. Required tests or smoke checks.
