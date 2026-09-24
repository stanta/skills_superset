---
name: telegram-ai-bot-runtime
description: This skill should be used when building, debugging, or scaling Telegram bots that combine `python-telegram-bot`, async handlers, AI inference, queueing, media inputs, payment flows, and per-user concurrency control, especially in `bot/bot.py`, `bot/messaging.py`, and adjacent runtime modules.
---

# Telegram AI Bot Runtime

## Overview

Operate Telegram bot runtimes that mix chat UX, async update handling, AI calls, media processing, and billing-sensitive workflows. Focus on handler boundaries, per-user sequencing, resilience, and platform-specific runtime pitfalls.

## When to use

- Add or change Telegram handlers, callback flows, commands, or middleware-like runtime logic.
- Debug message ordering, duplicate processing, blocked handlers, or media-processing delays.
- Review webhook versus polling behavior.
- Change payment, reminder, onboarding, or queue-drain behavior.
- Improve concurrency control around AI responses.

## Core workflow

### 1. Classify the update path

- Command handler
- Text message handler
- Callback query
- Media upload
- Payment event
- Background broadcast or reminder

### 2. Preserve per-user sequencing

- Keep semaphore or queue-based protections intact for concurrent user messages.
- Store queued payloads durably when the bot cannot process immediately.
- Preserve FIFO order for replayed messages.

### 3. Keep the handler thin

- Parse Telegram update data.
- Delegate business logic and AI work to separate functions.
- Keep platform-specific code isolated from memory, prompt, or DB logic.

### 4. Treat media and AI latency as a delivery risk

- Avoid blocking the update loop.
- Send placeholders or progress signals when long AI tasks are expected.
- Separate upload parsing from downstream AI generation.

### 5. Keep payments and admin paths explicit

- Route payment callbacks, invoice success, and staff actions through strongly bounded handlers.
- Add defensive logging and idempotency around billing-sensitive paths.

## Repository guidance

Prioritize these files:

- `bot/bot.py`
- `bot/messaging.py`
- `bot/broadcasting.py`
- `bot/onboarding.py`
- `bot/buy.py`
- `bot/stars_server.py`
- `bot/yookassa_server.py`
- `bot/arcpay_server.py`

## Non-negotiables

- Avoid blocking operations in handler execution paths.
- Preserve per-user ordering and queue durability.
- Separate Telegram transport concerns from AI/business logic.
- Add handler tests for new commands, callbacks, and concurrency-sensitive flows.
- Keep payment logic idempotent and auditable.

## Deliverables

When using this skill, produce:

1. Runtime change summary.
2. Update-path map.
3. Concurrency and delivery risk notes.
4. Required handler tests.
5. Rollback steps for runtime regressions.
