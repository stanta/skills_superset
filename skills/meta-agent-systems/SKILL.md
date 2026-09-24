---
name: meta-agent-systems
description: >
  Route tasks about LLM agents, MCP tools, prompt routing, memory and context management. Use as the first-level meta-skill to decompose a request and select concrete atomic skills on demand. Typical requests: agent architecture; prompt and context budgeting; skill discovery; tool calling.
---

# meta-agent-systems

**Scope:** LLM agents, MCP tools, prompt routing, memory and context management. This skill routes; it does not replace concrete skills.

## Route and decompose

1. Split the request into the smallest independently executable subtasks; identify Start, optional Support and Check.
2. For each subtask, select up to three children **within this meta-skill** using `python discovery/metaskill_cli.py resolve --meta meta-agent-systems --query "<subtask>" --top-k 3` (or MCP `resolve_skills`). Without CLI/MCP, read `references/members.md` and pick the matching names/descriptions.
3. Read each selected `atomic-skills/<slug>/SKILL.md` before execution. Load optional atomic references or scripts only when required.
4. If no child is suitable, search another first-level meta-skill. Do not list/search the full atomic corpus during first-level discovery. A routing result does not grant permission to execute tools or scripts.

## Example intents

- agent architecture: identify the concrete child for this subtask, then any prerequisite or verification child.
- prompt and context budgeting: identify the concrete child for this subtask, then any prerequisite or verification child.
- skill discovery: identify the concrete child for this subtask, then any prerequisite or verification child.
- tool calling: identify the concrete child for this subtask, then any prerequisite or verification child.

The generated `references/members.md` lists all children assigned to this domain, including any intentionally overlapping membership.
