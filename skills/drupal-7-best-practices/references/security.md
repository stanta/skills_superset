# Drupal 7 Security Best Practices

Security in Drupal 7 is three disciplines applied without exception:
**validate input**, **sanitize output**, **enforce access control**. Everything below is a specialization of those three.

## 1. SQL Injection — always parameterize

Never interpolate user data into SQL strings. Use one of two safe paths.

### Static queries — `db_query()` with named placeholders

```php
// CORRECT — placeholders, never concatenation
$result = db_query(
  'SELECT nid, title FROM {node} WHERE type = :type AND status = :status',
  array(':type' => 'article', ':status' => 1)
);
foreach ($result as $row) {
  // ...
}
```

```php
// WRONG — SQL injection
db_query("SELECT nid FROM {node} WHERE title LIKE '%" . $input . "%'");
```

- Table names are wrapped in `{braces}` so they are correctly prefixed.
- `db_like()` escapes user data for `LIKE` patterns: `db_query('... WHERE name LIKE :name', array(':name' => '%' . db_like($q) . '%'))`.

### Dynamic queries — `db_select()` builder

```php
$query = db_select('node', 'n')
  ->fields('n', array('nid', 'title'))
  ->condition('n.type', 'article')
  ->condition('n.status', 1)
  ->orderBy('n.created', 'DESC')
  ->range(0, 10);
$rows = $query->execute()->fetchAllAssoc('nid');
```

The builder (`db_select`, `db_insert`, `db_update`, `db_delete`, `db_merge`) handles escaping automatically via `condition()`. Only build raw fragments with `->where()` or `->having()` when necessary, and still pass placeholders:

```php
$query->where('n.created > :cutoff', array(':cutoff' => $timestamp));
```

### Other DB safety rules

- `db_insert('mytable')->fields(array(...))->execute()` — never build an `INSERT` string.
- Use `db_transaction()` for multi-step writes:
  ```php
  $txn = db_transaction();
  try {
    // multiple writes...
  }
  catch (Exception $e) {
    $txn->rollback();
    watchdog_exception('mymodule', $e);
  }
  ```
  Committing is implicit when `$txn` goes out of scope without `rollback()`.

## 2. Cross-Site Scripting (XSS) — sanitize on output

| Situation | Function |
|---|---|
| Plain text (title, name, single line) | `check_plain($string)` |
| Rich/HTML from an untrusted editor | `filter_xss($string)` |
| Admin-supplied HTML (trusted) | `filter_xss_admin($string)` |
| URLs (attributes, redirects) | `check_url($uri)` / `valid_url($uri)` |
| Body text with a text format | `check_markup($text, $format_id)` |
| Translatable UI string | `t('Hello @name', array('@name' => $name))` |

### `t()` placeholder rules (critical)

- `@variable` → escaped with `check_plain()` (safe default).
- `%variable` → wrapped in `<em>` (safe).
- `!variable` → **inserted raw** — only ever use when the value is already sanitized.

```php
// SAFE
return t('Welcome back, @username', array('@username' => $user->name));

// DANGEROUS — raw insertion of user data
return t('Welcome back, !username', array('!username' => $user->name));
```

### URL output

```php
$url = url('node/' . $node->nid);           // internal path -> alias
$safe = check_url($user_supplied_uri);       // sanitize external/protocol-relative
```

## 3. Cross-Site Request Forgery (CSRF) — use the Form API

- **Always** render forms through `drupal_get_form($form_id)` / the Form API. The Form API injects `form_build_id` and `form_token`, providing automatic CSRF protection.
- Never hand-write `<form>` + raw `$_POST` handling in a page callback.
- For destructive actions, use a **confirm form** (`confirm_form()`) and check `$form_state['values']['confirm']`.

```php
function mymodule_delete_form($form, &$form_state, $node) {
  return confirm_form($form,
    t('Delete %title?', array('%title' => $node->title)),
    'node/' . $node->nid,
    t('This action cannot be undone.'),
    t('Delete'), t('Cancel'));
}

function mymodule_delete_form_submit($form, &$form_state) {
  node_delete($form_state['values']['nid']);
  drupal_set_message(t('Deleted.'));
  $form_state['redirect'] = 'node';
}
```

