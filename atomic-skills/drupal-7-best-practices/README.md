# Drupal 7 Best Practices — Skill Package

A reusable AI skill capturing the best practices for **developing and maintaining Drupal 7 code**. Created for the `taktaev.com` project (a legacy Drupal 7 site), but applicable to any Drupal 7 codebase.

## Why this skill exists

`taktaev.com` is a **Drupal 7** site (core **7.81**, from the March 2022 database dump in [`DB/`](../../DB/)). A review of the existing skill library found:

- **No Drupal skill at all** in `/home/stan/.kilocode/skills/`.
- The closest existing materials were `engineering-drupal-performance.md` and `engineering-drupal-shopping-cart.md` under `/512-2/mcps/agency-agents/` — but both target **Drupal 10/11** (BigPipe, Dynamic Page Cache, Twig, YAML config, Commerce 2.x, Symfony services).
- The generic `engineering-cms-developer.md` role uses **Drupal 8+** conventions (`.info.yml`, `src/`, Twig, `#[Block]` attributes) that are actively harmful if applied to Drupal 7.

Drupal 7 is a fundamentally different platform: procedural PHP + hooks, `.info`/`.module`/`.install` files, PHPTemplate `.tpl.php` templates, the Database API with `{table}` placeholders, and configuration-in-code via Features + Strongarm. This skill closes that gap.

## Project context discovered (taktaev.com DB dump)

From `DB/a145188_taktaevr_2022-03-12_15_09.sql` (MySQL 5.7, ~32 MB), parsed via `scripts/inventory_site_from_dump.py`:

