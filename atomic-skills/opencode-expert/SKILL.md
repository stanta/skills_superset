---
name: opencode-expert
description: >-
  This skill should be used when configuring, operating, extending, or
  troubleshooting the OpenCode AI coding agent (sst/opencode) — including
  opencode.json / opencode.jsonc project and global configuration, AGENTS.md
  custom instructions, provider and model setup, agent definitions (primary and
  subagent), permission rules, MCP server integration, LSP diagnostics, TUI
  keybinds, custom commands, plugins, skill definitions (SKILL.md), session
  management, GitHub Actions integration, and terminal workflow best practices.
  Trigger phrases: opencode, opencode.json, opencode config, AGENTS.md,
  opencode agent, opencode MCP, opencode permission, opencode skill,
  opencode provider, opencode TUI, opencode plugin, opencode rules.
license: MIT
metadata:
  category: development
  source:
    repository: https://github.com/sst/opencode
    stars: 30000+
    related:
      - https://github.com/awesome-opencode/awesome-opencode
      - https://github.com/opencode-ai/opencode
      - https://github.com/bradAGI/awesome-cli-coding-agents
---

# OpenCode Expert

Comprehensive guide for configuring and operating the **OpenCode** AI coding
agent — the open-source, provider-agnostic, terminal-native coding assistant
(formerly known as `sst/opencode` / `anomalyco/opencode`).

Official docs: <https://opencode.ai/docs/>

---

## 1. Installation

```bash
# Recommended — Homebrew (macOS / Linux)
brew install anomalyco/tap/opencode

# npm / bun / pnpm / yarn
npm i -g opencode-ai@latest

# One-liner
curl -fsSL https://opencode.ai/install | bash

# Arch Linux
sudo pacman -S opencode

# Windows
scoop install opencode
choco install opencode

# Nix
nix run nixpkgs#opencode

# mise
mise use -g opencode
```

After installing, launch with `opencode` in any git repository.

---

## 2. Configuration — `opencode.json` / `opencode.jsonc`

Configuration is loaded in order of precedence (highest first):

| Scope       | Location                                     |
|------------|----------------------------------------------|
| **Project** | `<repo>/opencode.json` or `opencode.jsonc`   |
| **Global**  | `~/.config/opencode/opencode.json`           |

Use `$schema` for IDE autocompletion:

```jsonc
{
  "$schema": "https://opencode.ai/config.json"
}
```

### 2.1 Model & Provider

```jsonc
{
  "model": "anthropic/claude-sonnet-4-20250514",
  "provider": {
    "anthropic": { "disabled": false },
    "openai": {
      "models": { "gpt-4o": { "disabled": false } }
    },
    "openrouter": {
      "models": { "anthropic/claude-3.5-sonnet": {} }
    }
  }
}
```

Provider API keys are set via `/connect` command in the TUI or environment variables.
OpenCode supports **75+ LLM providers** via AI SDK and Models.dev. Local models
(Ollama, LM Studio) are supported.

### 2.2 Permissions

Three-tier permission system: `"allow"`, `"ask"`, `"deny"`.
Glob patterns match tool arguments. Agent-level overrides are supported.

```jsonc
{
  "permission": {
    "edit": { "*": "allow" },
    "read": { "*": "allow", "*.env": "ask" },
    "bash": {
      "*": "ask",
      "git *": "allow",
      "git commit *": "deny",
      "git push *": "deny",
      "npm *": "allow",
      "grep *": "allow"
    },
    "skill": "allow"
  }
}
```

**Best practice:** Start restrictive (`"ask"`) and selectively `"allow"` safe
commands. Always `"deny"` destructive git operations for subagents.

### 2.3 Agents

Two modes: `"primary"` (user-facing, Tab-switchable) and `"subagent"` (spawnable).

Built-in agents:
- **build** — Full-access development agent (default)
- **plan** — Read-only analysis and code exploration agent

```jsonc
{
  "agent": {
    "reviewer": {
      "description": "Code review specialist — read-only",
      "mode": "subagent",
      "model": "anthropic/claude-sonnet-4-20250514",
      "prompt": "You are a code reviewer. Focus on security, performance, and maintainability.",
      "tools": { "write": false, "edit": false, "bash": false }
    }
  }
}
```

Agent prompts can reference files: `"prompt": "{file:./prompts/build.txt}"`.

