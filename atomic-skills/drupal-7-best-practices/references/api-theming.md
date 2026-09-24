# Drupal 7 API & Theming Reference

Covers the four pillars of Drupal 7 development: hooks, render arrays, the Database API, the Field/Entity API, and PHPTemplate theming.

## 1. Hooks & the menu/router system

### `hook_menu()` — the router

```php
function my_module_menu() {
  $items = array();

  $items['my-module'] = array(
    'title' => 'My Module page',
    'page callback' => 'my_module_page',
    'access callback' => 'user_access',
    'access arguments' => array('access content'),
    'type' => MENU_NORMAL_ITEM,
  );

  $items['my-module/%node'] = array(
    'title' => 'Node detail',
    'page callback' => 'my_module_node_page',
    'page arguments' => array(1),   // the %node wildcard -> loaded node
    'access callback' => 'node_access',
    'access arguments' => array('view', 1),
  );

  return $items;
}
```

- `page callback` + `page arguments` define the handler; `%node` auto-loads the node.
- `access callback` / `access arguments` are mandatory for access control.
- `type` = `MENU_NORMAL_ITEM`, `MENU_CALLBACK`, `MENU_LOCAL_TASK`, `MENU_DEFAULT_LOCAL_TASK`.

### Alter hooks (prefer these over hacking)

```php
function my_module_form_alter(&$form, &$form_state, $form_id) {
  if ($form_id == 'node_article_form') {
    $form['field_tags']['#required'] = TRUE;
  }
}

function my_module_node_view($node, $view_mode, $langcode) {
  if ($node->type == 'article' && $view_mode == 'teaser') {
    $node->content['my_extra'] = array(
      '#markup' => t('Published @date', array('@date' => format_date($node->created))),
      '#weight' => 5,
    );
  }
}
```

### Blocks (core block API in D7)

```php
function my_module_block_info() {
  $blocks['latest_articles'] = array(
    'info' => t('Latest articles'),
    'cache' => DRUPAL_CACHE_GLOBAL,
  );
  return $blocks;
}

function my_module_block_view($delta = '') {
  if ($delta == 'latest_articles') {
    return array(
      'subject' => t('Latest'),
      'content' => array('#markup' => my_module_render_latest()),
    );
  }
}
```

## 2. Render arrays & theming

Drupal 7 output is a **render array**, converted to HTML with `render()`/`drupal_render()`. Never `echo` markup in a callback.

### Core render keys

```php
$build = array(
  '#theme' => 'item_list',           // theme function/template
  '#items' => array('One', 'Two'),   // list items
  '#markup' => check_plain($text),   // escaped markup
  '#prefix' => '<div class="wrap">',
  '#suffix' => '</div>',
  '#attributes' => array('class' => array('my-class')),
  '#attached' => array(              // CSS/JS attachment
    'css' => array(drupal_get_path('module', 'my_module') . '/my_module.css'),
    'js' => array(drupal_get_path('module', 'my_module') . '/my_module.js'),
  ),
  '#cache' => array(                 // render caching
    'keys' => array('my_module', 'latest', $node->nid),
    'bin' => 'cache',
    'expire' => CACHE_TEMPORARY,
  ),
);

print render($build);  // or return $build from a page/block callback
```

### Custom templates via `hook_theme()`

```php
function my_module_theme($existing, $type, $theme, $path) {
  return array(
    'my_module_card' => array(
      'variables' => array('node' => NULL),
      'template' => 'my-module-card',  // uses my-module-card.tpl.php
      'path' => $path . '/templates',
    ),
  );
}
```

`my-module-card.tpl.php`:

```php
<div class="card">
  <h2><?php print check_plain($node->title); ?></h2>
</div>
```

Render it:

```php
$output = theme('my_module_card', array('node' => $node));
```

### Preprocess functions

```php
// In a theme's template.php or a module
function mytheme_preprocess_my_module_card(&$variables) {
  $node = $variables['node'];
  $variables['teaser'] = text_summary($node->body[LANGUAGE_NONE][0]['value'], NULL, 200);
}
```

### Adding JS/CSS & libraries (theme layer)

