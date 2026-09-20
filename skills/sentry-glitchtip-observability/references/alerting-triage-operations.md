# Alerting, Triage, and Operations

## Alert design

Create different classes of alerts for different questions.

### New/regressed issue alerts

Useful when:

- a new production issue first appears;
- a resolved issue regresses;
- an error starts in a new release.

Route to the owning team or engineering channel rather than paging by default.

### Rate or user-impact alerts

Page only when a threshold implies meaningful service impact.

Examples:

- checkout exceptions exceed an absolute or rate threshold;
- failed transaction count rises sharply after a deploy;
- a critical background job stops completing;
- an error affects many distinct users/accounts.

Avoid paging on "one error occurred."

## Ownership

For Sentry, use ownership rules or source-control CODEOWNERS integration when available. Current Sentry APIs support project ownership configuration and automatic assignment modes.

Ownership should map to the team capable of fixing the code, not merely the team that receives alerts.

For GlitchTip, configure project/team membership and alert destinations explicitly; do not assume Sentry CODEOWNERS behavior is implemented identically.

## Triage order

For a new production issue:

1. Confirm environment and release.
2. Check first seen, last seen, frequency, and affected users/accounts.
3. Read the original exception and full stack.
4. Inspect breadcrumbs and structured context.
5. Check tags: route, browser/runtime, region, provider, feature.
6. Open the trace and identify the failing span when performance data exists.
7. Correlate request/trace IDs with centralized logs.
8. Compare the issue start time with deploy metadata.
9. Inspect commits in the release or source diff.
10. Decide: mitigate, rollback, feature-disable, retry, or fix forward.
11. Add the issue to the incident/work item if user impact is material.
12. Verify the fix in the next release before resolving permanently.

## Severity model

Example:

- **Critical** — active loss of availability, money movement, authentication, data integrity, or broad user impact. Page immediately.
- **High** — major feature failure or rapidly increasing error rate. Notify owning team urgently.
- **Medium** — isolated production bug with workaround. Track in normal engineering flow.
- **Low** — noisy or cosmetic issue. Batch or suppress after validation.

Do not infer severity from exception type alone.

## Alert quality checklist

Every alert should define:

- condition;
- environment;
- project/service;
- owner;
- severity;
- notification target;
- deduplication/cooldown behavior;
- runbook or first-response steps;
- stop condition.

Review alerts after incidents. Remove alerts that repeatedly generate no action.

## Cron and heartbeat monitoring

Use monitor/heartbeat semantics for scheduled jobs where absence is the failure.

Examples:

- settlement batch;
- reconciliation;
- invoice generation;
- backup;
- daily report;
- blockchain indexer checkpoint;
- token price refresh.

Sentry provides Cron/Monitor APIs and SDK integrations.

GlitchTip uptime monitoring supports a Heartbeat mode in which the application calls a generated URL and GlitchTip alerts when expected calls stop.

Heartbeat monitoring is usually better than logging "job finished" and hoping someone notices its absence.

## Uptime monitoring

Use uptime checks for externally observable availability.

Monitor:

- public API health that reflects dependencies, not only process liveness;
- login/auth path;
- payment initiation endpoint;
- customer-facing web application;
- webhook ingress when externally testable.

Do not expose sensitive internal endpoints solely for uptime checks.

For GlitchTip, associate an uptime monitor with a project that has notification rules. Current documentation notes that hosted uptime requests count toward organization event limits.

## External monitoring principle

Do not depend on one system to monitor itself.

For self-hosted GlitchTip:

- monitor GlitchTip ingress from an external uptime system;
- monitor PostgreSQL/Valkey/storage independently;
- alert on worker queue/backlog and database capacity via infrastructure monitoring.

For Sentry SaaS:

- keep infrastructure/SLO monitoring in a separate metrics system when the service requires independent availability signals.

## Incident evidence

Capture:

- issue URL/ID;
- release;
- environment;
- deployment time;
- event count;
- affected user/account estimate;
- trace ID/request ID;
- suspected commit;
- mitigation;
- final fix release;
- regression test added.

Turn recurring classes into automated tests or static/runtime guards.

## Sources

- https://docs.sentry.io/api/projects/update-ownership-configuration-for-a-project/
- https://docs.sentry.io/api/crons/
- https://docs.sentry.io/api/monitors/
- https://glitchtip.com/documentation/uptime-monitoring/
- https://glitchtip.com/documentation/cli/
