# Telegram bot test automation research summary

Research date: 2026-07-16.

## Project context

The current workspace contains `reports_ad`, a Python Telegram polling bot for advertising proof screenshots. It uses `python-telegram-bot` 21+/22+, `telegram_menu`, `pytest`, and `pytest-asyncio`. Existing tests already fake Telegram update/context behavior and avoid real Telegram tokens or network calls for normal regression runs.

Important project constraints:

- Keep Telegram runtime on `python-telegram-bot` polling for now.
- Keep task history non-persistent.
- Validate URL, UTM, file MIME, file size, and image dimensions before heavy browser work.
- Use per-user locks for heavy generation tasks.
- Redact tokens, raw user identifiers, local paths, full URLs with UTM, and uploaded file details in logs.

## Best-practice findings

Recommended testing pyramid:

1. Unit tests: call handlers directly with fake updates/context and mocked downstream services.
2. Bot API contract tests: mock HTTP calls to Telegram Bot API or use a local test double.
3. Local integration tests: run the app with fake services and fake Bot API endpoints.
4. Live E2E tests: drive a dedicated test bot via a Telegram user client only when secrets are explicitly present.

Useful public references found:

- python-telegram-bot Wiki: recommends using a userbot library such as Telethon or Pyrogram for real-environment tests.
- python-telegram-bot testing docs: PTB itself uses pytest and framework-level tests.
- tgintegration: a Pyrogram-based integration test/automation library for Telegram bots.
- End-to-end Telegram bot testing articles: use a Telegram client/session, bounded conversations, and pytest fixtures.

## Pyrogram/fork research

The original Pyrogram repository is archived. For new active work, prefer an actively maintained fork.

GitHub API snapshot collected on 2026-07-16:

| Repository | Status | Stars | Forks | Last push | Notes |
| --- | --- | ---: | ---: | --- | --- |
| `pyrogram/pyrogram` | archived | 4616 | 1385 | 2024-12-23 | Original project; not suitable as active dependency for new test harnesses. |
| `KurimuzonAkuma/kurigram` | active | 776 | 208 | 2026-07-14 | Best current candidate found; advertises active maintenance and drop-in Pyrogram compatibility. |
| `Mayuri-Chan/pyrofork` | active | 289 | 155 | 2026-07-01 | Viable alternative; supports newer Telegram features. |
| `TelegramPlayGround/PyroTGFork` | active | 209 | 58 | 2026-06-28 | Viable alternative; docs available. |

All listed candidate forks exceed the 5-star and/or 5-fork threshold. Kurigram has the best combined activity/popularity signal in this comparison.

## Adoption recommendation

Use Kurigram only for test-time live E2E drivers unless production explicitly requires MTProto functionality. Do not migrate `reports_ad` runtime from `python-telegram-bot` solely for testing.

Suggested optional dependency pattern:

```toml
[project.optional-dependencies]
telegram-e2e = [
  "kurigram>=2.1,<3",
  "pytest-asyncio>=0.23",
  "python-dotenv>=1.0",
]
```

Suggested default command structure:

```bash
pytest
TELEGRAM_E2E=1 pytest -m telegram_e2e
```

## Live E2E credential model

Required secrets for Kurigram-driven live tests:

- `TELEGRAM_API_ID`
- `TELEGRAM_API_HASH`
- `TELEGRAM_SESSION_STRING` or a test-only session file path outside the repository
- `TELEGRAM_BOT_USERNAME`
- optional test bot token if the test harness starts the bot process itself

Never commit or print these values.