```php
drupal_add_css(drupal_get_path('module', 'my_module') . '/my_module.css');
drupal_add_js(drupal_get_path('module', 'my_module') . '/my_module.js');
drupal_add_js(array('myModule' => array('basePath' => base_path())), 'setting');
drupal_add_library('system', 'ui.datepicker');
drupal_add_html_head($element, 'unique-key');
```

## 3. Database API

```php
// SELECT — builder
$query = db_select('node', 'n')
  ->fields('n', array('nid', 'title'))
  ->condition('type', 'article')
  ->orderBy('created', 'DESC')
  ->range(0, 10);
$result = $query->execute();
while ($row = $result->fetchAssoc()) { /* ... */ }

// SELECT — static with placeholders
$count = db_query('SELECT COUNT(*) FROM {node} WHERE type = :type', array(':type' => 'article'))
  ->fetchField();

// INSERT
$id = db_insert('my_table')->fields(array('title' => $title))->execute();

// UPDATE
db_update('my_table')->fields(array('status' => 1))->condition('id', $id)->execute();

// DELETE
db_delete('my_table')->condition('id', $id)->execute();

// MERGE (upsert)
db_merge('my_table')->key(array('id' => $id))->fields(array('title' => $title))->execute();

// LIKE (escaped)
$query = db_select('node', 'n')->condition('title', '%' . db_like($q) . '%', 'LIKE');
```

### Pagination & sorting

```php
$query = db_select('node', 'n')
  ->extend('PagerDefault')->limit(20)
  ->extend('TableSort')->orderByHeader($header);
$query->fields('n', array('nid', 'title'));
$result = $query->execute();
// Render pager:
$build[] = array('#theme' => 'pager');
```

### Transactions

```php
$txn = db_transaction();
try {
  db_insert(...)->execute();
  db_insert(...)->execute();
}
catch (Exception $e) {
  $txn->rollback();
  watchdog_exception('my_module', $e);
  throw $e;
}
```

## 4. Field API & Entity API

### Reading field values safely

```php
// With field_get_items / field_view_field (core Field API)
$items = field_get_items('node', $node, 'field_tags');
if ($items) {
  foreach ($items as $item) {
    $tid = $item['tid'];
  }
}

$rendered = field_view_field('node', $node, 'field_image', array('label' => 'hidden'));
```

### Entity API wrapper (Entity API module — preferred)

```php
$wrapper = entity_metadata_wrapper('node', $node);
$title = $wrapper->title->value();       // ->value()
$wrapper->field_description->set('New'); // ->set()
$wrapper->save();
```

### Loading entities

```php
$node = node_load($nid);
$nodes = node_load_multiple($nids);
$nodes = node_load_multiple(array(), array('type' => 'article', 'status' => 1)); // conditions
```

### Direct field access (understand the shape, but prefer the APIs)

```php
// field data lives under the language key (LANGUAGE_NONE = 'und' for single-language)
$value = $node->field_custom[LANGUAGE_NONE][0]['value'];
```

Use this only when the Field/Entity APIs are unavailable — the wrapper and `field_get_items()` are safer because they understand translation and metadata.

## 5. Forms (Form API)

```php
function my_module_settings_form($form, &$form_state) {
  $form['limit'] = array(
    '#type' => 'textfield',
    '#title' => t('Limit'),
    '#default_value' => variable_get('my_module_limit', 10),
    '#size' => 4,
    '#element_validate' => array('element_validate_integer_positive'),
  );
  return system_settings_form($form); // auto-saves to variables
}

function my_module_custom_form_submit($form, &$form_state) {
  variable_set('my_module_limit', $form_state['values']['limit']);
  drupal_set_message(t('Saved.'));
}
```

Common element types: `textfield`, `textarea`, `select`, `checkboxes`, `radios`, `checkbox`, `managed_file`, `value`, `markup`, `fieldset`, `container`, `password_confirm`, `tableselect`.

## 6. Cron & queues

```php
function my_module_cron() {
  // light periodic work
}

function my_module_cron_queue_info() {
  $queues['my_module_jobs'] = array(
    'worker callback' => 'my_module_process_job',
    'time' => 30,
  );
  return $queues;
}

function my_module_process_job($job) {
  // $job->data — process one unit of work
}
```