- **Drupal 7 core 7.81** (from the `system` module `schema_version` 7081). It is behind the final release 7.102 and past **EOL (5 Jan 2025)** — see [`references/deployment-maintenance.md`](references/deployment-maintenance.md#drupal-7-end-of-life--migration).
- **Enabled contrib modules (18)**: `cck`, `content_migrate`, `ckeditor`, `ctools`, `entity`, `ljxp` (likely custom), `module_filter`, `module_missing_message_fixer`, `pathauto`, `synonyms` (+ `synonyms_provider_field/property`, `synonyms_search`), `taxonomy_manager`, `token`, `views` + `views_ui`, `webform`.
- **Enabled themes**: `bartik` (core), `garland` (core), `responsive_blog` (contrib).
- **Legacy CCK tables present**: `cck_field_settings`, `content_node_field`, `content_node_field_instance` (leftover from a Drupal 6 → 7 migration — a maintenance hazard).
- **Orphaned tables from uninstalled modules**: `advagg`/`cache_advagg`, `captcha_*`, `date_format_*`, `comment`, `forum`/`taxonomy_forums`, `upload`, and Facebook tables (`fb_app`, `fb_user_app`). These modules are **not** in the enabled (nor `system`) list — their tables are dead weight to be dropped during migration.

**Maintenance implications for this site specifically:**
1. It is several releases behind the final Drupal 7 (7.102) and is now past **EOL** — engage D7ES immediately and/or migrate.
2. `cck`/`content_migrate` are Drupal-6-era helpers — they signal an incomplete D6→D7 migration and should be phased out.
3. The 18 contrib modules above must be re-acquired (from git/drupal.org) to rebuild the codebase — the DB dump does not contain PHP code. Run `scripts/inventory_site_from_dump.py` to produce the full manifest.

## Package layout

```
drupal-7-best-practices/
├── SKILL.md                         # Main skill (lean, always loaded on trigger)
├── README.md                        # This file (usage + project context)
├── scripts/
│   └── inventory_site_from_dump.py  # Extract version + module/theme manifest from a SQL dump
└── references/
    ├── security.md                  # SQLi / XSS / CSRF / access control
    ├── coding-standards.md          # Drupal coding standards, Coder/PHPCS
    ├── api-theming.md               # Hooks, render arrays, DB API, Field API, theming
    ├── performance-caching.md       # Caching layers, Views, drupal_static, aggregation
    ├── deployment-maintenance.md    # Drush, hook_update_N, Features, EOL/migration
    └── recovery-restore.md          # Restore from dump, rebuild codebase/files, incident recovery
```

## How to use this skill

1. **Trigger**: any prompt about Drupal 7 — "fix this module", "add a form", "secure this query", "why is this page slow", "deploy this change", "migrate off Drupal 7", "restore the site from the dump", "recover admin access". The `description` in [`SKILL.md`](SKILL.md) routes such prompts to this skill.
2. **Always-loaded**: [`SKILL.md`](SKILL.md) carries the critical rules and workflow (kept under ~5k words).
3. **Load on demand**: the agent opens a `references/*.md` file when the task touches that area (security, standards, APIs, performance, deployment, recovery).

### Effective agent workflow on this codebase

- **Before editing**: `drush pm-list --status=enabled`, locate custom modules in `sites/all/modules/custom`, read the module's `.info`/`.install`.
- **While coding**: follow the hook/render/DB/Field API patterns in [`references/api-theming.md`](references/api-theming.md); run Coder/PHPCS per [`references/coding-standards.md`](references/coding-standards.md).
- **Before merge**: run the security checklist in [`references/security.md`](references/security.md#quick-security-checklist).
- **Before release**: follow the deploy runbook in [`references/deployment-maintenance.md`](references/deployment-maintenance.md#deploy-runbook-canonical-order).
- **Restoring/rebuilding**: follow [`references/recovery-restore.md`](references/recovery-restore.md) and run `scripts/inventory_site_from_dump.py` against the dump.

## Research sources (GitHub, 5+ stars and/or 5+ forks)

| Repository | Stars | Forks | Relevance |
|---|---|---|---|
| [`drupal/drupal`](https://github.com/drupal/drupal) (7.x branch) | 4280 | 1984 | Core — canonical API reference |
| [`drupal-composer/drupal-project`](https://github.com/drupal-composer/drupal-project) | 1563 | 907 | Composer project template (migration target scaffolding) |
| [`geerlingguy/drupal-vm`](https://github.com/geerlingguy/drupal-vm) | 1349 | 619 | Local Drupal dev VM (archived, still useful for local D7 envs) |
| [`pfrenssen/coder`](https://github.com/pfrenssen/coder) (drupal/coder) | 30 | 52 | Drupal coding standards + PHPCS sniffs |
| [`acquia/coding-standards-php`](https://github.com/acquia/coding-standards-php) | 20 | 15 | Acquia PHP/Drupal sniffs |

Canonical non-repo references used: [Drupal coding standards](https://www.drupal.org/docs/develop/standards), [Drupal 7 best practices](https://www.drupal.org/docs/7/site-building-best-practices/best-practices), [UN WFP Drupal 7 Standards & Best Practice](http://andrewholgate.github.io/un-wfp-drupal7-standards-best-practice/), and the [Drupal 7 API reference](https://api.drupal.org/api/drupal/7.x).

## How to install to the common (global) skills

The project-level copy lives at `.kilocode/skills/drupal-7-best-practices/`. To make it available across all projects, copy the whole directory to the user skills folder:

```bash
cp -r .kilocode/skills/drupal-7-best-practices /home/stan/.kilocode/skills/drupal-7-best-practices
```

(Or run the same `cat > ...` content there.) The `description` frontmatter makes it auto-discoverable by the agent in any project.

## Success criteria

- Agent never suggests Drupal 8+ patterns (Twig/YAML/Symfony) for this Drupal 7 site.
- All new/changed code follows Drupal 7 conventions and passes Coder/PHPCS.
- Security checklist passes (no SQL injection, XSS, missing access control).
- Deploys are reproducible and sequenced (`updb` → `fr` → `cc`).
- The EOL/migration risk is surfaced and tracked for `taktaev.com`.
- A restore-from-dump path is documented, tested, and produces a complete module/theme manifest.
