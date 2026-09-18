# Drupal 7 Recovery & Restoration Playbook

Use this when restoring a Drupal 7 site from a backup, rebuilding a codebase from only a database dump, recovering admin access, or responding to a broken/hacked site. **This project (`taktaev.com`) currently has only a database dump — no code and no `files/` directory — so the "rebuild from dump" path below is the primary scenario.**

## 1. Understand what you actually have

A Drupal 7 site is three independent pieces that must all be restored:

| Piece | Where it lives | Restored from |
|---|---|---|
| **Database** | MySQL/MariaDB | `*.sql` dump (e.g. [`DB/a145188_taktaevr_2022-03-12_15_09.sql`](../../../DB/)) |
| **Codebase** | `webroot` on disk | Git repository, or a matching Drupal 7 core + contrib download |
| **Files** | `sites/default/files/` (public/private) | filesystem backup / `file_managed` table reference |

A database dump alone contains the **content, configuration, and the module/theme inventory** — but not the PHP code or uploaded files. You must reconstruct the other two pieces.

## 2. Inventory the site FROM the dump (before importing)

Run the bundled script to extract the Drupal version and the module/theme list:

```bash
python3 scripts/inventory_site_from_dump.py DB/a145188_taktaevr_2022-03-12_15_09.sql
```

It reports:
- **Core version** (from the `system` module `schema_version`, e.g. `7081` → Drupal **7.81**).
- **Enabled modules** (core vs. `sites/…` contrib) and **enabled themes**.
- Disabled modules, which are safe to omit from the rebuild.

Manual SQL equivalents (after import, or against the dump):

```sql
-- Core version (system module schema_version)
SELECT schema_version FROM system WHERE name = 'system';

-- Enabled contrib modules
SELECT name, filename, schema_version FROM system
WHERE type = 'module' AND status = 1 AND filename LIKE 'sites/%';

-- Enabled themes
SELECT name, filename FROM system
WHERE type = 'theme' AND status = 1;
```

## 3. Restore the database

```bash
# Create an empty DB and import
mysql -u USER -p -e "CREATE DATABASE taktaev CHARACTER SET utf8 COLLATE utf8_general_ci;"
mysql -u USER -p taktaev < DB/a145188_taktaevr_2022-03-12_15_09.sql
```

- The dump is a standard `mysqldump` (header shows `Server version 5.7.22-22-log`); it is compatible with MySQL 5.7/8.0 and MariaDB.
- After import, verify the `system` and `users` tables are non-empty.

## 4. Reconstruct the codebase (the hard part)

### 4.1 Core
1. Note the exact version from step 2 (e.g. 7.81).
2. Download the **same** minor release from https://www.drupal.org/project/drupal/releases (or restore core from Git at the matching tag `7.x` → e.g. `7.81`).
3. Ideally bring core to the final release **7.102** and run `drush updb` — but do this after a successful same-version restore first, so you can distinguish "restore broken" from "upgrade broken".

### 4.2 Contrib modules & themes
1. From the inventory, recreate each contrib module/theme under `sites/all/modules/` and `sites/all/themes/`.
2. If you have the original Git repo, restore from it (preferred — exact versions). Otherwise download each from drupal.org at a compatible version (match the `schema_version` / serialized `info.version` in the `system` table).
3. **Enabled contrib modules in this site's `system` table** (authoritative — from the script output): `cck`, `content_migrate`, `ckeditor`, `ctools`, `entity`, `ljxp` (likely custom), `module_filter`, `module_missing_message_fixer`, `pathauto`, `synonyms` (+ `synonyms_provider_field`/`synonyms_provider_property`/`synonyms_search`), `taxonomy_manager`, `token`, `views` + `views_ui`, `webform`. Restore these at compatible releases and audit their security status.
4. Custom modules are NOT recoverable from the dump — they must come from your code repository. If the repo is lost, they must be rebuilt from spec.

### 4.3 `settings.php`
```php
// sites/default/settings.php — minimal, correct DB creds
$databases = array(
  'default' => array(
    'default' => array(
      'database' => 'taktaev',
      'username' => 'DBUSER',
      'password' => 'DBPASS',
      'host'     => 'localhost',
      'driver'   => 'mysql',
      'prefix'   => '',
    ),
  ),
);
$update_free_access = FALSE;
```