## 4. Access Control — enforce, don't hide

### Menu callbacks

```php
function mymodule_menu() {
  $items['admin/reports/custom'] = array(
    'title' => 'Custom report',
    'page callback' => 'mymodule_report_page',
    'access callback' => 'user_access',
    'access arguments' => array('access custom report'),
    'type' => MENU_NORMAL_ITEM,
  );
  return $items;
}
```

Every `page callback` must have an `access callback` (default is `user_access`). For entity-level checks, write a custom access callback that calls `node_access('view', $node)` or `field_access()`.

### Permissions

```php
function mymodule_permission() {
  return array(
    'administer mymodule' => array(
      'title' => t('Administer MyModule'),
      'description' => t('Configure MyModule settings.'),
    ),
    'view private content' => array(
      'title' => t('View private content'),
    ),
  );
}
```

### Node / field / query access hooks

- `hook_node_access($node, $op, $account)` — per-node view/edit/delete control.
- `hook_field_access($op, $field, $entity_type, $entity, $account)` — per-field control.
- `hook_query_alter(QueryAlterableInterface $query)` / `hook_query_TAG_alter()` — enforce row-level filtering on listings (e.g., hide unpublished nodes).
- `hook_node_access_records()` + `hook_node_grants()` — the node access grant system (use `node_access_rebuild()` after changes).

```php
function mymodule_node_access($node, $op, $account) {
  if ($node->type == 'private_doc' && $op == 'view') {
    if (user_access('view private content', $account)) {
      return NODE_ACCESS_ALLOW;
    }
    return NODE_ACCESS_DENY;
  }
  return NODE_ACCESS_IGNORE;
}
```

## 5. Input validation & file uploads

- Validate every value from `$_GET`, `$_POST`, `$form_state['values']`, and external APIs.
- Use Form API element properties: `#required`, `#maxlength`, `#element_validate`, `'#options'`.
- For files, use the managed-file API and `file_validate_*`:

```php
$form['upload'] = array(
  '#type' => 'managed_file',
  '#title' => t('Upload'),
  '#upload_location' => 'public://mymodule/',
  '#upload_validators' => array(
    'file_validate_extensions' => array('pdf doc docx'),
    'file_validate_size' => array(5 * 1024 * 1024), // 5 MB
  ),
);
```

- Store sensitive files in the **private** filesystem (`private://`) and serve them through a menu callback that enforces access — never expose private files via `public://`.
- Never trust a filename or MIME type supplied by the client.

## 6. Redirects & headers

- `drupal_goto($path)` only after validating the target is a local/internal path (avoid open redirect).
- Use `drupal_access_denied()` / `drupal_not_found()` for 403/404 responses.
- Emit security headers in `hook_init()` or the theme: `X-Content-Type-Options: nosniff`, `X-Frame-Options: SAMEORIGIN`, `Referrer-Policy`, and (carefully) `Content-Security-Policy`.

## 7. Security updates & the Drupal 7 EOL problem

- **Drupal 7 core reached community EOL on 5 Jan 2025.** Free `SA-CORE` advisories stopped. See [`deployment-maintenance.md`](deployment-maintenance.md#drupal-7-end-of-life--migration) for the D7ES / migration options.
- While patched: subscribe to security advisories (`drush pm-updatecode` / `drush pm-updatestatus`) and apply core + contrib updates promptly.
- Track the `dblog`/watchdog for repeated "access denied", PHP errors, and failed logins.
- Keep `settings.php` out of version control (or use a separate `settings.local.php`), and never commit credentials/API keys.

## 8. Quick security checklist (run before merge/release)

```
□ 0 string-concatenated SQL; all db_query()/db_select() parameterized
□ All output escaped: check_plain / filter_xss / check_url / check_markup / t(@var)
□ No t('!var') with unescaped user data
□ All forms via drupal_get_form() / Form API (CSRF protected)
□ All menu callbacks have access callback/arguments
□ Custom permissions declared in hook_permission()
□ hook_node_access/hook_field_access cover sensitive entities/fields
□ File uploads use managed_file + file_validate_* ; private files behind access check
□ No credentials in code or committed config
□ Core + contrib security updates applied (or D7ES vendor engaged)
□ watchdog clean of repeated access-denied / PHP errors
```
