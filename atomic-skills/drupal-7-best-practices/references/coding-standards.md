# Drupal 7 Coding Standards & Conventions

Source: [Drupal coding standards](https://www.drupal.org/docs/develop/standards) — version-independent and enforced by the **Coder** module + PHP_CodeSniffer.

## Why it matters

Drupal 7 code is read far more often than written, and the community tooling (`Coder`/PHPCS, `pareview.sh`) only works if conventions are followed. Consistent hook names, docblocks, and `.info`/`.install` structure are what make a module reviewable, patchable, and updatable.

## Enforcing standards automatically

Install PHP_CodeSniffer + Coder, then register the `Drupal` and `DrupalPractice` standards:

```bash
composer require --dev drupal/coder dealerdirect/phpcodesniffer-composer-installer
vendor/bin/phpcs --config-set installed_paths vendor/drupal/coder/coder_sniffer
vendor/bin/phpcs --standard=Drupal,DrupalPractice --extensions=php,inc,module,install sites/all/modules/custom
vendor/bin/phpcbf --standard=Drupal,DrupalPractice sites/all/modules/custom  # auto-fix
```

Repositories: [`drupal/coder`](https://github.com/pfrenssen/coder) (52+ forks) and [`acquia/coding-standards-php`](https://github.com/acquia/coding-standards-php).

## `.info` file format (module/theme declaration)

```ini
name = My Module
description = Provides custom functionality for the site.
core = 7.x
package = Custom
dependencies[] = node
dependencies[] = views
files[] = my_module.module
files[] = includes/my_module.admin.inc
version = 7.x-1.0
; php = 5.3  (optional PHP requirement)
```

Rules:
- `core = 7.x` is mandatory.
- `dependencies[]` lists machine names of required modules.
- `files[]` registers any `.inc` file so it is loaded for class discovery.
- The `name` and `description` appear in the admin UI; keep `description` under ~255 chars.

## File structure conventions

```
my_module/
├── my_module.info          # declaration (required)
├── my_module.module        # hooks (required)
├── my_module.install       # schema, install, update hooks (required if DB)
├── includes/               # optional class/helper files (list in files[])
│   └── my_module.admin.inc
├── my_module.pages.inc     # page callbacks
├── my_module.admin.inc     # admin forms
└── my_module.test          # SimpleTest tests
```

## Naming conventions

- Module/theme machine names: lowercase, alphanumeric + underscores (`my_module`).
- Function names: `<module>_<hook>` or `<module>_<descriptive>` — e.g. `my_module_node_view()`, `my_module_form_alter()`.
- Constants: uppercase with underscores (`MY_MODULE_DEFAULT_LIMIT`).
- Classes: `UpperCamelCase`; file named `Class.inc`, listed in `files[]`.
- Never prefix global functions with `drupal_`, `node_`, `user_`, etc. (collides with core).
- Don't define PHP functions/constants that core or common contrib already define.

## Docblocks (required for all functions & hooks)

```php
/**
 * Implements hook_node_view().
 */
function my_module_node_view($node, $view_mode, $langcode) {
  // ...
}
```

- Every hook implementation opens with `/** Implements hook_NAME(). */`.
- Public helper functions get a full docblock with `@param` and `@return`.

## Coding style highlights

- Indent with **two spaces** (no tabs).
- Opening brace on the same line; `else` on its own line.
- Control structures use spaces: `if ($x) {`, `foreach ($items as $item) {`.
- String concatenation uses `.` with spaces: `$full = $first . ' ' . $last;`.
- Use `'single quotes'` for strings without interpolation, `"double quotes"` only when interpolating.
- Use the `&&`/`||` operators with explicit parentheses for clarity; use `!empty()`/`isset()` guards.
- `return` early for guard clauses to reduce nesting.
- Use `t()` for every human-readable string; `watchdog()` for logging with a severity constant.

## Hook signature reference (most common)

```php
hook_menu()                                     // routes & menu items
hook_permission()                               // permissions
hook_theme($existing, $type, $theme, $path)     // theme registry
hook_form_alter(&$form, &$form_state, $form_id)
hook_form_FORM_ID_alter(&$form, &$form_state, $form_id)
hook_node_load($nodes, $types)
hook_node_view($node, $view_mode, $langcode)
hook_node_presave($node)
hook_node_insert($node) / hook_node_update($node) / hook_node_delete($node)
hook_entity_load($entities, $type)
hook_block_info() / hook_block_view($delta = '')
hook_cron() / hook_cron_queue_info() / hook_queue_info()
hook_mail($key, &$message, $params) / hook_mail_alter(&$message)
hook_schema() / hook_install() / hook_uninstall() / hook_update_N(&$sandbox)
hook_views_data() / hook_views_default_views()
hook_features_api() / hook_ctools_plugin_api()
```

Full catalog: [`api.drupal.org` — Drupal 7 hooks](https://api.drupal.org/api/drupal/7.x/search/hook_).

## `.install` file conventions

```php
function my_module_schema() {
  $schema['my_module_items'] = array(
    'description' => 'Stores custom items.',
    'fields' => array(
      'id' => array('type' => 'serial', 'not null' => TRUE, 'description' => 'Primary key'),
      'title' => array('type' => 'varchar', 'length' => 255, 'not null' => TRUE, 'default' => ''),
    ),
    'primary key' => array('id'),
  );
  return $schema;
}

function my_module_update_7001(&$sandbox) {
  db_add_field('my_module_items', 'weight', array(
    'type' => 'int', 'not null' => TRUE, 'default' => 0,
  ));
}

function my_module_update_7002(&$sandbox) {
  // Data migration / batch processing (supports $sandbox for long jobs).
}
```

- Update numbers are sequential and `7`-prefixed (`7001`, `7002`, ...).
- Use the Schema API helpers (`db_add_field`, `db_change_field`, `db_drop_field`, `db_create_table`, `db_drop_table`, `db_add_index`, ...) inside update hooks — never raw `ALTER`.
- Make update hooks idempotent: guard with `if (!db_field_exists(...))`.
- Long data migrations use `$sandbox` + `drush updb` batch support.
