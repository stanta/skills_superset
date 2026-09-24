# Drupal 11 Configuration, Recipes, and Entity Modeling

## Classify Data Before Building

| Data kind | Use | Examples |
|---|---|---|
| Deployable behavior/settings | Configuration API | module settings, view displays, field definitions |
| Configurable records with identity/dependencies | Config Entity | image styles, roles, vocabularies, custom workflow definitions |
| Editorial/user-owned records | Content Entity | nodes, media, users, commerce orders |
| Environment-local mutable value | State API | last-run timestamp, deployment marker |
| Request/user temporary data | TempStore/session | multistep wizard progress |
| Sensitive value | secret manager or settings override | API key, database password |

Do not put content in configuration, configuration in state, or secrets in either exported configuration or repository files.

## Configuration Schema

Provide schema for every custom configuration object so Drupal can validate, translate, and type it.

```yaml
# config/schema/acme_catalog.schema.yml
acme_catalog.settings:
  type: config_object
  label: 'Catalog settings'
  mapping:
    items_per_page:
      type: integer
      label: 'Items per page'
    featured_bundle:
      type: string
      label: 'Featured bundle'
```

Install defaults under `config/install/acme_catalog.settings.yml`. Place dependent, conditionally installed configuration under `config/optional/`.

Read editable config through `getEditable()` only when saving. Read normal config through the injected config factory:

```php
$limit = (int) $this->configFactory
  ->get('acme_catalog.settings')
  ->get('items_per_page');
```

Settings overrides in [`settings.php`](web/sites/default/settings.php) are runtime-only and intentionally do not write back to active configuration.

## Configuration Workflow

```bash
# Development after intentional UI/code changes
drush config:export -y
git diff -- config/sync

# Deployment
drush updatedb -y
drush config:import -y
drush cache:rebuild
```

Rules:
- Commit complete, reviewed configuration exports with the code requiring them.
- Never modify active production configuration manually and leave it unexported.
- Resolve configuration UUID, dependency, and environment differences deliberately.
- Use Config Split or a comparable governed approach only for genuinely environment-specific extension/config differences.
- Validate configuration during CI and deploy from the same artifact tested in CI.

## Recipes

Use Drupal recipes to package reusable site capabilities and configuration installation, not runtime business logic.

A recipe may define extension installation, configuration imports, strictness, and configuration actions. Keep it idempotent and composable.

```yaml
# recipes/acme_editorial/recipe.yml
name: 'Acme editorial baseline'
description: 'Installs the editorial content model and workflows.'
type: 'Site'
install:
  - node
  - media
  - content_moderation
  - workflows
config:
  strict: false
  import:
    node: '*'
    media: '*'
```

Recipe guidance:
- Keep each recipe capability-focused and dependency-explicit.
- Avoid embedding environment secrets or deployment-only settings.
- Test recipe application against a clean site and an existing compatible site.
- Keep module code as the source of behavior and recipes as the source of repeatable assembly.
- Review resulting config changes exactly as regular exported configuration.

## Content Entity vs. Config Entity

Choose a Content Entity when records are numerous, editorial, revisionable, translatable, fieldable, or access-controlled per record. Choose a Config Entity when records define deployable application behavior and must move through config synchronization.

For Content Entities, consider:
- canonical/add/edit/delete routes;
- revision and moderation requirements;
- translation and fieldability;
- ownership and access handlers;
- list builder, forms, views data, and storage schema;
- cache tags and list cache tags;
- validation constraints.

For Config Entities, define:
- immutable machine ID and human label;
- configuration prefix and entity keys;
- config export properties;
- dependencies and schema;
- collection/entity permissions;
- safe deletion behavior when referenced.

## Typed Data and Validation

Use Typed Data and field APIs instead of array-shaped assumptions. Read translated entities through the entity repository/translation context. Validate entities before persistence when input does not come from normal entity forms:

```php
$violations = $entity->validate();
if ($violations->count() > 0) {
  throw new \InvalidArgumentException((string) $violations);
}
$entity->save();
```

Use Symfony/Drupal constraints for reusable invariants. Do not enforce durable business rules only in a form validator because imports, APIs, migrations, and queue workers bypass forms.

## Revisions, Moderation, and Translation

- Enable revisions for editorial/audit requirements; do not overwrite history silently.
- Use Content Moderation workflows rather than custom status flags for editorial lifecycle.
- Resolve translations from context; do not assume the default language is display-correct.
- Include language and moderation/access dimensions in cache contexts/tags as appropriate.
- Preserve revision metadata and ownership during migrations.

## Configuration and Data Updates

Use:
- `hook_update_N()` for database schema and update-path essentials;
- `hook_post_update_NAME()` for fully bootstrapped entity/config transformations;
- deploy hooks only for site-specific deployment operations when the project has a governed deploy-hook convention;
- migrations for repeatable source-to-destination content imports.

Requirements:
- Make updates restart-safe and bounded with `$sandbox` for large datasets.
- Never call arbitrary external APIs in a blocking update hook.
- Do not assume all records fit in memory.
- Do not re-save every entity merely to trigger hooks unless explicitly required and tested.
- Test the supported upgrade path from the oldest maintained release snapshot.

## Configuration/Entity Checklist

```text
□ Data classified as config/content/state/temp/secret before implementation
□ Every custom config object has a config schema
□ Install vs optional config placement is intentional
□ Exports contain no secrets, hostnames, or environment-only values
□ Entity type matches record semantics (content vs config)
□ Entity access, revisions, translation, validation, and cache tags are designed
□ Recipe is composable, idempotent, and free of runtime business logic
□ Update/post-update paths are restart-safe and tested at production scale
□ CI reviews and validates the full configuration diff
```
