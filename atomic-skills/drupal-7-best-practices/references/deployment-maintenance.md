# Drupal 7 Deployment & Maintenance

Covers Drush-driven administration, the deploy runbook, configuration-in-code via Features + Strongarm, and the Drupal 7 end-of-life exit path.

## 1. Drush commands (Drush 8 for Drupal 7)

```bash
drush status                          # environment + Drupal version
drush pm-list --status=enabled        # enabled modules
drush en my_module -y                 # enable
drush dis my_module -y                # disable
drush updb -y                         # run hook_update_N() (database updates)
drush cc all                          # clear all caches
drush cc css-js                       # clear aggregated assets
drush fr my_feature -y                # revert a Feature to code
drush features-list                   # list Features and their state
drush fu my_feature -y                # update a Feature from overrides
drush pm-update -y                    # update modules (respect security releases)
drush pm-updatecode                   # report available updates
drush cron                            # run cron
drush sql-cli / drush sql-dump / drush sql-sync
drush vget my_module_limit            # get a variable
drush vset my_module_limit 20         # set a variable
drush user-create / drush user-password
```

## 2. Configuration in code — Features + Strongarm

Drupal 7 has no `config/sync`. Reproducible configuration is exported to a **Feature module** and stored in code.

```php
// my_feature.features.inc
function my_feature_features_api() {
  return array(
    'my_feature' => array(
      'name' => 'My Feature',
      'description' => 'Exports content types, fields, views, variables.',
      'components' => array(
        'node' => array('article', 'page'),
        'field_base' => array('body', 'field_tags'),
        'field_instance' => array('node-article-body'),
        'views_view' => array('my_view'),
        'variable' => array('site_name', 'my_module_limit'),
      ),
    ),
  );
}
```

- **Strongarm** exports variables via `variable_get`/`variable_set` in a `strongarm` component so settings are code, not hidden DB state.
- **CTools exportables** (views, panels, page_manager, etc.) integrate through `hook_ctools_plugin_api()`.
- After importing on a target environment, run `drush fr my_feature -y` to apply the exported config.

## 3. Schema & data changes — `hook_update_N()`

Every production schema/data change ships as a numbered update hook (see [`coding-standards.md`](coding-standards.md#install-file-conventions) and [`api-theming.md`](api-theming.md)). Rules:

- Idempotent: guard against re-running (`db_field_exists()`, `db_table_exists()`).
- Use Schema API helpers (`db_add_field`, `db_change_field`, `db_add_index`, `db_create_table`).
- Large data migrations use `$sandbox` for batch-safe execution.
- Apply with `drush updb -y` on every deploy.

## 4. Deploy runbook (canonical order)

```bash
# 1. Pre-deploy
drush vset maintenance_mode 1        # or admin UI maintenance mode
drush sql-dump --gzip --result-file=../backups/pre-deploy.sql.gz

# 2. Deploy code (git pull / rsync / artifact)

# 3. Post-deploy, in this exact order
drush updb -y                        # database schema/data updates
drush fr -y                          # revert all Features to code
drush cc all                         # clear caches (serves new code/config)

# 4. Verify & exit maintenance
drush vset maintenance_mode 0
```

Never skip the cache clear after a code deploy — Drupal 7 serves stale render/asset caches otherwise.

## 5. `settings.php` environment split

```php
// sites/default/settings.php (committed, no secrets)
$local_settings = __DIR__ . '/settings.local.php';
if (file_exists($local_settings)) {
  require_once $local_settings;
}
```

- `settings.local.php` holds per-environment DB credentials and is **git-ignored**.
- Production-safe defaults in `settings.php`:
  ```php
  $update_free_access = FALSE;
  error_reporting(E_ALL & ~E_DEPRECATED & ~E_STRICT);
  ini_set('display_errors', '0');
  ini_set('log_errors', '1');
  ```

## 6. Drupal 7 End of Life & migration

**Drupal 7 community support ended 5 January 2025.** Free `SA-CORE` security advisories have stopped. This site's database dump indicates **core 7.54** (circa 2017) — well behind the final release, 7.102 — so it must not be left unpatched.

### Option A — Stay on D7 with Vendor Extended Support (D7ES)
- Subscribe to a Drupal 7 **Vendor Extended Support** program (approved vendors: Tag1 Consulting, HeroDevs, and others listed on drupal.org).
- Receive backported security fixes beyond EOL; keep running `drush pm-update`.
- Suitable only as a short-term bridge while planning migration.

### Option B — Migrate to Drupal 10/11
- Use the **Migrate** + **Migrate Upgrade** (`migrate_upgrade` in Drush 8) path, or a phased rebuild.
- Re-model content types/fields in Drupal 8+ (Fields API carries over conceptually), migrate Views, and rebuild custom modules as Symfony-based plugins/services.
- This is the long-term destination.

### Option C — Migrate to Backdrop CMS
- **Backdrop** is a maintained fork of Drupal 7 with a near-identical API/hook model (lower migration friction).
- Suitable for sites that want to preserve Drupal-7-style architecture but need active security releases.

### Recommendation
Prioritize an explicit, dated exit decision: engage D7ES immediately for security, then commit to a Drupal 10/11 (or Backdrop) migration roadmap. A legacy Drupal 7 site with no plan is the single biggest ongoing risk.

## 7. Maintenance checklist (routine)

```bash
drush pm-updatecode          # what needs updating?
drush pm-update -y           # apply (after backup)
drush updb -y && drush fr -y && drush cc all
drush cron                   # verify cron runs clean
```

```
□ Core + contrib at latest (or D7ES vendor engaged)
□ No PHP errors / repeated access-denied in dblog/watchdog
□ Database backed up before every change
□ Features overridden? (drush features-list) — reconcile with drush fu/fr
□ Maintenance mode used for risky deploys
□ EOL exit path documented and dated
```
