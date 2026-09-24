---
name: meta-genomics-omics
description: >
  Route tasks about genomics, genetics, transcriptomics, NGS, variants and biological datasets. Use as the first-level meta-skill to decompose a request and select concrete atomic skills on demand. Typical requests: sequence analysis; variant interpretation; gene expression; biological cohorts.
---

# meta-genomics-omics

**Scope:** genomics, genetics, transcriptomics, NGS, variants and biological datasets. This skill routes; it does not replace concrete skills.

## Route and decompose

1. Split the request into the smallest independently executable subtasks; identify Start, optional Support and Check.
2. For each subtask, select up to three children **within this meta-skill** using `python discovery/metaskill_cli.py resolve --meta meta-genomics-omics --query "<subtask>" --top-k 3` (or MCP `resolve_skills`). Without CLI/MCP, read `references/members.md` and pick the matching names/descriptions.
3. Read each selected `atomic-skills/<slug>/SKILL.md` before execution. Load optional atomic references or scripts only when required.
4. If no child is suitable, search another first-level meta-skill. Do not list/search the full atomic corpus during first-level discovery. A routing result does not grant permission to execute tools or scripts.

## Example intents

- sequence analysis: identify the concrete child for this subtask, then any prerequisite or verification child.
- variant interpretation: identify the concrete child for this subtask, then any prerequisite or verification child.
- gene expression: identify the concrete child for this subtask, then any prerequisite or verification child.
- biological cohorts: identify the concrete child for this subtask, then any prerequisite or verification child.

The generated `references/members.md` lists all children assigned to this domain, including any intentionally overlapping membership.
