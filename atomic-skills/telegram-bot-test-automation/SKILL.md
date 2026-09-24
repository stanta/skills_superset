---
name: telegram-bot-test-automation
description: This skill should be used when designing, implementing, reviewing, or operating automated test environments for Python Telegram bots, especially pytest-based unit, integration, and end-to-end tests for python-telegram-bot, Pyrogram/Kurigram userbot drivers, Telegram Bot API mocking, conversation state machines, media uploads, and CI-safe regression suites.
---

# Telegram Bot Test Automation

Use this skill to build reliable automated testing for Telegram bots without leaking tokens, relying on manual chats, or coupling all coverage to the live Telegram network. Prefer a layered strategy: deterministic unit tests first, local Bot API/transport contract tests second, and a small gated live E2E suite driven by a Telegram user client only when credentials are explicitly available.

## Scope

Apply this skill when working on:

- Python Telegram bots built with `python-telegram-bot`, `aiogram`, Pyrogram-compatible frameworks, or custom Bot API clients.
- Conversation/state-machine tests for `/start`, `/help`, `/cancel`, menu buttons, inline callbacks, uploads, validation errors, retries, and successful flows.
- Test harnesses that simulate Telegram `Update` objects, Bot API responses, userbot-driven chats, file downloads, media uploads, and polling/webhook delivery.
- CI pipelines that must run most tests without Telegram credentials and run live smoke tests only behind explicit opt-in variables.

For the `reports_ad` project, keep the runtime on `python-telegram-bot` polling unless product scope changes. Use Pyrogram/Kurigram primarily as a live userbot E2E driver, not as a reason to rewrite the bot runtime.

## Research baseline

Use the current research summary in `references/research-summary.md` before making dependency decisions. The key conclusions are:

- Original Pyrogram is archived and should not be selected for new actively maintained test infrastructure.
- Kurigram is the strongest current Pyrogram-compatible fork found during research: actively maintained, drop-in oriented, and above the 5-star/5-fork threshold.
- Pyrofork and PyroTGFork are viable alternatives but showed less favorable combined activity/popularity signals during the 2026-07-16 check.
- `tgintegration` is useful to study because it is Pyrogram-based and focuses on real-time Telegram bot integration tests, but assess maintenance and compatibility before adopting it directly.

## Layered test strategy

### 1. Pure unit tests

Implement most coverage without network access:

- Instantiate fake or factory-made `Update`, `Message`, `CallbackQuery`, `User`, `Chat`, and context objects.
- Call handlers directly with `pytest` and `pytest-asyncio`.
- Assert returned states, mutated `context.user_data`, `context.bot_data`, reply text, reply markup, sent photos/documents, and cleanup behavior.
- Mock heavy dependencies: screenshot generation, OCR/LLM calls, database writes, queues, file downloads, and Telegram uploads.
- Cover boundary cases: empty text, unknown commands, duplicate callback clicks, oversized files, wrong MIME, invalid URLs, repeated `/cancel`, user lock contention, timeout mapping, and safe user-facing errors.

For `python-telegram-bot`, keep tests close to the handler contract used in the project: async handler function plus update/context fakes. Avoid requiring a real `Application` unless testing handler registration or lifecycle behavior.

### 2. Bot API/transport contract tests

Add a thin layer that verifies Telegram API integration without talking to Telegram production:

- Use HTTP mocking (`respx`, `pytest-httpx`, `responses`, or equivalent) for Bot API clients that use `httpx`/`aiohttp`/`requests`.
- Assert request method, endpoint, payload shape, multipart upload fields, timeout behavior, retry decisions, and redaction.
- When using polling code, simulate `getUpdates` responses and verify offset advancement, duplicate update handling, and graceful shutdown.
- When using webhooks, test signature/secret-token validation, idempotency, and parsing of raw JSON into framework update objects.

### 3. Local or sandbox integration tests

Use this layer for end-to-end application wiring while still avoiding real user accounts:

- Start the bot in-process or as a subprocess with fake tokens and fake downstream services.
- Route Bot API traffic to a mock server or local Telegram Bot API test double.
- Verify handler registration, dependency injection, environment parsing, logging, metrics, and cleanup in one integrated run.
- Mark these tests separately, for example `@pytest.mark.integration`, so regular unit runs remain fast.

### 4. Live Telegram E2E tests

Run live tests only when explicitly requested and only with private test credentials:

