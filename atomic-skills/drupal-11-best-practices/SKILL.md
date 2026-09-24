---
name: drupal-11-best-practices
description: This skill should be used when architecting, developing, reviewing, testing, securing, optimizing, deploying, upgrading, or maintaining Drupal 11 applications, custom modules, themes, recipes, APIs, and Composer projects. It covers Drupal 11-specific service and dependency-injection patterns, plugins and attributes, entities and Typed Data, configuration schemas and recipes, render arrays and cacheability metadata, Twig and Single-Directory Components, access control and secure coding, PHPUnit test layers, PHPStan/PHPCS/Rector quality gates, Composer/Drush operations, observability, deployment, and upgrade discipline. Do not use it for Drupal 7 procedural APIs or PHPTemplate sites.
metadata:
  category: development
  source:
    - repository: https://github.com/drupal/drupal
      path: 11.x
    - repository: https://github.com/drupal/recommended-project
      path: 11.x
    - repository: https://github.com/pfrenssen/coder
    - repository: https://github.com/mglaman/phpstan-drupal
    - repository: https://github.com/palantirnet/drupal-rector
    - repository: https://github.com/drevops/vortex
---

# Drupal 11 Development and Operations Best Practices

Build Drupal 11 code as a modern, Composer-managed Symfony application while preserving Drupal-native extension points, cacheability, configuration semantics, access control, and upgradeability. Prefer small services, typed contracts, plugins, events, and render arrays over static service location, procedural orchestration, raw HTML, direct database access, or core/contrib modification.

## Establish the Correct Context

1. Confirm the exact Drupal core, PHP, database, Drush, Composer, and contributed-project versions before proposing syntax or dependencies.
2. Treat Drupal 11 as distinct from Drupal 7: use YAML metadata, namespaced classes, services, attributes/plugins, Twig, configuration management, and PHPUnit—not `.info`, `hook_menu()`, PHPTemplate, or SimpleTest.
3. Use Composer as the only dependency and scaffold authority. Keep the web root separate through `drupal/recommended-project`; commit `composer.json` and `composer.lock`, not `vendor/` or generated scaffold drift.
4. Prefer dependency injection. Reserve the global `\Drupal::*()` service locator for `.module` hooks and narrow glue code where injection is unavailable.
5. Preserve cacheability metadata and access-result metadata through every render, entity, API, and authorization path.

## Non-Negotiable Rules

1. **Never modify core or contrib directly.** Implement extension points, patches managed by Composer, or a custom module/theme; document every patch and remove it when upstream resolves the issue.
2. **Define explicit compatibility.** Declare `core_version_requirement: ^11` (or a deliberately tested range) and constrain dependencies in Composer.
3. **Inject services through constructors and `create()` factories.** Depend on interfaces where available; keep controllers/forms/plugins thin and business rules in testable services.
4. **Require explicit entity query access behavior.** Call `accessCheck(TRUE)` for user-facing queries. Use `accessCheck(FALSE)` only for privileged internal work after documenting and testing the authorization boundary.
5. **Return render arrays with complete cache metadata.** Attach dependencies via `CacheableMetadata`; define correct tags, contexts, and max-age. Never fix stale output by setting an entire page to `max-age: 0`.
6. **Enforce access at the operation boundary.** Use route requirements, entity access handlers, permissions, field access, and `AccessResult`; bubble the access result's cacheability.
7. **Trust Twig auto-escaping and safe render APIs.** Avoid `|raw`; validate input, use placeholders for database queries, validate destinations/URIs, and protect state-changing routes/forms with CSRF controls.
8. **Separate configuration, state, content, and secrets.** Export deployable configuration; use State API for environment-local runtime state; use environment/settings overrides or secret managers for credentials; provide config schemas.
9. **Ship schema/config/data changes through update APIs.** Use `hook_update_N()` for required update-time changes and `hook_post_update_NAME()` for post-update entity/config operations; make long work sandboxed and restart-safe.
10. **Test at the cheapest sufficient layer.** Unit-test pure logic, Kernel-test Drupal integration, Functional-test HTTP/forms/access, and FunctionalJavascript-test actual browser behavior. Add regression tests before fixing defects.
11. **Gate every merge.** Run PHPCS (`Drupal` + `DrupalPractice`), PHPStan with `phpstan-drupal`, PHPUnit, deprecation checks, configuration validation, and targeted browser tests.
12. **Deploy immutable code and synchronized configuration.** Back up, deploy the locked artifact, run database updates, import configuration, rebuild caches, run cron/queues, and execute smoke tests; define rollback before changing production.

