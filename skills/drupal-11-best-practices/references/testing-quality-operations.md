# Drupal 11 Testing, Quality Gates, Composer, and Operations

## Choose the Cheapest Sufficient Test Layer

| Layer | Base/tool | Use for |
|---|---|---|
| Unit | PHPUnit + mocks/stubs | Pure services, value objects, algorithms, no Drupal container |
| Kernel | `KernelTestBase` | Services, plugins, entities, schema, config, database integration |
| Functional | `BrowserTestBase` | Routes, forms, permissions, HTTP output, cache headers |
| Functional JS | `WebDriverTestBase`/FunctionalJavascript | AJAX, behaviors, dialogs, real browser interactions |
| E2E/smoke | Playwright/Behat/site tool | Critical user journeys across the deployed stack |

Add a failing regression test before fixing a defect. Do not use a browser test when a unit/kernel test proves the same contract.

## PHPUnit Examples

```php
final class PriceCalculatorTest extends UnitTestCase {

  /** @dataProvider cases */
  public function testCalculate(string $input, string $expected): void {
    self::assertSame($expected, (new PriceCalculator())->calculate($input));
  }

}
```

```php
final class CatalogStorageTest extends KernelTestBase {
  protected static $modules = ['system', 'user', 'field', 'node', 'acme_catalog'];

  protected function setUp(): void {
    parent::setUp();
    $this->installEntitySchema('user');
    $this->installEntitySchema('node');
    $this->installSchema('system', ['sequences']);
    $this->installConfig(['acme_catalog']);
  }
}
```

```php
final class CatalogAccessTest extends BrowserTestBase {
  protected static $modules = ['node', 'acme_catalog'];
  protected $defaultTheme = 'stark';

  public function testDeniedWithoutPermission(): void {
    $this->drupalGet('/admin/reports/catalog');
    $this->assertSession()->statusCodeEquals(403);
  }
}
```

Test stable semantic identifiers and outcomes, not brittle DOM structure. Cover denied-access and cache/invalidation behavior—not only the happy path.

## Required Quality Toolchain

Install project-compatible versions through Composer:

```bash
composer require --dev drupal/core-dev drupal/coder mglaman/phpstan-drupal palantirnet/drupal-rector
```

Typical gates:

```bash
vendor/bin/phpcs --standard=Drupal,DrupalPractice web/modules/custom web/themes/custom
vendor/bin/phpstan analyse web/modules/custom web/themes/custom
vendor/bin/phpunit -c web/core/phpunit.xml.dist web/modules/custom
composer validate --strict
composer audit
```

Use Rector/Upgrade Status for controlled modernization and deprecation discovery. Review every automated change; do not mass-apply refactors without tests.

## Static Analysis and Type Discipline

- Enable PHPStan Drupal extensions and increase the level progressively; baseline only existing debt, never new findings.
- Add array-shape/generic docblocks where Drupal APIs return broad arrays.
- Use strict types in class files where project policy supports it.
- Avoid suppressions; scope unavoidable ignores to a rule/path with a reason and removal issue.
- Treat deprecation warnings as release-blocking before the next core major/minor removes the API.

## Composer Discipline

- Use `drupal/recommended-project` and `drupal/core-recommended` for tested dependency constraints.
- Commit [`composer.lock`](composer.lock); build production with `composer install --no-dev --prefer-dist --optimize-autoloader`.
- Require/remove packages through Composer; never copy contrib code manually.
- Configure `composer/installers`/scaffold through project templates, not ad hoc scripts.
- Keep patches declared, checksummed where supported, linked to upstream issues, and covered by tests.
- Run `composer audit` and review abandoned packages in CI.
- Update deliberately: change constraints/lockfile in a branch, run the full suite, deploy the identical artifact.

## Drush Operations

```bash
drush status
drush updatedb:status
drush config:status
drush updatedb -y
drush config:import -y
drush cache:rebuild
drush cron
drush queue:run QUEUE_NAME
drush state:get system.maintenance_mode
drush watchdog:show --severity=Error --count=50
```

Avoid commands that mutate production outside the deployment process. Export intentional configuration changes from development and review them in Git.

## CI Pipeline Order

1. Validate Composer metadata/lockfile and install dependencies.
2. Lint YAML/Twig/JS/CSS and run PHPCS.
3. Run PHPStan and deprecation checks.
4. Run unit then kernel tests.
5. Install a clean site, import configuration/apply recipes, and run functional/JS tests.
6. Build the immutable production artifact.
7. Scan dependencies/container/secrets.
8. Deploy to staging and run smoke/access/cache tests.

Parallelize independent gates, but never allow later green stages to hide an earlier failed gate.

## Deployment Runbook

Preconditions:
- tested immutable artifact from committed `composer.lock`;
- verified DB/files backup and restore procedure;
- compatible update/config path tested against a production-like snapshot;
- maintenance/traffic-drain and rollback decisions documented.

Recommended sequence:

```bash
# Deploy artifact / release directory first.
drush state:set system.maintenance_mode 1 --input-format=integer
# Drain or pause queue workers if schema/config changes require it.
drush updatedb -y
drush config:import -y
drush cache:rebuild
drush cron
# Run application-specific queue/smoke checks.
drush state:set system.maintenance_mode 0 --input-format=integer
drush cache:rebuild
```

Ordering may differ for zero-downtime blue/green deployments; test compatibility between old/new code and schema. Do not claim rollback is possible if updates destructively transform data without a restore plan.

## Observability and Reliability

Instrument and monitor:
- HTTP rate, errors, p50/p95/p99 latency;
- PHP exceptions and watchdog/syslog events;
- queue depth, age, retries, poison messages, and worker heartbeat;
- cron completion and duration;
- DB latency/locks/slow queries;
- cache hit/miss and Redis/Memcache health;
- external dependency latency/errors;
- deployment version and post-release regressions;
- Core Web Vitals for key templates.

Log structured operational context but never secrets, access tokens, full sensitive payloads, or unnecessary personal data. Use correlation/request IDs across ingress, queue, and external calls.

## Backups and Recovery

A recoverable Drupal 11 system needs:
- Git/immutable code artifact + [`composer.lock`](composer.lock);
- database backups with tested point-in-time recovery;
- public/private files or object-storage versioning;
- environment/secret recovery procedure;
- exported configuration/recipes;
- documented RPO/RTO and practiced restore runbook.

Verify backups by restoring them. A successful backup job without a tested restore is not evidence of recoverability.

## Update and Upgrade Discipline

- Subscribe to Drupal security advisories and define patch SLAs by severity.
- Before core/contrib updates, read release notes, API changes, and known issues.
- Run Upgrade Status, PHPStan, Rector dry-runs, PHPUnit, and config diff review.
- Test updates from the oldest supported current application release.
- Remove deprecated APIs before upgrading the core version that deletes them.
- Keep core/contrib customizations out of source so upgrades remain repeatable.

## Definition of Done

```text
□ Regression test demonstrates the requested behavior/fix
□ PHPCS Drupal + DrupalPractice passes
□ PHPStan passes with no new baseline debt
□ Unit/kernel/functional/JS layers used appropriately
□ Composer validate/audit and deprecation checks pass
□ Clean install/config import/recipe application succeeds
□ Update hooks tested on a production-like snapshot
□ Deployment, rollback, queue, cron, and smoke steps documented
□ Monitoring and alerting cover the new failure modes
□ Backups and restore procedure remain valid
```
