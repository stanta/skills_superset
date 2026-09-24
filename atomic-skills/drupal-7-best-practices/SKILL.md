---
name: drupal-7-best-practices
description: This skill should be used when developing, refactoring, reviewing, securing, maintaining, or recovering/restoring a Drupal 7 site. It provides Drupal 7-specific best practices for coding standards (Coder/PHPCS), security hardening (SQL injection, XSS, CSRF, access control), the Database and Field/Entity APIs, render arrays and PHPTemplate theming, caching/performance, Drush-driven maintenance, update hooks, Features-driven configuration management, disaster recovery and site restoration from database dumps and backups, and the Drupal 7 end-of-life support and migration path. Use it for any Drupal 7 site — including legacy sites such as taktaev.com — instead of Drupal 8+ skills that assume Twig, YAML configuration, and Symfony services.
metadata:
  category: development
  source:
    - repository: https://github.com/drupal/drupal
      path: 7.x
    - repository: https://github.com/pfrenssen/coder
    - repository: https://github.com/acquia/coding-standards-php
    - repository: https://github.com/drupal-composer/drupal-project
---

# Drupal 7 Development & Maintenance Best Practices

> Drupal 7 is a procedural-PHP, hook-driven CMS. It is **not** Drupal 8/9/10/11: there is no Twig, no YAML config export, no Symfony services, no `src/` directory, and no Composer-managed codebase by default. Anyone applying modern Drupal patterns here will break the site. This skill exists so that an agent working on a Drupal 7 codebase — such as `taktaev.com` — uses the *correct* era-specific APIs, security discipline, and deployment rituals instead of cargo-culting Drupal 10 advice.

## ⚠️ Context You Must Internalize First

