# Meta-skills: plain-search-compatible two-level discovery

## Agent runtime (no scripts and no MCP required)

The ordinary first-level skill scanner sees `skills/meta-*/SKILL.md` only.
Every meta-skill is a standard `SKILL.md` with YAML `name`, `description`
and Markdown instructions. The agent chooses a meta by the normal skill
search, reads its `references/members.md` using normal text search or file
reading, then reads only selected `atomic-skills/<original-path>/SKILL.md`.
Repeat for other subtasks; 1–3 atomic skills per subtask is the default.
Neither CLI nor Python nor a resident service is required by the agent.

For an explicitly named old skill, first read
`skills/meta-specialist-catalog/references/legacy-names.md` and search
for the original exact ID or frontmatter name. This file maps all original
skills to meta group(s) and exact target paths; direct reading of a known
`atomic-skills/<original-path>/SKILL.md` also works without a script.

## Visibility and limits

The entire original `skills/` subtree is preserved byte-for-byte under
`atomic-skills/`. Initial discovery only scans `skills/`, containing
26 meta-skills. A repository-global `**/SKILL.md` file search still sees
atomic files; configure a client to use `skills/` as its *skill discovery
root* and allow ordinary read access to `atomic-skills/` for second-level
loading. A generic code-search UI is not an access-control boundary.

File-path compatibility requires migrating hardcoded
`skills/<original-path>/...` to `atomic-skills/<original-path>/...`.
Preserving old paths while hiding them from a scanner of `skills/` is
not possible. Original frontmatter names, ordinary SKILL.md bodies,
relative bundled scripts, references and assets are unchanged.

## Taxonomy and maintenance

Domains are curated topic groups with matching over existing skill names
and descriptions, not neural embeddings. Some skills belong to two meta
domains. The unmatched set is under `meta-specialist-catalog`. Catalogs
and exact-name registry are static Markdown; they were generated at
authoring time. A maintainer may regenerate them offline after additions.
An optional GitHub Actions validation can check link targets, atomic
coverage and the meta-only first-level root. No agent-time scripts or
new discovery API are necessary. This branch does not claim measured
routing accuracy, token savings, or perfect topic classification.
