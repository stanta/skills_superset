# Privacy, Sampling, and Noise Control

## Privacy baseline

Assume an error event can contain more than the explicit exception:

- HTTP headers;
- cookies;
- request URL and query parameters;
- local variables;
- breadcrumbs;
- user context;
- device/browser metadata;
- SQL or HTTP spans;
- log attributes.

Minimize at the source before relying on backend scrubbing.

Never send:

- passwords;
- bearer tokens;
- session cookies;
- private keys or seed phrases;
- signing material;
- payment-card data;
- raw KYC documents;
- secret API parameters;
- full Telegram init data or other signed authentication payloads;
- sensitive request/response bodies unless explicitly approved.

## SDK controls

Keep default PII collection disabled unless a reviewed requirement says otherwise.

Use `beforeSend` / `before_send` or equivalent event processors to remove application-specific sensitive fields.

Example shape:

```ts
Sentry.init({
  // ...
  sendDefaultPii: false,
  beforeSend(event) {
    if (event.request?.headers) {
      delete event.request.headers.Authorization;
      delete event.request.headers.Cookie;
    }

    if (event.request) {
      delete event.request.data;
    }

    return event;
  },
});
```

Do not mutate only one representation of a secret while leaving it in breadcrumbs, tags, contexts, query strings, or exception messages.

## Sentry server-side scrubbing

Sentry supports project/organization data scrubbing, additional sensitive field names, advanced rules, and IP-address scrubbing.

Use both layers:

1. SDK-side minimization before egress.
2. Backend scrubbing as defense in depth.

Treat server-side rules as non-retroactive for events already stored.

## GlitchTip privacy posture

Because GlitchTip accepts Sentry-compatible events, prefer the same SDK-side minimization pattern.

For hosted or self-hosted GlitchTip, decide retention, storage location, backups, and user access based on the actual data category being ingested.

Do not assume self-hosting eliminates privacy obligations.

## Filter before sampling

Use deterministic filters for known non-actionable noise:

- health checks;
- load balancer disconnects;
- expected client cancellations;
- browser extensions;
- unsupported old clients if intentionally out of support;
- bots/crawlers;
- expected authorization failures;
- intentionally retried transient errors already represented by a final failure metric.

Do not filter a class until the team can explain why it is non-actionable.

## Error sampling

Start by capturing all actionable errors.

Only introduce error-event sampling after:

- high-volume issues are understood;
- deterministic filters are in place;
- the team has enough data to preserve severe and rare failures.

If the SDK supports a sampler callback, retain:

- uncaught/fatal errors;
- payment or checkout failures;
- security-sensitive failures;
- low-frequency regressions;
- errors in a newly deployed release.

Sample repetitive known issues more aggressively if every instance adds little information.

## Performance sampling

Performance events can dominate cost and storage.

GlitchTip currently recommends low production trace rates and notes that 1–10% is sufficient for many teams. A common starting point is 1%, then adjust from measured request volume and debugging needs.

Do not copy the same sample rate to every service.

Prefer a trace sampler when traffic mixes:

- health/static endpoints -> 0% or near 0%;
- normal high-volume API -> low rate;
- checkout/payment/auth critical path -> higher rate;
- new release/canary -> temporarily higher rate;
- rare background job -> high or 100% if volume is low.

Illustrative TypeScript pattern:

```ts
Sentry.init({
  // ...
  tracesSampler(ctx) {
    const name = ctx.name ?? "";

    if (name.includes("/health")) return 0;
    if (name.includes("/checkout")) return 0.25;
    return 0.01;
  },
});
```

Verify the current SDK callback signature before copying framework-specific code.

## Cardinality control

High-cardinality tags and transaction names make searches slower and dashboards less useful.

Avoid tags containing:

- UUIDs;
- raw URLs;
- transaction hashes;
- user-generated strings;
- wallet addresses;
- email addresses.

Put high-cardinality values in structured context only when necessary and privacy-safe.

Normalize route names at instrumentation time.

## Event-budget review

Review at least:

- errors received;
- transactions received;
- logs received;
- dropped by sample rate;
- dropped by before-send/event processor;
- rate-limited events;
- noisy issue groups;
- top projects by volume;
- top transaction names by volume.

Sentry exposes dropped-event reasons such as sample rate, before-send, event processor, rate limit, and queue overflow. Use these signals to detect an SDK that silently loses useful telemetry.

For self-hosted GlitchTip, also review PostgreSQL size, object/file storage, hot/cold retention, and worker backlog.

## Privacy verification

Before production:

1. Generate a synthetic request containing fake secrets in every risky location.
2. Trigger a controlled error.
3. Inspect the raw event if the product permits it.
4. Confirm secrets are absent from headers, cookies, breadcrumbs, request data, tags, contexts, logs, and stack-local variables.
5. Document the test in CI or a security runbook.

## Sources

- https://docs.sentry.io/api/projects/update-a-project/
- https://docs.sentry.io/api/organizations/update-an-organization/
- https://docs.sentry.io/product/stats/
- https://glitchtip.com/sdkdocs/all-sdks/
- https://glitchtip.com/documentation/performance/
- https://glitchtip.com/documentation/frequently-asked-questions/
