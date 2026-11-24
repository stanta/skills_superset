---
name: webapp-testing
description: "Run local browser UI checks with Playwright when a browser is part of the requested user journey."
license: Complete terms in LICENSE.txt
metadata:
  category: development
  source:
    repository: https://github.com/ComposioHQ/awesome-claude-skills
    path: webapp-testing
---

# Web Application Testing

Only use a browser when the requested behavior involves a rendered UI. For API-only or MCP-only checks, use [verification](../verification/SKILL.md) directly.

## Lightweight workflow

1. Inspect available tools, project scripts, server and existing test suite. Start a local server with the project's command or bundled `scripts/with_server.py` **if present**, checking `--help` first.
2. Navigate and await an app-specific readiness condition (element, URL, response or event). **Do not require `networkidle`**: polling, WebSockets and analytics may keep the network busy.
3. Inspect accessible roles/labels and rendered DOM, use stable selectors and execute the user interaction.
4. Assert visible behavior and relevant side effects. Capture logs, screenshots or Playwright traces for failures.
5. Close browser resources and report actual runs, failures and blocked areas.

Prefer locator auto-waiting and explicit state assertions; avoid arbitrary sleeps. Use direct scripts for small one-off checks and Page Object Models only when repeated flows warrant them. Never assume Python, a helper, a particular host or browser binary is installed. For maintained suites and CI see [playwright-expert](../playwright-expert/SKILL.md).