### 4.4 Files directory
```bash
mkdir -p sites/default/files
chmod 755 sites/default
chmod -R 755 sites/default/files   # web server must be able to write
```
- Verify `variable` table file paths match reality:
  ```sql
  SELECT name, value FROM variable
  WHERE name IN ('file_public_path','file_private_path','file_temporary_path','file_default_scheme');
  ```
- Uploaded files are **not** in the dump — restore `files/` from a filesystem backup, or accept that attachments are missing (the `file_managed` table will still list them).

## 5. Post-restore rebuild (Drush)

```bash
drush rr                  # registry rebuild (re-scan classes/includes)
drush cc all              # clear all caches
drush updb -y             # apply any pending update hooks
drush cron                # verify cron runs
drush status              # confirm version + DB connection
```

If Drush isn't installed yet, bootstrap it after the codebase exists (`composer`/`pear` or download `drush.phar` for Drush 8).

## 6. Recover admin access

```bash
# Reset a known account's password
drush user-password admin --password='NewPass!'

# Generate a one-time login link (uid 1)
drush uli            # prints http://site/user/reset/1/TOKEN/login

# Or directly in SQL (then clear sessions)
UPDATE users SET pass = '$S$...' WHERE uid = 1;   # use drush to generate the hash instead
```

## 7. White Screen of Death (WSOD) & broken-site triage

1. **Reveal the error**: temporarily set `error_reporting(E_ALL)` and `ini_set('display_errors', '1')` in `settings.php`, or check `sites/default/files/tmp/` and the PHP error log.
2. **Check the watchdog**: `drush watchdog-show` or read the `watchdog` table:
   ```sql
   SELECT message, variables, timestamp FROM watchdog ORDER BY timestamp DESC LIMIT 20;
   ```
3. **Memory**: raise `memory_limit` (Drupal 7 + many modules needs ≥ 256M):
   ```php
   ini_set('memory_limit', '256M');
   ```
4. **Disable the culprit module** (a fatal in `hook_*` can white-screen the whole site):
   ```bash
   drush dis broken_module -y
   # or, if bootstrap fails entirely:
   mysql -u USER -p DBNAME -e "UPDATE system SET status=0 WHERE name='broken_module';"
   drush cc all
   ```
5. **Verify `.htaccess`** is present and unmodified (Drupal 7 relies on it for URL rewriting + security).

## 8. Full backups & the Drush archive (preventative)

```bash
# Full snapshot: code + database + files in one tarball
drush archive-dump --destination=/backups/taktaev-$(date +%F).tar.gz

# Restore a full snapshot on a fresh host
drush archive-restore /backups/taktaev-YYYY-MM-DD.tar.gz
```

A complete, recoverable backup = **code (Git) + `drush sql-dump` + `sites/default/files/`**. A DB dump alone is necessary but not sufficient.

## 9. Security-incident recovery

If the site was compromised:
1. **Freeze and snapshot** the current state (forensics) before changing anything.
2. **Diff core against a clean copy** (checksums): `drush core-check` or `diff -r webroot drupal-7.102-clean`.
3. Find recently modified/added files: `find . -mtime -30 -type f` (look for `*.php` in `files/`, obfuscated files, new files in `modules/`).
4. **Reinstall clean core** (same version), reapply patches, re-verify contrib module checksums.
5. **Rotate all credentials**: DB user, admin passwords, `settings.php` salts, any API keys.
6. Run the security checklist in [`security.md`](security.md) and re-apply `drush pm-update`.

## 10. Verification checklist (before declaring "recovered")

```
□ Database imported; system/users tables populated
□ Codebase matches core version (drush status)
□ All enabled contrib modules/themes present (system table vs. disk)
□ settings.php DB credentials correct; no secrets committed
□ sites/default/files/ exists and is writable
□ drush rr + drush cc all + drush updb run clean
□ Homepage renders; admin login works (drush uli)
□ Watchdog clean of fatal errors / repeated access-denied
□ Uploaded files restored (or their absence documented)
□ Security updates applied; D7ES/migration decision recorded
```
