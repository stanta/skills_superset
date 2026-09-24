# Drupal 11 Best Practices Skill

Reusable guidance for architecting, developing, reviewing, testing, securing, optimizing, and operating modern Drupal 11 applications.

## Why a Separate Drupal 11 Skill

The workspace is currently a restored Drupal 7 project, and the existing [`drupal-7-best-practices/SKILL.md`](../drupal-7-best-practices/SKILL.md) correctly targets procedural hooks, `.info` files, PHPTemplate, Features, and Drush 8. Drupal 11 is a different architecture: Composer-managed Symfony components, namespaced services, dependency injection, attributes/plugins, YAML configuration, Twig/Single-Directory Components, cacheability metadata, and PHPUnit test layers. Keeping separate skills prevents accidental cross-version advice.

The agency roles reviewed under `/512-2/mcps/agency-agents/engineering/` contain useful Drupal 10/11 performance and CMS material, but are role/persona-oriented and mix generic or older guidance. This package refactors the useful concepts into concise, task-oriented, Drupal 11-specific procedures.

## Package Layout

```text
drupal-11-best-practices/
├── SKILL.md
├── README.md
└── references/
    ├── architecture-development.md
    ├── configuration-recipes-entities.md
    ├── security-access-api.md
    ├── rendering-theming-performance.md
    └── testing-quality-operations.md
```

## Usage

The skill should trigger for requests such as:
- “Create a Drupal 11 module/service/plugin/form.”
- “Review this Drupal 11 controller or entity access handler.”
- “Fix stale Drupal render caching.”
- “Design a config entity or Drupal recipe.”
- “Add Unit/Kernel/Functional tests and CI quality gates.”
- “Secure or optimize JSON:API/custom endpoints.”
- “Plan Composer/Drush deployment or core upgrade.”

Read [`SKILL.md`](SKILL.md) first. Load only the relevant reference:

| Task | Reference |
|---|---|
| Services, DI, controllers, plugins, hooks, events, persistence | [`references/architecture-development.md`](references/architecture-development.md) |
| Config schemas, entities, recipes, data updates | [`references/configuration-recipes-entities.md`](references/configuration-recipes-entities.md) |
| Access, input/output safety, files, secrets, APIs | [`references/security-access-api.md`](references/security-access-api.md) |
| Render arrays, cache metadata, Twig, SDC, JS, performance | [`references/rendering-theming-performance.md`](references/rendering-theming-performance.md) |
| PHPUnit, PHPCS/PHPStan/Rector, Composer/Drush, CI/deploy/restore | [`references/testing-quality-operations.md`](references/testing-quality-operations.md) |

## Recommended Team Adoption

1. Start Drupal 11 projects from `drupal/recommended-project` with `web/` as document root.
2. Store custom modules/themes under `web/*/custom`, configuration under `config/sync`, and reusable assembly in recipes.
3. Install and configure Coder, `phpstan-drupal`, Rector, PHPUnit, YAML/Twig/JS linting, and Composer audit in CI.
4. Require route/entity/query access tests and cacheability review in pull requests.
5. Test clean install/config import and upgrade from the oldest supported release snapshot.
6. Deploy immutable artifacts generated from the committed lockfile and monitor queues, cron, errors, cache hit rates, latency, and Core Web Vitals.

## Evidence Sources

Only GitHub repositories meeting the requested threshold of at least five stars or forks were used as repository sources. Counts were checked through GitHub on 12 September 2026.

| Repository | Stars | Forks | Use |
|---|---:|---:|---|
| [`drupal/drupal`](https://github.com/drupal/drupal) | 4282 | 1983 | Canonical Drupal 11 APIs, tests, cache/access semantics |
| [`drupal/recommended-project`](https://github.com/drupal/recommended-project) | 152 | 159 | Official Composer project structure |
| [`pfrenssen/coder`](https://github.com/pfrenssen/coder) | 30 | 52 | Drupal/DrupalPractice PHPCS standards |
| [`mglaman/phpstan-drupal`](https://github.com/mglaman/phpstan-drupal) | 208 | 86 | Drupal-aware PHPStan static analysis |
| [`palantirnet/drupal-rector`](https://github.com/palantirnet/drupal-rector) | 160 | 76 | Automated modernization/deprecation remediation |
| [`drevops/vortex`](https://github.com/drevops/vortex) | 133 | 29 | CI, code-quality, testing, and deployment reference architecture |
| [`platformsh-templates/drupal11`](https://github.com/platformsh-templates/drupal11) | 4 | 8 | Drupal 11 cloud template and operations patterns |
| [`theodorosploumis/drupal-best-practices`](https://github.com/theodorosploumis/drupal-best-practices) | 34 | 12 | Supplemental review and site-building practices |

Current Drupal API details were cross-checked against the Context7 snapshot for [`drupal/drupal` 11.2.2](https://github.com/drupal/drupal/tree/11.2.2), including configuration override precedence, update/post-update hooks, render cache semantics, access-result cacheability, entity-query access checking, and the core development test toolchain. Before implementing in a live project, verify APIs against that project's exact current core version and release notes.

## Boundaries

- Use [`../drupal-7-best-practices/SKILL.md`](../drupal-7-best-practices/SKILL.md) for Drupal 7 maintenance/recovery.
- Use this skill for Drupal 11 application engineering and operations.
- Use a dedicated migration plan/skill when the primary task is a Drupal 7 → Drupal 11 content/code migration; apply both version-specific skills at their respective source/destination boundaries.
