# Drupal 11 Architecture and Custom Development

## Recommended Project Shape

Start new builds from `drupal/recommended-project`, keep the public web root in `web/`, and place custom code under `web/modules/custom` and `web/themes/custom`.

```text
project/
├── composer.json
├── composer.lock
├── config/sync/
├── recipes/
├── web/
│   ├── core/                 # Composer-managed
│   ├── modules/contrib/      # Composer-managed
│   ├── modules/custom/
│   │   └── acme_catalog/
│   ├── themes/contrib/       # Composer-managed
│   ├── themes/custom/
│   └── sites/default/
└── vendor/                   # never commit
```

Keep deployment tooling and tests outside the web root. Never place secrets in [`settings.php`](web/sites/default/settings.php) or exported configuration.

## Minimal Custom Module

```yaml
# acme_catalog.info.yml
name: 'Acme Catalog'
type: module
description: 'Provides catalog domain behavior.'
package: Custom
core_version_requirement: ^11
dependencies:
  - drupal:node
```

Use explicit module dependencies only for APIs that are actually required. Put Composer library requirements in the root [`composer.json`](composer.json), not custom module metadata.

## Routing, Controllers, and Injection

```yaml
# acme_catalog.routing.yml
acme_catalog.report:
  path: '/admin/reports/catalog'
  defaults:
    _controller: '\Drupal\acme_catalog\Controller\CatalogReportController::build'
    _title: 'Catalog report'
  requirements:
    _permission: 'access catalog report'
```

```php
<?php

declare(strict_types=1);

namespace Drupal\acme_catalog\Controller;

use Drupal\Core\Controller\ControllerBase;
use Drupal\Core\DependencyInjection\ContainerInjectionInterface;
use Drupal\acme_catalog\CatalogReportBuilderInterface;
use Symfony\Component\DependencyInjection\ContainerInterface;

final class CatalogReportController extends ControllerBase implements ContainerInjectionInterface {

  public function __construct(
    private readonly CatalogReportBuilderInterface $reportBuilder,
  ) {}

  public static function create(ContainerInterface $container): static {
    return new static($container->get('acme_catalog.report_builder'));
  }

  public function build(): array {
    return $this->reportBuilder->build();
  }

}
```

- Keep controllers as adapters: parse route input, invoke a service, return a render array/response.
- Type arguments and returns; use `final` for concrete classes not designed for extension.
- Use constructor property promotion and `readonly` where appropriate.
- Never call the container from business/domain services.

## Services and Contracts

```yaml
# acme_catalog.services.yml
services:
  Drupal\acme_catalog\CatalogReportBuilderInterface:
    alias: acme_catalog.report_builder

  acme_catalog.report_builder:
    class: Drupal\acme_catalog\CatalogReportBuilder
    arguments:
      - '@entity_type.manager'
      - '@current_user'
      - '@renderer'
```

```php
interface CatalogReportBuilderInterface {
  /**
   * Builds a cacheable report render array.
   *
   * @return array<string, mixed>
   *   A render array.
   */
  public function build(): array;
}
```

Prefer autowiring only when the project's convention supports predictable service discovery. Explicit arguments make Drupal service dependencies and overrides easier to review.

## Plugins, Attributes, and Discovery

Use a plugin when behavior is:
- selected by configuration;
- discoverable and interchangeable;
- managed by a plugin manager;
- likely to have multiple implementations.

Drupal 11 favors PHP attributes for many plugin types:

```php
use Drupal\Core\Block\Attribute\Block;
use Drupal\Core\Block\BlockBase;
use Drupal\Core\StringTranslation\TranslatableMarkup;

#[Block(
  id: 'acme_catalog_summary',
  admin_label: new TranslatableMarkup('Catalog summary'),
)]
final class CatalogSummaryBlock extends BlockBase {

  public function build(): array {
    return [
      '#theme' => 'acme_catalog_summary',
      '#cache' => [
        'tags' => ['node_list:product'],
        'contexts' => ['user.permissions'],
      ],
    ];
  }

}
```

Inject dependencies into container-aware plugins using the relevant factory interface (for example, `ContainerFactoryPluginInterface`). Do not use `\Drupal::service()` inside plugin methods.

## Hooks, Events, and Subscribers

Use hooks for Drupal-owned extension points and events for decoupled application interactions.

```php
/**
 * Implements hook_entity_presave().
 */
function acme_catalog_entity_presave(\Drupal\Core\Entity\EntityInterface $entity): void {
  if ($entity->getEntityTypeId() !== 'node' || $entity->bundle() !== 'product') {
    return;
  }
  \Drupal::service('acme_catalog.product_normalizer')->normalize($entity);
}
```

Keep hook implementations thin because procedural hooks cannot receive constructor injection. Delegate immediately to a service.

```yaml
services:
  acme_catalog.subscriber:
    class: Drupal\acme_catalog\EventSubscriber\CatalogSubscriber
    tags:
      - { name: event_subscriber }
```

```php
final class CatalogSubscriber implements EventSubscriberInterface {
  public static function getSubscribedEvents(): array {
    return [KernelEvents::REQUEST => ['onRequest', 20]];
  }
}
```

Avoid subscribers for behavior already represented by entity hooks, access handlers, validation constraints, or plugins.

## Forms and Validation

- Use Form API for server-side validation, CSRF tokens, value processing, AJAX, and accessible error handling.
- Inject services into forms through `ContainerInjectionInterface`/`create()`.
- Put reusable domain validation in Symfony constraints/validators rather than form callbacks.
- Never trust client-side validation, hidden fields, or route parameters.
- Use ConfigFormBase only for editable configuration; add configuration schema.

## Data Access and Persistence

Prefer entity storage and repositories:

```php
$query = $this->entityTypeManager
  ->getStorage('node')
  ->getQuery()
  ->accessCheck(TRUE)
  ->condition('type', 'product')
  ->condition('status', 1)
  ->sort('created', 'DESC')
  ->range(0, 20);
$nids = $query->execute();
$nodes = $this->entityTypeManager->getStorage('node')->loadMultiple($nids);
```

- State explicitly whether access checking is enabled.
- Batch-load entities; avoid N+1 loads in loops.
- Use the Database API only for data that does not fit entities or for measured, justified query paths.
- Use transactions for multi-write invariants; make queue workers idempotent.
- Do not load/write entities from Twig.

## Custom Tables and Update Discipline

Define custom tables with `hook_schema()` only when entities/key-value/state do not fit. Add database changes with `hook_update_N()`. Use `hook_post_update_NAME()` for entity/config operations requiring a fully bootstrapped system.

```php
function acme_catalog_update_11001(array &$sandbox): void {
  if (!\Drupal::database()->schema()->fieldExists('acme_item', 'external_id')) {
    \Drupal::database()->schema()->addField('acme_item', 'external_id', [
      'type' => 'varchar',
      'length' => 128,
      'not null' => FALSE,
    ]);
  }
}
```

Never re-edit an update hook once released. Add a new update number instead.

## Architecture Review Checklist

```text
□ Business logic lives in injectable services, not controllers/forms/hooks
□ Services depend on interfaces where useful and have narrow responsibilities
□ Plugins represent configurable interchangeable behavior
□ Entity queries declare accessCheck(TRUE/FALSE) explicitly
□ No core/contrib edits or untracked patches
□ No direct static service location outside unavoidable glue code
□ No unbounded entity loads or writes inside render/preprocess loops
□ Update hooks are append-only, restart-safe, and covered by deployment tests
□ Public APIs and extension points have docblocks and stable contracts
```
