---
name: telegram-mini-apps-specialist
description: Use when building, debugging, or reviewing Telegram Mini Apps that run on React/Vite and integrate with Telegram runtime APIs, TON Connect, and wallet-oriented user flows.
source_repo: https://github.com/Telegram-Mini-Apps/tma.js
source_validation: GitHub research confirmed 5+ stars/forks; observed public signals included ~1.1k stars and ~388 forks on 2026-03-13.
---

# telegram-mini-apps-specialist

## Purpose

This skill provides project-specific guidance for Telegram Mini App work across the repositories in this workspace, especially [`wallet-tma/package.json`](../../../wallet-tma/package.json:1), [`architecton-voting-app/package.json`](../../../architecton-voting-app/package.json:1), and the TMA/web deployment surface described in [`arc-web/docs/architecture-overview.md`](../../../arc-web/docs/architecture-overview.md:15).

## Use this skill when

- A task depends on Telegram launch parameters, Telegram-specific runtime APIs, or Mini App execution context.
- A React app must behave correctly both inside Telegram and in local browser development.
- A feature uses TON Connect or wallet-adjacent flow inside a Telegram Mini App shell.
- HTTPS local development, deep links, or bot-to-mini-app handoff needs to be stabilized.

## Do not use this skill when

- The task is generic React UI work with no Telegram runtime dependency. Use [`frontend-react-dev`](../frontend-react-dev/SKILL.md) instead.
- The task is backend-only API logic. Use [`fastapi-expert`](../fastapi-expert/SKILL.md) and [`python-dev`](../python-dev/SKILL.md) instead.

## Recommended workflow

1. **Classify runtime context**
   - Confirm whether the page runs inside Telegram, in a local mock shell, or as a standalone web fallback.
   - Review existing runtime assumptions in [`architecton-voting-app/src/mockEnv.ts`](../../../architecton-voting-app/src/mockEnv.ts:1) and the TMA dependency list in [`wallet-tma/package.json`](../../../wallet-tma/package.json:16).

2. **Stabilize Telegram bridge initialization**
   - Keep Telegram SDK initialization centralized.
   - Avoid scattering launch-parameter parsing or SDK bootstrap logic across many components.

3. **Separate TMA shell concerns from product logic**
   - Keep Telegram shell APIs, TON Connect wiring, and deep-link logic in adapters/hooks.
   - Keep feature and UI logic testable without Telegram globals.

4. **Protect development ergonomics**
   - Provide mock launch data and safe fallbacks for browser-only execution.
   - Require HTTPS when testing true Telegram embedding scenarios.

5. **Audit wallet and transaction UX**
   - Confirm wallet connect/disconnect, retry, and error states are explicit.
   - Avoid hidden transaction side effects during render or uncontrolled route transitions.

6. **Test the right layers**
   - Unit-test hooks and adapter logic with mocked Telegram APIs.
   - Keep real Telegram/manual smoke tests focused on critical launch and wallet flows.

## Project guidance

- For [`wallet-tma`](../../../wallet-tma/package.json:1), prefer this skill whenever work touches `@tma.js/sdk`, `@tma.js/sdk-react`, or `@tonconnect/ui-react`.
- For [`architecton-voting-app`](../../../architecton-voting-app/package.json:1), use this skill when the feature depends on Telegram environment bootstrapping, route integration, or TON Connect UI.
- For [`arc-web`](../../../arc-web/package.json:1), use this skill only when the change affects the Telegram Mini App flavor of the main product surface documented in [`arc-web/docs/architecture-overview.md`](../../../arc-web/docs/architecture-overview.md:15).

## Output expectations

When this skill is used, the output should include:

- runtime classification,
- Telegram/TON integration boundary,
- fallback strategy for non-Telegram execution,
- test plan for Telegram-specific behaviors,
- security or UX risks around wallet and transaction flows.
