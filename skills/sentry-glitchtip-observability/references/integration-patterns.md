# SDK Integration Patterns

## Project topology

Prefer one observability project per independently deployable application or service boundary when ownership, release cadence, alerting, or runtime differs materially.

Do not create separate projects only for production versus staging when the same service can be cleanly separated by the `environment` field.

Useful shared fields:

- `service`
- `environment`
- `release`
- `region`
- `route` or normalized transaction name
- `feature`
- `job_name`
- `request_id` or trace/correlation ID
- low-cardinality tenant/account class when needed

Avoid high-cardinality tags such as raw URLs containing IDs, full wallet addresses, transaction hashes, email addresses, request bodies, or unbounded user input.

## JavaScript / TypeScript baseline

Initialize the SDK before application startup and framework initialization.

Portable baseline:

```ts
import * as Sentry from "@sentry/node";

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.APP_ENV ?? "development",
  release: process.env.APP_RELEASE,
  tracesSampleRate: Number(process.env.SENTRY_TRACES_SAMPLE_RATE ?? "0.01"),
  sendDefaultPii: false,
});
```

For GlitchTip, use the GlitchTip DSN and disable session tracking when supported by that SDK:

```ts
Sentry.init({
  dsn: process.env.GLITCHTIP_DSN,
  environment: process.env.APP_ENV ?? "development",
  release: process.env.APP_RELEASE,
  tracesSampleRate: 0.01,
  autoSessionTracking: false,
  sendDefaultPii: false,
});
```

Framework-specific SDK versions can require initialization in a dedicated preload/instrumentation file. Follow the current framework guide rather than moving initialization later for convenience.

## Python baseline

```python
import os
import sentry_sdk

sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN"),
    environment=os.environ.get("APP_ENV", "development"),
    release=os.environ.get("APP_RELEASE"),
    traces_sample_rate=float(os.environ.get("SENTRY_TRACES_SAMPLE_RATE", "0.01")),
    send_default_pii=False,
)
```

For GlitchTip:

```python
sentry_sdk.init(
    dsn=os.environ["GLITCHTIP_DSN"],
    environment=os.environ.get("APP_ENV", "development"),
    release=os.environ.get("APP_RELEASE"),
    traces_sample_rate=0.01,
    auto_session_tracking=False,
    send_default_pii=False,
)
```

## Capture policy

Prefer automatic framework capture for unhandled exceptions.

Manually capture only when:

- the exception is handled and will not otherwise reach the framework handler;
- the failure is operationally relevant despite graceful recovery;
- extra context materially improves diagnosis.

Bad:

```ts
try {
  await charge();
} catch (err) {
  Sentry.captureException(err);
  throw err; // framework will capture it again
}
```

Better:

```ts
try {
  await charge();
} catch (err) {
  addDomainContext(err);
  throw err;
}
```

Or, when the exception is intentionally handled:

```ts
try {
  await optionalAnalyticsSync();
} catch (err) {
  Sentry.captureException(err, {
    tags: { subsystem: "analytics-sync" },
  });
}
```

## Context and users

Add context that helps answer:

- which release introduced the error;
- which route/job/feature failed;
- whether the failure is isolated or systemic;
- which dependency/provider was involved;
- whether the user-visible result failed.

Use stable, privacy-safe user identifiers only when needed:

```ts
Sentry.setUser({ id: internalPseudonymousId });
```

Do not attach email, phone, Telegram auth payloads, wallet seed phrases, private keys, raw payment metadata, or KYC data unless there is an explicit legal and operational need plus documented controls.

## Breadcrumbs

Breadcrumbs should explain the path to failure without reproducing sensitive payloads.

Good breadcrumb categories:

- route transition;
- state-machine transition;
- external API call class;
- feature flag evaluation;
- queue/job transition;
- payment state transition using internal IDs or redacted references.

Avoid recording complete request/response bodies.

## Distributed tracing

Enable tracing only across services that can preserve and trust trace headers.

In browser SDKs, explicitly constrain `tracePropagationTargets` for cross-origin calls.

Example:

```ts
Sentry.init({
  // ...
  tracePropagationTargets: [
    /^https:\/\/api\.example\.com\//,
    /^https:\/\/payments\.example\.com\//,
  ],
});
```

Do not propagate tracing headers to arbitrary third-party domains.

Normalize transaction names. Prefer:

```text
POST /orders/:orderId/pay
```

over:

```text
POST /orders/92e9b3.../pay?wallet=...
```

## Logs

Use logs as structured evidence, not as a second copy of every error event.

For GlitchTip, current documentation supports logs through Sentry SDK envelopes. Do not configure a raw OTLP HTTP log exporter directly to GlitchTip because it does not expose a raw OTLP receiver for this path.

Correlate logs with trace IDs and request IDs when the logging stack supports it.

## Short-lived jobs and serverless

Ensure pending events flush before the process exits. Exact APIs differ by SDK.

Typical patterns:

- Node: `await Sentry.flush(timeoutMs)`
- Python/serverless: use the framework integration or SDK flush behavior
- Go: `defer sentry.Flush(...)`
- Java: call `Sentry.flush(...)` before exit when necessary

Do not add blocking flush calls to every long-running web request.

## Verification endpoint

A test endpoint can be useful in staging:

```ts
app.get("/__debug/observability", (_req, _res) => {
  throw new Error("observability-integration-test");
});
```

Protect or remove it in production. Prefer a controlled deployment verification job over a publicly reachable permanent crash endpoint.

## Sources

- https://docs.sentry.io/
- https://glitchtip.com/sdkdocs/all-sdks/
- https://glitchtip.com/sdkdocs/javascript/
- https://glitchtip.com/sdkdocs/node/
- https://glitchtip.com/sdkdocs/python/
- https://glitchtip.com/documentation/logs/