## Working Process

### 1. Discover and Bound the Change

- Inspect [`composer.json`](composer.json), [`composer.lock`](composer.lock), active extensions, configuration sync path, environment overrides, and custom code boundaries.
- Identify the owning entity type, plugin manager, service, event, route, form, or theme hook before introducing a new abstraction.
- Search Drupal 11 API/deprecation documentation and the codebase before inventing an extension point.
- Choose the smallest compatible change; record security, cacheability, configuration, data migration, and rollback implications.

### 2. Design Drupal-Natively

- Define module metadata, routes, permissions, services, libraries, config schema, and install/default config as declarative YAML.
- Put domain logic in services; use plugins for discoverable interchangeable behavior, events for decoupled reactions, and hooks for supported cross-cutting integration.
- Model content with Content Entities and deployable settings with Config Entities; avoid custom tables unless the entity/storage model genuinely does not fit.
- Read [`references/architecture-development.md`](references/architecture-development.md) for patterns and examples.

### 3. Implement Secure, Cache-Correct Output and APIs

- Return render arrays or cacheable responses; add entity/config/list dependencies.
- Check entity/field/route access using the actual account and retain `AccessResult` cache contexts/tags.
- Prefer core JSON:API for standard entity APIs; introduce custom routes only when the contract differs materially.
- Read [`references/security-access-api.md`](references/security-access-api.md) and [`references/rendering-theming-performance.md`](references/rendering-theming-performance.md).

### 4. Manage Configuration and Data Evolution

- Add config schema for every custom config object; distinguish install config from optional config.
- Export and review configuration diffs; split/ignore environment-specific configuration deliberately rather than editing production.
- Use recipes for reusable installation/configuration packages; keep custom business logic in modules.
- Read [`references/configuration-recipes-entities.md`](references/configuration-recipes-entities.md).

### 5. Verify and Release

- Add tests at the correct layer and run static analysis/coding standards before broad integration tests.
- Verify anonymous, authenticated, privileged, denied-access, multilingual, cache-hit, invalidation, and failure paths.
- Deploy by the runbook in [`references/testing-quality-operations.md`](references/testing-quality-operations.md); measure logs, queues, cache hit rates, latency, and Core Web Vitals after release.

## Reference Loading Guide

| Reference | Load when |
|---|---|
| [`references/architecture-development.md`](references/architecture-development.md) | Creating modules, routes, controllers, forms, services, plugins, events, hooks, or custom architecture |
| [`references/configuration-recipes-entities.md`](references/configuration-recipes-entities.md) | Designing config/content entities, schemas, config deploys, recipes, update hooks, or migrations |
| [`references/security-access-api.md`](references/security-access-api.md) | Handling users, permissions, access, forms, queries, files, REST/JSON:API, serialization, or secrets |
| [`references/rendering-theming-performance.md`](references/rendering-theming-performance.md) | Building render arrays, Twig, SDC components, libraries, caching, Views, images, or performance work |
| [`references/testing-quality-operations.md`](references/testing-quality-operations.md) | Adding tests, CI gates, Composer/Drush workflows, deployments, observability, updates, or incident recovery |
| [`README.md`](README.md) | Understanding scope, sources, installation, usage examples, and adoption guidance |

## Completion Criteria

- No core/contrib edits, undocumented patches, unbounded global service location, or deprecated APIs.
- Every route/entity/query has explicit, tested access behavior.
- Every dynamic render/API response has correct cache tags, contexts, and max-age.
- Custom configuration includes schema and has a reviewed export/import path.
- Business logic is injectable and covered at the cheapest sufficient PHPUnit layer.
- PHPCS, PHPStan, PHPUnit, deprecation, config, and smoke gates pass.
- The Composer lockfile, database updates, configuration import, cache rebuild, cron/queue checks, and rollback procedure are part of deployment.
