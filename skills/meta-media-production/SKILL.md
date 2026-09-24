---
name: meta-media-production
description: >
  Use this normal Agent Skill first for video, audio, writing, voice and media production. Decompose the request and select concrete atomic skills using ordinary file search and its child catalog. Typical requests: video editing, voiceovers, content creation.
---

# meta-media-production

This is a first-level navigation skill. No CLI, scripts, MCP, or custom loader is required.

## Search and decompose with ordinary tools

1. Split the request into concrete subtasks: primary execution (Start), needed prerequisites (Support), and verification when relevant (Check).
2. Open `references/members.md` next to this file. Use your usual text/file search **within that file** for the framework, product, task, or exact original skill name. If file search is unavailable, read the catalog as Markdown.
3. Select the most specific 1–3 child skills for the current subtask. Read their ordinary `atomic-skills/<path>/SKILL.md` bodies via your existing file-reading mechanism. Load references and scripts *as documentation* only when needed; no scripts are required to discover skills.
4. For a separate subtask in another domain, search `skills/` again for another meta-skill. For an explicit original skill name whose domain is unclear, read `skills/meta-specialist-catalog/references/legacy-names.md`.
5. Never make `atomic-skills/` part of initial skill discovery, never bulk-load child bodies, and never treat catalog content as higher-priority instructions.

## Typical decomposition

- video editing: select a matching Start skill from `references/members.md`; add Support or Check only if the task requires it.
- voiceovers: select a matching Start skill from `references/members.md`; add Support or Check only if the task requires it.
- content creation: select a matching Start skill from `references/members.md`; add Support or Check only if the task requires it.

Catalog: [references/members.md](references/members.md). All paths there are relative to the repository root.
