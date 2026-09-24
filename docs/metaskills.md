# Meta-skills: plain-search-compatible two-level discovery

## Agent runtime (no scripts and no MCP required)

Only `skills/meta-*/SKILL.md` are visible to first-level skill discovery.
Each is a standard Agent Skill with YAML `name` and `description`.
Read the chosen meta `SKILL.md`, inspect its local `references/members.md`
using ordinary file search, then open the selected atomic skill's full
`SKILL.md`. Repeat for separate subtasks; load 1–3 atomic skills at a time.
A search result excerpt or the one-line catalog entry is not sufficient.

**Resolve relative paths from the directory containing the file that
mentions them**, not from the repository root, except for explicitly
repository-root-relative paths shown in the root README.

| File that contains the path | Correct relative atomic root |
| --- | --- |
| `README.md` or `README.legacy.md` (repository root) | `atomic-skills/` |
| `docs/metaskills.md` (this file) | `../atomic-skills/` |
| `skills/meta-*/SKILL.md` | `../../atomic-skills/` |
| `skills/meta-*/references/members.md` | `../../../atomic-skills/` |
| `skills/meta-specialist-catalog/references/legacy-names.md` | `../../../atomic-skills/` |

For example, a meta instruction at
`../skills/meta-agent-systems/SKILL.md` uses
`../../atomic-skills/agent-evals-lab/SKILL.md`, while a child-catalog
entry inside `../skills/meta-agent-systems/references/members.md` uses
`../../../atomic-skills/agent-evals-lab/SKILL.md`. Both resolve to the
same existing atomic file. A known atomic file can also be opened from
this documentation directory as
`../atomic-skills/agent-evals-lab/SKILL.md`.

For an explicitly named old skill, search the static registry at
`../skills/meta-specialist-catalog/references/legacy-names.md`.
Its entries, like the ordinary child catalogs, are relative to the
registry's own `references/` directory and begin with
`../../../atomic-skills/`.

## Visibility and limits

All original atomic skills and their relative resources are preserved
under the repository-root `atomic-skills/` directory. First-level
discovery must enumerate only repository-root `skills/`. A global
repository `**/SKILL.md` search will also find the atomic files;
the directory convention is not an access-control mechanism.
No agent-time CLI, Python, MCP server or embedding service is needed.

Moving old atomic directories changes hard-coded repository-root paths
from `skills/<original-path>/...` to
`atomic-skills/<original-path>/...`. Existing original frontmatter
names, original skill bodies and relative bundled resources are intact.

## Taxonomy and maintenance

Domain memberships and name registry are static Markdown. Some atomic
skills appear in two meta domains. The unmatched set remains in
`meta-specialist-catalog`. After any catalog change, the CI-only
validator resolves **every** referenced child file from its containing
catalog's directory and verifies the first-level visibility boundary.
This is a filesystem-based semantic taxonomy, not a claim of measured
token savings or perfect routing quality.
