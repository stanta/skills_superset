# Drupal 7 Performance & Caching

Drupal 7 performance is layered. Profile first (`devel` query log, XHProf/Tideways), fix the actual bottleneck, and prove it with before/after numbers — never "optimize" on a hunch.

## 1. The cache layers

| Layer | What it caches | Who it serves |
|---|---|---|
| `cache_bootstrap` | System/menu/router bootstrap data | everyone |
| `cache_page` | Full rendered HTML pages | anonymous users |
| `cache_block` | Individual block output | everyone (per block `cache` setting) |
| `cache_field`, `cache_menu`, `cache_views` | subsystem-specific | subsystem |
| Render `#cache` | Render arrays | the render pipeline |
| Views cache | View query/result/output | the View |

### Core cache API

```php
// Set
cache_set($cid, $data, 'cache', CACHE_TEMPORARY); // or CACHE_PERMANENT

// Get
if ($cache = cache_get($cid, 'cache')) {
  $data = $cache->data;
}

// Invalidate (clears by cid prefix)
cache_clear_all('my_module:', 'cache', TRUE);
```

- `CACHE_TEMPORARY` (~6h, default) vs `CACHE_PERMANENT`.
- `$cid` should include every variable the value depends on (nid, uid, langcode, etc.).
- `cache_clear_all($cid, 'cache', TRUE)` with `$wildcard = TRUE` treats `$cid` as a prefix.

## 2. Static caching with `drupal_static()`

For per-request memoization of expensive lookups:

```php
function my_module_expensive_list() {
  $list = &drupal_static(__FUNCTION__);
  if (!isset($list)) {
    $list = my_module_really_expensive_query();
  }
  return $list;
}

// In tests / after mutations:
drupal_static_reset('my_module_expensive_list');
```

This avoids re-running the same query many times within one request.

## 3. Render array caching

```php
$build['#cache'] = array(
  'keys' => array('my_module', 'report', $node->nid),
  'bin' => 'cache',
  'expire' => CACHE_TEMPORARY,
  'granularity' => DRUPAL_CACHE_PER_PAGE | DRUPAL_CACHE_PER_ROLE,
);
```

The render cache invalidates automatically on `cache_clear_all()`; include the entity id in the keys so saving that entity bumps the cache.

## 4. Block caching

In `hook_block_info()`, set the `cache` key:

| Constant | Meaning |
|---|---|
| `DRUPAL_CACHE_GLOBAL` | Cache once for everyone (default) |
| `DRUPAL_CACHE_PER_ROLE` | Cache per role |
| `DRUPAL_CACHE_PER_USER` | Cache per user |
| `DRUPAL_CACHE_PER_PAGE` | Cache per page path |
| `DRUPAL_NO_CACHE` | Never cache (only if truly dynamic) |

Use the most permissive cache level that is still correct. `DRUPAL_NO_CACHE` on a homepage block is a common self-inflicted slowdown.

## 5. Views optimization

- Enable **Views caching** (time-based or, better, tag-based) on expensive views.
- Add a **pager or a limit** — an unbounded view is an outage waiting to happen.
- Select only the fields you need; use **raw/field rendering** for lists, not full rendered entities.
- Use **aggregation/count** queries instead of loading entities to count them.
- Add **contextual filters** that are indexed.
- Enable the `Views UI` "Query performance" warnings and fix the "no index" findings.

## 6. Database query tuning

- Index every `field_*` value column used in a filter/sort (Drupal field tables have `value`, `tid`, `fid`, etc.).
- Read `EXPLAIN` on slow queries (`db_query('EXPLAIN ...')` in `devel` or via the DB log).
- Eliminate N+1: load entities in bulk with `node_load_multiple()` rather than one-per-row.
- Bound every result set with `->range()` or a pager.

## 7. Front-end delivery (CSS/JS aggregation & images)

- Enable **CSS and JS aggregation** at `/admin/config/development/performance` (Drupal 7 has built-in aggregation; the **Advanced CSS/JS Aggregation** (`advagg`) module can improve it further but is **not** currently enabled on this site — its `cache_advagg*` tables are orphaned).
- Use **image styles** (`image_style_url()`) instead of outputting originals; set explicit dimensions to avoid layout shift.
- Lazy-load below-the-fold images; preload the LCP image.
- Defer non-critical JS where the theme supports it without breaking functionality.

## 8. Backends & infrastructure

- Front the cache bins with **Memcache** (`memcache` module) or **Redis** (`redis` module) instead of the DB cache.
- Ensure **opcache** is on and sized to the codebase in production.
- Put **Varnish/Cloudflare/nginx** in front and honor `Cache-Control` headers emitted by `drupal_add_http_header()`.

## 9. Profile-first workflow

1. Enable `devel` + `devel`'s query log (dev only) — find the slowest queries.
2. XHProf/Tideways the hot pages — find the render bottleneck.
3. Check `admin/reports/status` and `admin/reports/dblog` for slow-path warnings.
4. Fix the top cause, then **re-measure before/after**.
5. Never disable a cache to fix stale content — fix the cache key/invalidation instead.

## Quick checklist

```
□ cache_page + block caching enabled; no unjustified DRUPAL_NO_CACHE
□ drupal_static() around repeated per-request lookups
□ Expensive render arrays return #cache with entity-aware keys
□ Views: pagers/limits + caching + indexed filters
□ Slow field_* columns indexed (EXPLAIN confirmed)
□ No N+1 entity loads (node_load_multiple / bulk loads)
□ CSS/JS aggregation enabled (advagg configured); image styles used
□ Memcache/Redis backing the cache bins in production
□ Every change measured before/after
```
