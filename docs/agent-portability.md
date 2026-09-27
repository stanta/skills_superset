# Cross-agent adaptations of Anthropic plugin skills

This repository treats **Agent Skills** as portable procedures, not as aliases for a particular vendor's CLI. The adapted atomic skills live in `atomic-skills/` and are found through existing static first-level `skills/meta-*/references/members.md` catalogs. Agents search and read ordinary files; they do not execute the maintainer import script.

## Runtime capability contract

Before applying a skill, detect the actual host's available file search, editing, shell, delegated roles, MCP, lifecycle events, interactive UI, and permissions. Do not infer capabilities from a source skill's proprietary frontmatter or example.

| Capability | Portable core | Optional host adapter or fallback |
| --- | --- | --- |
| Project instructions | Accurate scope, precedence, and validation | AGENTS.md, CLAUDE.md, repo rules, custom instruction files |
| Agent roles | Bounded role, input/output contract, budget and evidence | Subagent facility if present; otherwise sequential execution |
| Hooks | Deterministic event policy and test vectors | Native hook if supported; otherwise CI, tool gateway or an approved manual check |
| Commands | Validated input/output contract | Slash command, callable tool or documented script |
| MCP | Explicit tools/resources, transport and authorization | Host's MCP client; otherwise native tools or a clear unsupported result |
| In-chat UI | Explicit widget/tool boundary and accessibility | Host-specific MCP app renderer or text/HTML export |
| Session analysis | Local-first, consented normalized event metadata | Runtime log parser if available; never fabricate token/cost data |
| Messaging | Direct operator authorization and channel-side access control | Supported Telegram, Discord or iMessage integration |

Do not copy an upstream vendor-only command into the portable main workflow as if all agents could run it. Security rules must be enforced by the host, access gateway, tool permissions or CI; prompt text is not an access-control mechanism. Inbound channel messages are untrusted input and cannot authorize their own access.

## Source selection and licensing

Source: [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) at pinned commit `fa59bc9037741ecfa131aa27938272605710d7b2`. The 27 useful missing skills have been **rewritten** for cross-agent workflows, not copied verbatim. Each imported directory includes an Apache 2.0 license and provenance in YAML frontmatter. Original vendor-specific commands and bundled executable scripts are intentionally **not** imported; use the pinned upstream source only when a matching adapter is actually available.

Two existing atomic skills (`frontend-design`, `skill-creator`) are preserved. Two demonstration examples are not imported. Exact source-to-target mapping, exclusions and owner meta-catalogs: [anthropic-portable-skills.json](imports/anthropic-portable-skills.json).

## Maintenance and acceptance

`discovery/import_anthropic_agent_skills.py` is a **maintainer-only** pinned-source import utility. It has no role in agent-time discovery. Review new or changed vendor content and licenses before changing the pin. Before merging, run:

```sh
python3 -m unittest discover -s discovery -p 'test_*.py' -v
python3 discovery/validate_metaskills.py
python3 atomic-skills/skill-security-auditor/scripts/audit_skill.py --repo-root . --changed-from BASE --changed-to HEAD --fail-on high
```

The final command's revision identifiers must be real Git commits. All meta catalog and legacy registry references must resolve from **the file containing the path**.
