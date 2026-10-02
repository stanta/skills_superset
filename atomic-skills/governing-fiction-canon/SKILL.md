---
name: governing-fiction-canon
description: Use when a fictional universe has multiple stories, creators, media, timelines, revisions, retcons, alternate continuities, disputed facts, or a need to decide what is authoritative and how canon changes are approved.
metadata:
  category: narrative-worldbuilding
  last_verified: "2026-10-02"
---

# Governing Fiction Canon

## Core principle

Canon is a **versioned authority system**, not a pile of notes. Every fact needs status, provenance, scope, and a change history.

## Canon states

Use explicit states rather than a binary canon/non-canon flag:

- **canonical** — currently authoritative;
- **provisional** — approved internally but not yet published;
- **in-world claim** — true only as a character/source assertion;
- **disputed** — published sources conflict and no ruling exists;
- **deprecated** — superseded but retained for history;
- **alternate** — valid in another branch/universe;
- **non-canon** — intentionally outside continuity.

## Minimum record

For each canon fact store:

- stable fact ID;
- subject / predicate / object or normalized statement;
- status and branch;
- source and first appearance;
- latest authoritative confirmation;
- effective story date and publication date;
- confidence / ambiguity;
- owner or approving editor;
- dependencies and affected entities;
- change log.

## Precedence policy

Write the policy before contradictions occur. A robust default is:

1. explicit current canon decision;
2. released primary narrative;
3. released secondary narrative;
4. official reference material;
5. internal notes.

Do not let an unpublished note silently override released material. If authority chooses to override published canon, record it as a retcon.

## Retcon classes

Classify every change:

- clarification;
- additive insertion;
- reinterpretation;
- soft override;
- hard rewrite;
- branch / alternate continuity;
- reboot.

Prefer the smallest change that repairs the inconsistency while preserving reader-visible promises.

## Change gate

Before approving a canon change:

1. state what changes;
2. list directly contradicted facts;
3. trace dependent characters, events, relationships, rules, and future plans;
4. estimate reader-visible blast radius;
5. choose migration or bridge scenes;
6. update timeline and character states;
7. record the decision and rationale.

## Anti-pattern: partial reboot

Resetting some histories while keeping interconnected histories unchanged creates contradiction cascades. If a reboot is necessary, define precisely what survives, what resets, and how cross-character dependencies are re-derived.

Use **auditing-lore-continuity** for impact analysis and **building-fiction-timelines** for temporal changes.