1. **Drupal 7 reached official community End of Life on 5 January 2025.** Core no longer receives free security advisories from drupal.org. Production sites must either (a) run under a **Drupal 7 Vendor Extended Support (D7ES)** agreement (Tag1 Consulting, HeroDevs, and other approved vendors), (b) migrate to Drupal 10/11, or (c) migrate to **Backdrop CMS** (the maintained Drupal 7 fork). Treat "we're on Drupal 7" as a live security risk until one of these is true.
2. **The code is PHP procedural + hooks.** Modules declare themselves in a `.info` file (`core = 7.x`), implement hooks in `.module` and `.install` files, and register menu routes via [`hook_menu()`](#hooks). There are no PSR-4 namespaces in core modules; third-party modules may use them via `files[]`.
3. **Sanitize on output, validate on input, parameterize on query.** These three disciplines are the entire security model and are non-negotiable (see [`references/security.md`](references/security.md)).
4. **Configuration lives in the database, managed in code via Features + Strongarm.** There is no `config/sync`. Reproducibility comes from `hook_update_N()`, `hook_features_api()`, and `variable_get()/variable_set()` wrapped in Feature exports.
5. **Performance = correct caching, not a plugin.** Drupal 7 is fast with `cache_page`, block caching, Views caching, render `#cache`, and CSS/JS aggregation — and collapses without them (see [`references/performance-caching.md`](references/performance-caching.md)).

---

## 🚨 Critical Rules (non-negotiable)

1. **Never write SQL by string concatenation — always use placeholders.** `db_query('SELECT * FROM {node} WHERE nid = :nid', array(':nid' => $nid))`, or the dynamic `db_select()` builder with `->condition()`. Raw interpolated variables are an instant SQL-injection vulnerability.
2. **Sanitize every piece of output.** Plain text → `check_plain()`; user HTML → `filter_xss()`; URLs → `check_url()`/`valid_url()` + `filter_xss()`; filtered body text → `check_markup()`. Use `t()` for translatable strings and pass variables as `@var` (escaped), never `!var` unless you have already escaped it.
3. **Never bypass the Form API's built-in CSRF protection.** Always build forms with `drupal_get_form()` and the Form API — do not hand-roll HTML `<form>` + `$_POST`. Confirm user actions (deletes, payments, sensitive mutations) additionally use a confirm form.
4. **Enforce access control, don't just hide UI.** Every menu callback needs an `access callback`/`access arguments` (or `user_access()`/`node_access()` inside). Every custom field needs `hook_field_access()`, every sensitive node type `hook_node_access()`. Hiding a link is not security.
5. **Use the Field API / Entity API — never read `$node->field_x[LANGUAGE_NONE][0]['value']` blindly.** Prefer `field_get_items()`, `field_view_field()`, and the Entity API's `entity_metadata_wrapper()` which understands field language, deltas, and metadata.
6. **Alter, don't hack.** Use `hook_form_alter()`, `hook_node_view()`, `hook_entity_load()`, `hook_views_*`. Never edit core or contrib files directly (your changes are lost on update); use patches or an override module.
7. **Every schema/data change ships as a numbered `hook_update_N()`** in `.install`. Never hand-edit the database on production. `hook_update_N()` must be idempotent and re-runnable by `drush updb`.
8. **Cache aggressively but correctly.** Return `#cache` on expensive render arrays, set block `cache` constants appropriately, enable Views caching, and invalidate caches in hooks via `cache_clear_all()` or by bumping cache tags — never by disabling the page cache to "fix" stale content.
9. **Run `drush updb && drush fr -y && drush cc all` on every deploy, in that order** (after taking the site into maintenance mode and backing up the DB). A Drupal 7 deploy without cache rebuild serves stale code.
10. **Never deploy with `$update_free_access` enabled or error display on.** In `settings.php`, ensure `error_reporting` is production-safe, display_errors is off, and log to the watchdog (`dblog`) or syslog.
11. **A recoverable site = code (Git) + `drush sql-dump` + `sites/default/files/`.** Take a full backup before any risky change; know how to restore from the database dump alone (the `system` table inventories modules/themes and the core version). See [`references/recovery-restore.md`](references/recovery-restore.md) and run `scripts/inventory_site_from_dump.py` to reconstruct a missing codebase.

---

## 🔄 Workflow Process

### Step 1 — Orient on the codebase (before touching anything)
1. Confirm the Drupal version from `CHANGELOG.txt` / `system` table — do not assume.
2. Inventory enabled modules (`drush pm-list --status=enabled` or the `system` table) and the custom vs. contrib split.
3. Locate the custom module/theme directories (`sites/all/modules/custom`, `sites/all/themes`, or `profiles/`).
4. Check for a `sites/default/settings.php` environment split and any Features/Strongarm exports.
5. Read the existing `*.info`, `*.install`, and `*.module` files to learn the established conventions.

### Step 2 — Write code following Drupal 7 standards
1. Create the module scaffold: `my_module.info` (`core = 7.x`), `my_module.module`, `my_module.install`.
2. Implement hooks with correct names and signatures (see [`references/api-theming.md`](references/api-theming.md)).
3. Add `hook_permission()` for anything privileged; enforce access in every callback.
4. Parameterize all queries, sanitize all output, validate all input.
5. Add `hook_schema()` and `hook_update_N()` for any new tables/columns.
6. Run Coder/PHPCS locally and fix violations before committing (see [`references/coding-standards.md`](references/coding-standards.md)).

### Step 3 — Theme correctly
1. Register templates via `hook_theme()` (or the `.info` `theme[]` registry for themes) with `template` / `variables` / `render element`.
2. Use `.tpl.php` templates + `template_preprocess_*` hooks; attach CSS/JS with `drupal_add_css()/drupal_add_js()/drupal_add_library()`.
3. Build output as render arrays (`#theme`, `#markup`, `#prefix`/`#suffix`, `#attached`), then `render()` them — do not `echo` markup directly.

### Step 4 — Optimize and harden
1. Profile first (`devel` + query log, XHProf/Tideways); fix the slowest queries.
2. Add render/block/Views caching with correct invalidation.
3. Re-run the security checklist in [`references/security.md`](references/security.md).

### Step 5 — Deploy and maintain
1. Maintenance mode → DB backup → deploy code → `drush updb` → `drush fr -y` → `drush cc all` → verify.
2. Track `SA-CORE` / module advisories; apply via `drush pm-update` (or D7ES vendor).
3. Continuously evaluate the EOL exit path (D7ES vs. migrate to Drupal 10/11 vs. Backdrop) — see [`references/deployment-maintenance.md`](references/deployment-maintenance.md).

---

## 📚 References (load as needed)

| Reference | Contents | Load when |
|---|---|---|
| [`references/security.md`](references/security.md) | SQLi/XSS/CSRF/access-control checklists, sanitization table, Form API, file uploads, advisories | Any code touching input, output, or access |
| [`references/coding-standards.md`](references/coding-standards.md) | Drupal coding standards, naming, docblocks, Coder/PHPCS setup, `.info`/`.install` format | Writing new modules or reviewing code |
| [`references/api-theming.md`](references/api-theming.md) | Hooks catalog, render arrays, Database API, Field/Entity API, theming/`.tpl.php` | Implementing any feature |
| [`references/performance-caching.md`](references/performance-caching.md) | Cache bins, block/Views/render caching, `drupal_static`, aggregation, backends | Performance work |
| [`references/deployment-maintenance.md`](references/deployment-maintenance.md) | Drush commands, `hook_update_N`, Features/Strongarm, deploy runbook, EOL/migration | Releases, updates, maintenance |
| [`references/recovery-restore.md`](references/recovery-restore.md) | Restore from DB dump, rebuild codebase/files, `drush archive-dump/restore`, recover admin, WSOD triage, security incident recovery | Restoring, recovering, or rebuilding a site |

**Grep patterns** for large references:
- Security sink functions: `grep -rEn "db_query|db_select|check_plain|filter_xss|check_url|check_markup|t\(" sites/all/modules`
- Raw superglobals (must be validated): `grep -rEn "\$_(GET|POST|REQUEST|COOKIE|FILES)" sites/all`
- Direct field array access (usually a smell): `grep -rEn "LANGUAGE_NONE|->field_[a-z_]+\[" sites/all/modules`
- Missing access on routes: `grep -rEn "access callback|access arguments|user_access|node_access" sites/all/modules`
- Inventory a dump (recovery): `python3 scripts/inventory_site_from_dump.py DB/dump.sql`

---

## ✅ Success criteria

- Zero string-concatenated SQL; every query parameterized or built via `db_select()`.
- Every rendered string escaped via `check_plain()`/`filter_xss()`/`check_markup()`/`t()`.
- Every privileged callback enforces access control.
- New tables/columns ship via `hook_schema()` + `hook_update_N()`, idempotent.
- Custom code passes Coder/PHPCS with no errors.
- Deploys are reproducible: `updb` + `fr` + `cc` in order, maintenance mode, DB backup.
- A restore-from-dump path is documented and tested; the code + DB + files backup set is complete.
- The EOL risk is documented and an exit path (D7ES / migration) is tracked.
