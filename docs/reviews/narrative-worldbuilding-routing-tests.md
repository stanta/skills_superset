# Narrative worldbuilding routing tests

Date: 2026-10-02
Branch: `feature/narrative-worldbuilding-skills`

## Baseline failure

Before this change, first-level discovery had no dedicated narrative-worldbuilding meta-skill. `meta-media-production` exposed video/audio/writing production skills but no skills for canon, fictional chronology, long-running character state, retcon governance, serialized arc planning, or lore contradiction audits. A request such as “design a shared universe for 60 comic issues and keep canon consistent” therefore had no specific first-level route.

## Post-change discovery scenarios

| Request | Expected first-level route | Atomic skills |
|---|---|---|
| “Create a fantasy world whose politics and economy follow from one magic rule.” | meta-narrative-worldbuilding | building-storyworlds |
| “Make a living show bible for a five-season drama.” | meta-narrative-worldbuilding | maintaining-story-bibles; designing-character-systems as needed |
| “Which version of this origin is canon after the reboot?” | meta-narrative-worldbuilding | governing-fiction-canon |
| “Build the chronology and verify ages and travel time.” | meta-narrative-worldbuilding | building-fiction-timelines; auditing-lore-continuity |
| “Design an ensemble whose relationships can sustain 40 episodes.” | meta-narrative-worldbuilding | designing-character-systems; planning-serialized-arcs |
| “Plan 60 comic issues without locking every issue in advance.” | meta-narrative-worldbuilding | planning-serialized-arcs; maintaining-story-bibles |
| “This retcon changes a character’s parentage; what else breaks?” | meta-narrative-worldbuilding | auditing-lore-continuity; governing-fiction-canon; building-fiction-timelines |
| “Find contradictions across novels, comics and a game.” | meta-narrative-worldbuilding | auditing-lore-continuity; governing-fiction-canon |
| “Create an image reference sheet for this already-defined character.” | meta-visual-design | not a narrative-worldbuilding task unless character logic is also being redesigned |
| “Storyboard issue #1 of this already-defined universe.” | meta-media-production / meta-visual-design | narrative skills only if the storyboard introduces canon changes |
| “Build a comic universe, define canon, then storyboard the pilot.” | decompose across metas | meta-narrative-worldbuilding first; media/visual production second |
| “Research medieval trade to ground my fictional economy.” | decompose across metas | meta-research-knowledge for evidence; building-storyworlds for fictional consequences |

## Behavioral pressure tests

### 1. Worldbuilder's disease
Prompt: “Invent 50 countries, 30 gods and 20 magic schools before we decide the story.”

Expected behavior: `building-storyworlds` should redirect toward premise, constraints, consequences, conflict surfaces and depth before breadth rather than rewarding lore volume.

### 2. Exception creep
Prompt: “The hero needs a new power in issue 18 to escape; add a one-off exception.”

Expected behavior: `building-storyworlds` and `governing-fiction-canon` should prefer existing capabilities/constraints or an explicit narrow exception with provenance and downstream impact.

### 3. Partial reboot
Prompt: “Reset only the protagonist’s history but keep all team stories unchanged.”

Expected behavior: `governing-fiction-canon` must flag dependency risk and require survival/reset rules plus impact analysis.

### 4. False precision
Prompt: “We only know the battle happened sometime that winter; assign an exact date.”

Expected behavior: `building-fiction-timelines` should preserve a range or relative offset.

### 5. Silent contradiction repair
Prompt: “Just edit the bible so the old version disappears.”

Expected behavior: `auditing-lore-continuity` and `governing-fiction-canon` should preserve the old fact as deprecated/superseded and record the change.

### 6. Endless serial reset
Prompt: “At the end of every six-issue arc, restore everyone to the starting status quo.”

Expected behavior: `planning-serialized-arcs` should preserve persistent consequences and use the new state to generate the next conflict.

## Acceptance criteria

- Dedicated first-level meta-skill is discoverable by worldbuilding/canon/lore/chronology/character-system/serialized-arc/continuity terms.
- Exact atomic skill names are in the specialist legacy-name registry.
- Media-production explicitly routes fictional-universe system work to the narrative meta-skill.
- All child paths listed in `members.md` exist.
- Skill descriptions are trigger-focused and begin with “Use when”.
- Atomic skill bodies remain under the repository's recommended ~500-word target.
- Research provenance is stored under `docs/research/`.
