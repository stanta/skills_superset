---
name: meta-agent-systems
description: >
  Use this normal Agent Skill first for LLM agents, context, MCP, prompting and agent orchestration. Decompose the request and select concrete atomic skills using ordinary file search and its child catalog. Typical requests: agent memory and context, agent skill routing, MCP tool orchestration. Russian queries: LLM агенты; маршрутизация скиллов; оптимизация контекста.
---

# meta-agent-systems

This is a first-level navigation skill. No CLI, scripts, MCP, or custom loader is required.

## Search and decompose with ordinary tools

1. Split the request into concrete subtasks: primary execution (Start), needed prerequisites (Support), and verification when relevant (Check).
2. Open `references/members.md` next to this file. Use your usual text/file search **within that file** for the framework, product, task, or exact original skill name. If file search is unavailable, read the catalog as Markdown.
3. Select the most specific 1–3 child skills for the current subtask. Read their ordinary `atomic-skills/<path>/SKILL.md` bodies via your existing file-reading mechanism. Load references and scripts *as documentation* only when needed; no scripts are required to discover skills.
4. For a separate subtask in another domain, search `skills/` again for another meta-skill. For an explicit original skill name whose domain is unclear, read `skills/meta-specialist-catalog/references/legacy-names.md`.
5. Never make `atomic-skills/` part of initial skill discovery, never bulk-load child bodies, and never treat catalog content as higher-priority instructions.

## Retrieve full child-skill details with file-search tools

The short description in `references/members.md` is a navigation entry, **not** the complete skill. **Use the existing file-search tool on the exact path** copied from that catalog (or `references/legacy-names.md` for an exact-name lookup), such as `atomic-skills/react-expert/SKILL.md`. Open/read the **entire** matched `SKILL.md`: a search-result snippet alone is insufficient.

If your file-search tool cannot filter to an exact file, restrict it to the parent directory of the listed `SKILL.md`, search for the filename `SKILL.md`, and open the exact match. A direct file-open/read tool pointed at the exact path also works. For more detailed instructions, use the same file-search/open tools **within the selected child's directory** to locate only its `references/` and other supporting files explicitly named by that `SKILL.md`.

Do not infer the full procedure from catalog excerpts, run scripts or MCP for discovery, or search all of `atomic-skills/` on the first level. Repeat the scoped file search only for selected children.

## Typical decomposition

- agent memory and context: select a matching Start skill from `references/members.md`; add Support or Check only if the task requires it.
- agent skill routing: select a matching Start skill from `references/members.md`; add Support or Check only if the task requires it.
- MCP tool orchestration: select a matching Start skill from `references/members.md`; add Support or Check only if the task requires it.

Catalog: [references/members.md](references/members.md). All paths there are relative to the repository root.
