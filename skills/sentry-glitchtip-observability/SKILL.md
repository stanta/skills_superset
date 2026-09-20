---
name: sentry-glitchtip-observability
description: Integrate, configure, review, and operate Sentry or GlitchTip application observability using Sentry-compatible SDKs, including error tracking, performance tracing, logs, releases and deploys, source maps and debug symbols, sampling, privacy and PII scrubbing, alerting, ownership, cron or uptime monitoring, and self-hosted GlitchTip. Use when adding Sentry or GlitchTip to web, backend, mobile, worker, or serverless applications; debugging production errors; reducing event noise or cost; wiring release metadata into CI/CD; or operating a GlitchTip deployment.
metadata:
  category: devops
  version: "1.0.0"
  last_verified: "2026-09-20"
---

# Sentry / GlitchTip Observability

## Purpose

Make application failures diagnosable, attributable to a release, privacy-safe, and actionable.

Treat Sentry and GlitchTip as application-observability backends behind Sentry-compatible SDKs. Keep the application instrumentation portable where practical, but never assume feature parity between vendors.

## Use this skill when

- Adding Sentry or GlitchTip to frontend, backend, worker, mobile, or serverless code.
- Reviewing an existing SDK integration for correctness, noise, privacy, or cost.
- Adding release, commit, deploy, source-map, or debug-symbol metadata to CI/CD.
- Designing error and performance sampling.
- Creating alerting, issue ownership, triage, cron, heartbeat, or uptime workflows.
- Migrating from Sentry to GlitchTip or running both in different environments.
- Deploying, scaling, backing up, upgrading, or securing self-hosted GlitchTip.
- Investigating a production regression and correlating it with a deployment.

## Vendor selection

Prefer **Sentry** when the organization needs the broadest Sentry-native product surface, managed SaaS, deeper vendor integrations, or Sentry-specific workflows.

Prefer **GlitchTip** when open source, self-hosting, lower operational footprint, data residency control, or a simpler Sentry-compatible error/performance stack is the priority.

For GlitchTip:

- use supported Sentry SDKs with the GlitchTip DSN;
- set session tracking off where the SDK exposes it because GlitchTip does not support session tracking;
- do not assume Sentry-only features such as every replay, release-health, or advanced product feature are compatible;
- use GlitchTip's documented CLI and APIs for source maps, debug files, releases, uptime monitors, and operational tasks;
- use Sentry-SDK-wrapped OpenTelemetry log support rather than sending raw OTLP logs directly to GlitchTip.

## Core invariants

1. **Initialize early.** Load the SDK before application code that may fail or create framework instrumentation.
2. **Keep environments in metadata, not separate code paths.** Use stable values such as `production`, `staging`, and `development`.
3. **Set a release on every production event.** Use the same release identifier in runtime, CI, artifacts, and deployment metadata.
4. **Upload source maps or debug symbols before traffic reaches the release.** A minified stack trace without matching artifacts is an observability defect.
5. **Preserve the original exception and stack.** Capture the real error object; avoid replacing it with a string.
6. **Avoid duplicate reporting.** Do not manually capture an exception and then rethrow it into an auto-capturing framework unless duplicate events are intentionally deduplicated.
7. **Scrub before sending.** Do not send passwords, access tokens, private keys, authorization headers, payment secrets, raw personal data, or sensitive request bodies.
8. **Filter before sampling.** Drop known noise deterministically; use sampling for volume control, not as a substitute for fixing or filtering noisy errors.
9. **Sample traces deliberately.** High-volume production systems rarely need 100% performance tracing. Preserve critical transactions using a sampler when possible.
10. **Constrain distributed tracing.** Explicitly control which outbound destinations receive trace propagation headers.
11. **Tag for operations, not curiosity.** Add low-cardinality, actionable dimensions such as service, route, feature, tenant class, release, environment, job name, or payment provider.
12. **Make alerts actionable.** Every paging alert needs a clear owner, severity, user-impact condition, and runbook or remediation path.
13. **Separate ingest credentials from management credentials.** Treat API and CI auth tokens as secrets with least privilege. Do not grant broad organization access for simple source-map upload jobs.
14. **Verify end-to-end.** Test one controlled exception, one traced request, release metadata, artifacts, alerts, and any heartbeat path in a production-like environment.
15. **Keep the observability backend non-critical to the product path.** Telemetry failure must not break user requests or payment processing.

## Standard implementation workflow

1. **Map the runtime**
   - List deployable services, frontends, workers, jobs, mobile apps, and serverless functions.
   - Decide project boundaries and shared metadata conventions.
   - Identify sensitive fields and cross-service trace paths.

2. **Choose the backend and feature subset**
   - Select Sentry, hosted GlitchTip, or self-hosted GlitchTip.
   - Verify framework and SDK compatibility before implementation.
   - Document any vendor-specific feature assumptions.

3. **Install and initialize the SDK**
   - Initialize before framework startup where required.
   - Read DSN, release, and environment from deployment configuration.
   - Enable framework integrations rather than writing custom capture middleware first.

4. **Define context**
   - Add stable tags and structured context.
   - Use a pseudonymous or internal user identifier only when operationally necessary.
   - Add correlation identifiers that link errors, logs, traces, and request logs.