- Use a dedicated test bot token and a dedicated Telegram test user account.
- Drive the bot with Kurigram as a Pyrogram-compatible userbot client.
- Store API ID, API hash, bot username, bot token, and session string in CI secrets or local `.env` files excluded from version control.
- Gate with an environment flag such as `TELEGRAM_E2E=1`; skip by default.
- Keep the suite small: `/start`, happy-path conversation, one validation failure, one cancel path, one media upload, and one timeout/error path if safely triggerable.
- Add message cleanup where possible and avoid testing in shared production chats.

## Recommended Pyrogram-compatible fork

Prefer Kurigram for new live Telegram E2E drivers when a Pyrogram-style client is needed.

Selection rationale from public sources and GitHub API research on 2026-07-16:

- `pyrogram/pyrogram`: archived, about 4616 stars and 1385 forks, not suitable for new active maintenance.
- `KurimuzonAkuma/kurigram`: active fork, about 776 stars and 208 forks, recently pushed, documented as actively maintained and drop-in oriented.
- `Mayuri-Chan/pyrofork`: active fork, about 289 stars and 155 forks, recently pushed, viable but lower momentum than Kurigram in this comparison.
- `TelegramPlayGround/PyroTGFork`: active fork, about 209 stars and 58 forks, viable but lower momentum than Kurigram in this comparison.

Pin the dependency conservatively in test extras only, for example `kurigram>=2.1,<3`, and keep imports under test-only modules. Re-check GitHub activity before major adoption because Telegram client ecosystems change quickly.

## Live E2E harness pattern with Kurigram

Create a test-only harness that mirrors user behavior:

1. Load secrets from environment: `TELEGRAM_API_ID`, `TELEGRAM_API_HASH`, `TELEGRAM_SESSION_STRING`, `TELEGRAM_BOT_USERNAME`, and optional `TELEGRAM_E2E_TIMEOUT`.
2. Start a Kurigram `Client` using a saved string session or an isolated session file outside the repository.
3. Send messages to the bot username one at a time.
4. Wait for bot responses with bounded timeouts and strong filters: chat ID, sender bot, text/caption, media type, and correlation token if the bot supports one.
5. Assert the external behavior, not internal implementation details.
6. Clean up sent/received messages when possible.
7. Disconnect the client in `finally` and never print session strings.

Avoid broad sleeps. Prefer polling with short intervals, event handlers, or conversation helpers that wait until a matching response appears. Make every assertion deterministic and timeout-bounded.

## Test data and fixtures

Maintain fixtures for:

- Minimal fake text messages and commands.
- Callback query/menu button updates.
- Telegram file metadata and downloaded local files.
- Valid and invalid media samples with exact MIME/size/dimension boundaries.
- Fake bot/context objects that record replies, documents, photos, edits, deletes, and chat actions.
- Downstream service fakes for screenshot generation, OCR/LLM, queues, and storage.
- Environment-variable fixtures that prevent accidental use of production tokens.

Prefer small generated media in temporary directories over committed large binaries unless visual fidelity is required.

## CI and safety requirements

- Run unit tests on every change.
- Run integration tests on pull requests when they do not require external credentials.
- Run live Telegram E2E only manually, nightly, or on protected branches with explicit secret availability.
- Mark tests clearly: `unit`, `integration`, `telegram_e2e`, `slow`, `network`.
- Fail fast if live credentials are incomplete; skip rather than partially running with production-like defaults.
- Redact bot tokens, API hash, session strings, chat IDs, user IDs, file IDs, and full URLs with UTM values from logs.
- Avoid parallel live tests against the same bot unless the bot supports per-test correlation and isolated conversations.
- Do not run polling live tests against a token already used by another bot instance; Telegram allows only one active `getUpdates` consumer per token.

## Quality checklist

Before considering the Telegram bot test environment complete, verify:

- Handlers are testable as plain async functions with injected dependencies.
- State transitions are covered for success, validation failure, edit/back/cancel, and duplicate input.
- Telegram API calls are mocked or recorded by fakes in unit tests.
- File/media handling is tested without external downloads in unit tests.
- User-facing errors are asserted to be safe and non-technical.
- Cleanup is tested for success, validation error, cancellation, timeout, and unexpected exception.
- Live E2E tests are opt-in, documented, timeout-bounded, and credential-safe.
- Kurigram/Pyrogram-compatible dependencies are isolated to test extras unless the production runtime needs MTProto.
