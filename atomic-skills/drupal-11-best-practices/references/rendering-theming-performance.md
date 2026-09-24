# Drupal 11 Rendering, Theming, Cacheability, and Performance

## Render Arrays First

Return render arrays from controllers, blocks, preprocess helpers, and services that produce presentation data. Render only at the final boundary.

```php
$build = [
  '#theme' => 'acme_catalog_card',
  '#product' => $product,
  '#attached' => [
    'library' => ['acme_catalog/card'],
  ],
  '#cache' => [
    'tags' => $product->getCacheTags(),
    'contexts' => ['languages:language_interface', 'user.permissions'],
    'max-age' => Cache::PERMANENT,
  ],
];
```

Use `CacheableMetadata` to combine dependencies instead of manually guessing metadata:

```php
$metadata = CacheableMetadata::createFromObject($product)
  ->addCacheContexts(['user.permissions']);
$metadata->applyTo($build);
```

## Cacheability Semantics

Cache metadata answers three questions:
- **tags**: which dependencies invalidate this output?
- **contexts**: by which request dimensions does output vary?
- **max-age**: how long may it live absent invalidation?

Rules:
- Add every entity/config/list dependency that influenced output.
- Use the narrowest valid context; `user` is much more expensive than `user.roles` or `user.permissions`.
- Prefer permanent max-age plus precise tags. Use finite TTL only for genuinely time-bound/external data.
- `max-age: 0` propagates upward and makes the containing render uncacheable. Isolate truly dynamic fragments with lazy builders/placeholders/BigPipe.
- Preserve cacheability of `AccessResult`, generated URLs, and cacheable responses.

## Blocks and Lazy Builders

```php
$build['personalized'] = [
  '#lazy_builder' => ['acme_catalog.lazy_builder:build', [$product_id]],
  '#create_placeholder' => TRUE,
];
```

The lazy callback must be deterministic for its arguments, return a render array, and attach its own cache metadata. Do not pass complex objects as lazy-builder arguments.

## Twig Discipline

- Keep Twig declarative; do not query entities, call services, or encode business rules in templates.
- Prepare normalized variables in preprocess/services.
- Trust auto-escaping; avoid `|raw`.
- Render field/entity render arrays rather than reconstructing formatter logic.
- Use translation filters/functions for UI text and retain contextual translation.
- Keep template suggestions intentional and document non-obvious variants.

## Single-Directory Components (SDC)

Use SDC for cohesive, reusable UI components with explicit props/slots and co-located Twig/CSS/JS metadata.

```text
components/card/
├── card.component.yml
├── card.twig
├── card.css
└── card.js
```

```yaml
# card.component.yml
name: Card
status: stable
props:
  type: object
  required: [title, url]
  properties:
    title:
      type: string
    url:
      type: string
slots:
  body:
    title: Body
```

Guidance:
- Define strict, minimal prop schemas and named slots.
- Keep Drupal entity objects out of component contracts where practical; map to presentation values/render arrays.
- Make components accessible by default and test keyboard/focus/error states.
- Avoid duplicated component assets and global selectors.

## Libraries and JavaScript Behaviors

```yaml
# acme_catalog.libraries.yml
card:
  css:
    component:
      components/card/card.css: {}
  js:
    components/card/card.js: {}
  dependencies:
    - core/drupal
    - core/once
```

```javascript
(function (Drupal, once) {
  Drupal.behaviors.acmeCatalogCard = {
    attach(context) {
      once('acme-catalog-card', '.catalog-card', context).forEach((element) => {
        // Initialize once, scoped to context.
      });
    },
  };
})(Drupal, once);
```

- Attach libraries only where used.
- Use Drupal behaviors + `once()` so AJAX/BigPipe reattachments are safe.
- Avoid jQuery unless a required dependency needs it.
- Pass small non-secret values through `drupalSettings`; never expose credentials/private data.

## Views and Query Performance

- Bound every View with pagination/range.
- Cache View results/render output with correct invalidation.
- Avoid relationships that multiply rows and full entity rendering when fields suffice.
- Index fields used for high-volume filtering/sorting after measuring with `EXPLAIN`.
- Eliminate N+1 entity/reference loads.
- Use exposed-filter validation and prevent abusive broad queries.

## Image and Front-End Performance

- Use image styles/responsive image styles, `srcset`/`sizes`, explicit dimensions, and modern formats where supported.
- Never lazy-load the LCP image; lazy-load below-the-fold images.
- Attach only needed libraries; avoid sitewide bundles for component-local behavior.
- Audit third-party scripts, fonts, consent handling, and render-blocking resources.
- Set performance budgets for JS/CSS/image weight and Core Web Vitals.

## Cache/Infrastructure Layers

Use the layers together:
- render cache;
- Dynamic Page Cache;
- Internal Page Cache;
- BigPipe for personalized placeholders;
- Redis/Memcache for suitable bins/locks/sessions;
- CDN/reverse proxy for public cacheable responses and static assets;
- PHP OPcache and correctly sized PHP-FPM workers.

Never publicly cache authenticated/personalized output. Verify actual headers (`Cache-Control`, `Age`, Drupal cache diagnostics when enabled) through the CDN, not only locally.

## Performance Workflow

1. Capture baseline: p50/p95/p99 latency, query count/time, cache hit rate, memory, LCP/INP/CLS.
2. Profile with Webprofiler/Tideways/Blackfire/APM and database slow-query tools.
3. Fix the largest measured cause: cacheability, N+1, Views, I/O, asset weight, or infrastructure.
4. Re-measure the identical scenario and record the trade-off.
5. Add a regression budget/test/monitor before closing the work.

## Rendering/Performance Checklist

```text
□ Render arrays used until the final rendering boundary
□ Dependencies added through CacheableMetadata
□ Cache tags, contexts, and max-age are complete and minimal
□ No page-wide max-age: 0 for one dynamic fragment
□ Twig contains presentation only and no unsafe |raw
□ SDC contracts are explicit, accessible, and entity-decoupled
□ JS uses behaviors + once(), with libraries attached only where needed
□ Views/entity queries are bounded, indexed after measurement, and N+1-free
□ Images are responsive, dimensioned, and LCP-aware
□ CDN does not publicly cache private/session responses
□ Before/after metrics and a regression guard exist
```