### 2.4 Custom Instructions — AGENTS.md & Rules

AGENTS.md is automatically loaded from the repo root. It acts as a project-
specific system prompt appended to every session.

Additional instruction files can be specified:

```jsonc
{
  "instructions": [
    "CONTRIBUTING.md",
    "docs/guidelines.md",
    ".cursor/rules/*.md",
    "https://raw.githubusercontent.com/my-org/shared-rules/main/style.md"
  ]
}
```

**Best practice:** Keep AGENTS.md under ~1000 tokens. Offload detailed guidelines
to separate files referenced via `instructions`.

### 2.5 MCP Servers

```jsonc
{
  "mcp": {
    "filesystem": {
      "type": "local",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path"]
    },
    "github": {
      "type": "local",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_..." }
    },
    "remote-api": {
      "type": "sse",
      "url": "https://api.example.com/mcp",
      "headers": { "Authorization": "Bearer token" }
    }
  }
}
```

MCP tools follow the same permission model as built-in tools.

### 2.6 LSP Integration

```jsonc
{
  "lsp": {
    "typescript-language-server": {
      "command": "typescript-language-server",
      "args": ["--stdio"]
    }
  }
}
```

Currently only **diagnostics** are exposed to the AI assistant from LSP.

### 2.7 Custom Commands

```jsonc
{
  "command": {
    "review": {
      "description": "Review staged changes",
      "prompt": "Review the staged changes and provide feedback"
    },
    "test": {
      "description": "Run and fix tests",
      "prompt": "Run the test suite. If any tests fail, fix them."
    }
  }
}
```

Commands are invoked via `/review`, `/test` in the TUI.
Custom command files (`.md`) can also be placed in `.opencode/commands/`,
`~/.config/opencode/commands/`, or `~/.agents/commands/`.

### 2.8 Plugins

```jsonc
{
  "plugin": [
    "@opencode/plugin-git",
    "./local-plugin.ts"
  ]
}
```

Notable community plugins:
- **agent-orchestrator** — Parallel agent spawning
- **opencode-agent-memory** — Persistent cross-session memory
- **opencode-agent-skills** — Skill loading plugin
- **opencode-beads** — Message bead UI
- **opencode-handoff** — Agent-to-agent handoff

### 2.9 TUI Keybinds

Configured in `~/.config/opencode/tui.json`:

```jsonc
{
  "$schema": "https://opencode.ai/tui.json",
  "keybinds": {
    "leader": "ctrl+x",
    "session_new": "<leader>n",
    "session_list": "<leader>l",
    "session_compact": "<leader>c",
    "agent_cycle": "tab",
    "model_list": "<leader>m",
    "command_list": "ctrl+p",
    "editor_open": "<leader>e",
    "sidebar_toggle": "<leader>b"
  }
}
```

---

## 3. Skills System (SKILL.md)

Skills allow reusable domain knowledge. Discovery paths:

| Scope     | Paths searched                                          |
|----------|---------------------------------------------------------|
| Project   | `.opencode/skills/*/SKILL.md`                           |
| Project   | `.claude/skills/*/SKILL.md`, `.agents/skills/*/SKILL.md`|
| Global    | `~/.config/opencode/skills/*/SKILL.md`                  |
| Global    | `~/.claude/skills/*/SKILL.md`, `~/.agents/skills/*/SKILL.md` |

Skill YAML frontmatter:

```markdown
---
name: git-release
description: Create consistent releases and changelogs
license: MIT
compatibility: opencode
metadata:
  audience: maintainers
---

## What I do
- Draft release notes from merged PRs
- Propose a version bump

## When to use me
Use when preparing a tagged release.
```

Enable the skill tool in permissions:

```jsonc
{ "permission": { "skill": "allow" } }
```

---

## 4. GitHub Integration

OpenCode can run as a GitHub Actions agent. Mention `/opencode` or `/oc` in
issue/PR comments to trigger tasks on the Actions runner.

```yaml
# .github/workflows/opencode.yml
name: OpenCode
on:
  issue_comment:
    types: [created]
jobs:
  opencode:
    if: contains(github.event.comment.body, '/opencode')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: opencode-ai/action@v1
        with:
          anthropic-api-key: ${{ secrets.ANTHROPIC_API_KEY }}
```

---

## 5. Session Management

