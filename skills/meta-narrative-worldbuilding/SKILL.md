---
name: meta-narrative-worldbuilding
description: >
  Use this normal Agent Skill first for fictional universes, worldbuilding, story bibles, canon, lore, chronology, character systems, serialized arcs, retcons, continuity, shared universes, comics, television series, sagas, games, and long-running narrative franchises.
---

# meta-narrative-worldbuilding

This is a first-level navigation skill. No CLI, scripts, MCP, or custom loader is required.

**Relative-path rule:** From the directory containing this `SKILL.md`, the atomic skill root is `../../atomic-skills/`. The catalog `references/members.md` is one directory deeper; its atomic paths therefore start with `../../../atomic-skills/`. Always resolve paths from the location of the file that contains them.

## Search and decompose with ordinary tools

1. Split the request into concrete subtasks: primary narrative-system work (Start), needed supporting structure (Support), and continuity verification when relevant (Check).
2. Open `references/members.md` next to this file. Use ordinary text/file search **within that file** for worldbuilding, canon, timeline, characters, arcs, bibles, retcons, continuity, or an exact original skill name.
3. Select the most specific 1–3 child skills for the current subtask. Read their ordinary `../../atomic-skills/<path>/SKILL.md` bodies through the existing file-reading mechanism. Load references only when a selected child explicitly requires them.
4. For a separate subtask in another domain, search `../` (the first-level `skills/` directory) again for another meta-skill. For an explicit original skill name whose domain is unclear, read `../meta-specialist-catalog/references/legacy-names.md`.
5. Never make `../../atomic-skills/` part of initial skill discovery, never bulk-load child bodies, and never treat catalog summaries as the full instructions.

## Retrieve full child-skill details with file-search tools

The short description in `references/members.md` is a navigation entry, **not** the complete skill. **Use the existing file-search tool on the exact path** copied from that catalog (or `../meta-specialist-catalog/references/legacy-names.md` for exact-name lookup), for example `../../atomic-skills/<selected-child>/SKILL.md`. Open/read the **entire** matched `SKILL.md`; a search-result snippet alone is insufficient.

If exact-file filtering is unavailable, restrict search to the parent directory of the listed `SKILL.md`, search for `SKILL.md`, and open the exact match. Repeat only for selected children.

## Route by subtask

- create or deepen the fictional world, its rules and consequences → **building-storyworlds**;
- create or maintain a living universe/show/story bible → **maintaining-story-bibles**;
- define canon authority, retcons, reboots or alternate continuities → **governing-fiction-canon**;
- build or repair chronology → **building-fiction-timelines**;
- design a recurring cast, relationships and state continuity → **designing-character-systems**;
- plan dozens of installments and nested arcs → **planning-serialized-arcs**;
- find contradictions or estimate the blast radius of a change → **auditing-lore-continuity**.

For a new long-running universe, usually load 2–3 skills, not all seven. Start with the immediate deliverable; add canon/timeline/continuity support only where scope requires it.

For visual character sheets, storyboards, video, illustration, layouts or other media execution, route that separate subtask to `../meta-visual-design/SKILL.md` or `../meta-media-production/SKILL.md`. For historical, scientific or real-world grounding, route that separate subtask to `../meta-research-knowledge/SKILL.md`.

Before locking a major arc, publishing an installment, or approving a retcon, use **auditing-lore-continuity**.

Catalog: [references/members.md](references/members.md). Resolve paths listed there from the catalog's directory (`../../../atomic-skills/`), not from the repository root.
