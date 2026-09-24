# Meta-skills branch: two-level progressive discovery

The `skills/` root contains only `meta-*/SKILL.md` entries. The entire original
skills tree is preserved as `atomic-skills/<original-slug>/`, including scripts,
references, assets and licenses. This physical separation makes ordinary
`skills/*/SKILL.md` discovery see **only meta-skills**. A repository-wide
`**/SKILL.md` search is unrestricted and can still see atomic skills; configure
agents to use only `skills/` as their *discovery root*.

## Agent protocol

1. Call CLI `search "<task>"` (or MCP `search_skills`) and read one relevant
   `skills/meta-*/SKILL.md`. This call never returns atomic skill names or paths.
2. Decompose the task into concrete subtasks. Call
   `resolve --meta meta-<domain> --query "<subtask>" --top-k 3` (or MCP
   `resolve_skills`), which searches **only the selected meta's children**.
   Without CLI/MCP, inspect that meta's generated `references/members.md`.
3. Read at most the required `atomic-skills/<slug>/SKILL.md` files and their
   optional references on demand. The meta is a router, not a replacement.
4. When the user explicitly names an old atomic skill, `lookup <original-slug>`
   (MCP `lookup_skill`) resolves it without an unscoped atomic search.

## Compatibility

The meta-skills use normal Agent Skills YAML frontmatter (`name`,
`description`) and Markdown bodies, so simple filesystem skill scanners can
discover them without an MCP extension. All atomic SKILL.md bodies and their
relative resources are unchanged. Existing direct **name-based** calls can use
`lookup`. **Old absolute/relative file paths change** from
`skills/<slug>/...` to `atomic-skills/<slug>/...`—there is no way to preserve
the old physical paths while also hiding them from a filesystem scanner that
enumerates that directory.

## Deterministic catalog

The first implementation uses curated semantic domain profiles, name and
description features, up to two overlapping memberships and manual overrides,
not neural embeddings. Unmatched skills are assigned to
`meta-specialist-catalog`. Generated `skills-index.jsonl` is **meta-only**;
`discovery/atomic-index.jsonl` is an internal index accessible only through
scoped resolution or explicit legacy lookup. The generation step creates
`skills/meta-*/references/members.md`. An index rebuild can run without a
resident service, API keys or a paid model.

## Commands

```bash
python discovery/metaskill_cli.py index
python discovery/metaskill_cli.py search "React TypeScript build" --top-k 3
python discovery/metaskill_cli.py resolve --meta meta-frontend-web --query "React build"
python discovery/metaskill_cli.py lookup agent-evals-lab
python discovery/metaskill_cli.py eval
python -m unittest discover -s discovery -p 'test_*.py' -v
```

Optional MCP stdio: `pip install 'mcp[cli]'` then
`python discovery/mcp_server.py`. First-level discovery works without MCP
when a client scans `skills/*/SKILL.md`.

Routing evaluation is distinct from end-to-end task success or token savings;
the bundled smoke set is not a representative production benchmark.