5. **Apply privacy and filtering**
   - Keep default PII collection off unless there is a documented need.
   - Scrub sensitive headers, cookies, bodies, query parameters, and structured context.
   - Drop health checks, expected cancellations, bot noise, browser-extension noise, and other known non-actionable events where appropriate.

6. **Configure performance tracing**
   - Start with a low production trace sample rate.
   - Use route/transaction-aware sampling for critical flows.
   - Explicitly define trace propagation targets for cross-origin browser requests.

7. **Wire releases into CI/CD**
   - Use a deterministic release value such as `service@semver` or commit SHA.
   - Associate commits when supported.
   - Inject and upload source maps or debug symbols before deploy.
   - Create deployment metadata for the correct environment.
   - Never rebuild the artifact after observability artifacts were generated.

8. **Configure operations**
   - Route new/regressed production issues to the owning team.
   - Add rate or user-impact alerts for high-value services.
   - Add heartbeat/cron monitoring for scheduled jobs.
   - Add external uptime checks for public entry points.

9. **Validate**
   - Trigger a test error.
   - Confirm stack trace readability, environment, release, tags, breadcrumbs, and trace correlation.
   - Confirm sensitive values are absent from the payload and UI.
   - Confirm alerts notify the expected destination exactly once.

10. **Operate and tune**
   - Review event volume, dropped events, sampling, noisy issues, and quota/storage use.
   - Tune alerts against actual incidents.
   - Convert recurring issue classes into tests and regression checks.

## Reference routing

| Topic | Reference | Load when |
|---|---|---|
| SDK integration patterns | `references/integration-patterns.md` | Adding SDKs, tags, users, traces, logs, workers |
| Privacy, filtering, sampling | `references/privacy-sampling-noise.md` | PII, before-send hooks, noise, quotas, trace/error sampling |
| Releases and source maps | `references/releases-sourcemaps-ci.md` | CI/CD, commits, deploys, debug IDs, source maps, symbols |
| Triage and alerting | `references/alerting-triage-operations.md` | Alerts, ownership, regressions, crons, uptime, incident workflow |
| GlitchTip self-hosting | `references/glitchtip-self-hosting.md` | Docker/Kubernetes, PostgreSQL, Valkey, retention, storage, backup, security |

## Minimum production baseline

A production integration is incomplete unless all applicable checks pass:

- SDK initialized before the application/framework starts handling real work.
- `environment` and `release` are present.
- One controlled exception arrives with a readable stack trace.
- JavaScript source maps or native debug files resolve correctly where applicable.
- Sensitive headers and payload fields have been tested for redaction.
- Performance sampling is explicitly configured when tracing is enabled.
- Browser trace propagation is restricted to intended destinations.
- Production alerts route to a real team or operational channel.
- Scheduled jobs have heartbeat/cron monitoring when missed execution matters.
- CI credentials use minimal required scope.
- Short-lived processes flush telemetry before exiting when required by the SDK.
- Telemetry failures do not fail the business request.
- For self-hosted GlitchTip, database backup and restore are tested and file storage is persistent.

## Anti-patterns

Avoid:

- hard-coding one DSN across local, staging, and production;
- naming environments with ephemeral values such as pod IDs;
- using request URLs with IDs as transaction names and causing high-cardinality groups;
- sending entire HTTP bodies "for debugging";
- attaching wallets, seed phrases, auth tokens, card data, private keys, or API secrets to events;
- setting `tracesSampleRate=1.0` in a high-traffic production service without a measured reason;
- globally sampling away severe errors instead of filtering known noise;
- manual `captureException` calls around every `try/catch`;
- swallowing exceptions after reporting when the normal control flow requires failure;
- uploading source maps after the release has already generated production errors;
- exposing source maps publicly solely to make error monitoring work;
- using a personal admin token in CI;
- paging on every new issue;
- treating Sentry/GlitchTip as a replacement for infrastructure metrics, centralized logs, SLOs, or synthetic monitoring;
- assuming every Sentry SDK feature is supported by GlitchTip;
- monitoring GlitchTip only with GlitchTip itself.

## Pair with

- `monitoring-expert` for Prometheus/Grafana, infrastructure metrics, structured logging, and general tracing.
- `sre-engineer` for SLIs, SLOs, error budgets, on-call, and incident policy.
- `devops` or `gitlab-cicd-devsecops` for deployment pipelines and credential boundaries.
- `security-reviewer` for privacy, threat modeling, and sensitive-data review.
- `llm-observability-ops` when traces include prompts, model calls, retrieval, or AI tool execution.

## Authoritative references

Verified 2026-09-20:

- https://docs.sentry.io/
- https://docs.sentry.io/api/releases/
- https://docs.sentry.io/api/projects/update-a-project/
- https://docs.sentry.io/api/projects/update-ownership-configuration-for-a-project/
- https://docs.sentry.io/api/crons/
- https://glitchtip.com/documentation/
- https://glitchtip.com/sdkdocs/all-sdks/
- https://glitchtip.com/documentation/performance/
- https://glitchtip.com/documentation/logs/
- https://glitchtip.com/documentation/cli/
- https://glitchtip.com/documentation/install/