| Action             | Keybind / Command            |
|-------------------|------------------------------|
| New session        | `<leader>n`                  |
| List sessions      | `<leader>l`                  |
| Compact / summarize| `<leader>c`                  |
| Fork session       | `/fork`                      |
| Share session       | `/share`                     |
| Export session      | `<leader>x`                  |
| Undo last change   | `<leader>u`                  |
| Redo               | `<leader>r`                  |

Sessions auto-persist. Use compaction (`<leader>c`) when context window grows
large to summarize earlier messages.

---

## 6. Best Practices

### 6.1 Project Setup Checklist

1. Create `opencode.json` at repo root with `$schema`.
2. Write `AGENTS.md` with project-specific rules (tech stack, conventions, test commands).
3. Configure permissions — whitelist safe bash commands explicitly.
4. Add relevant MCP servers (context7 for docs, filesystem for assets).
5. Define custom commands for repetitive tasks (`/test`, `/review`, `/deploy`).
6. Pin the model to a specific provider/model for deterministic behavior.

### 6.2 AGENTS.md Writing Tips

- State the tech stack, framework versions, and package manager.
- List preferred patterns (e.g., "Use async/await, not callbacks").
- Reference key files: "The main entry point is `src/main.py`".
- Specify test runners: "Run tests with `pytest -xvs`".
- State forbidden operations: "Never modify `migrations/` directly".
- Keep it concise — long AGENTS.md wastes context.

### 6.3 Effective Agent Workflows

- **Tab-switch** between `build` and `plan` agents: plan first, then build.
- Use **subagents** for specialized tasks (security review, docs generation).
- Use `/compact` (`<leader>c`) when sessions grow long.
- Use **custom commands** to standardize team workflows.
- Use **file references** in prompts: `{file:./prompts/review-checklist.md}`.

### 6.4 Permission Hardening

- Default to `"ask"` for bash and edit.
- Explicitly `"allow"` known-safe commands: `git status`, `git diff`, `grep`, `find`.
- `"deny"` destructive operations: `git push`, `rm -rf`, `docker rm`.
- Override per-agent: give `build` more access than `plan`.

### 6.5 MCP Server Selection

| Use Case                | Recommended MCP Server                        |
|------------------------|-----------------------------------------------|
| Library documentation  | `@upstash/context7-mcp`                       |
| File system access     | `@modelcontextprotocol/server-filesystem`     |
| GitHub integration     | `@modelcontextprotocol/server-github`         |
| Code search (Grep)     | `vercel/mcp-grep`                             |
| Database queries       | `@modelcontextprotocol/server-postgres`       |
| Web search             | `@modelcontextprotocol/server-brave-search`   |

### 6.6 Parallel Development

Use tools like **agent-orchestrator** plugin or **tmux + git worktrees** to
run multiple OpenCode instances on separate branches simultaneously.

### 6.7 Cost & Token Management

- Use `plan` agent (cheaper model) for exploration, `build` for implementation.
- Use session compaction to reduce accumulated context.
- Set `temperature: 0.3` for deterministic review agents.
- Monitor cost per session in the TUI status bar.

---

## 7. Troubleshooting

| Issue                            | Solution                                        |
|---------------------------------|------------------------------------------------|
| Provider not found              | Run `/connect` and authenticate                 |
| MCP server fails to start       | Check `command` path; run manually to debug     |
| Permissions too restrictive      | Add glob patterns to `permission.bash`          |
| Context too large                | Use `<leader>c` to compact session              |
| Agent ignoring rules             | Ensure AGENTS.md is in repo root, not nested    |
| Copilot auth fails               | Authenticate via GitHub CLI first               |
| Slow response                    | Switch to a faster model or local inference     |

---

## 8. Reference Resources

- **Official docs**: <https://opencode.ai/docs/>
- **GitHub repo**: <https://github.com/sst/opencode> (30K+ ⭐)
- **Awesome OpenCode**: <https://github.com/awesome-opencode/awesome-opencode> (curated plugins, themes, agents)
- **Awesome CLI Coding Agents**: <https://github.com/bradAGI/awesome-cli-coding-agents>
- **AGENTS.md spec**: <https://agents.md/>
- **OpenCode SDK**: `@opencode-ai/sdk` — programmatic access to sessions, messages, tools
- **Reddit community**: <https://reddit.com/r/opencodeCLI>
