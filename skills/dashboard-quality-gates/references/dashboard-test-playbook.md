# Dashboard Test Playbook

## Requirement-to-test template

| Requirement | Risk | Test level | Fixture/scenario | Assertion | Evidence | Gate |
|---|---|---|---|---|---|---|
| Summary is tenant-scoped | Data leak | API + E2E + stream | Tenant A/B overlapping IDs | No B facts/events/cache in A | Logs + trace + test result | P0 zero tolerance |
| Recovered failure is separate | Wrong health signal | Unit + integration | Failed run with successful retry lineage | Recovered increments; unresolved failed does not | Expected/actual aggregate | P1 |

## Metric oracle strategy

1. Freeze a minimal event/run fixture.
2. Calculate expected values independently of production aggregation code.
3. Include boundary and adversarial rows.
4. Compare backend read model, displayed value, and drill-down record count.
5. Keep the fixture versioned with metric contract changes.

Required fixture categories:

- empty and true zero;
- exactly at time boundary;
- timezone/DST/calendar month;
- duplicate event;
- late/corrected event;
- retry chain with recovery;
- cancellation/timeout/policy block;
- missing cost/token data;
- high value/rounding;
- unauthorized or deleted entity.

## Dashboard state matrix

| Data | Live | Permission | Mutation | Expected UI |
|---|---|---|---|---|
| None | Connected | Allowed | Idle | “No data yet,” not zero/error |
| Cached valid | Disconnected | Allowed | Idle | Retain data, label stale/disconnected, offer retry |
| Partial | Connected | Allowed | Idle | Identify missing widgets/sources; preserve available facts |
| Error | Connected | Allowed | Idle | Scoped error and recovery; do not blank unrelated widgets |
| Valid | Connected | Read-only | Attempted | Disabled/hidden action with reason; server also rejects |
| Valid | Connected | Allowed | Pending | Disable duplicate action; show progress and cancel policy |
| Valid | Lost | Allowed | Unknown | Reconcile durable outcome before allowing repeat |

## Agent-control-plane scenarios

- A ready idle agent is not shown as stopped.
- A running agent whose latest prior run failed displays current execution separately from last outcome.
- A retry chain that recovers remains inspectable and is counted as recovered.
- A stalled run is distinguished from slow but progressing.
- An approval expiry and denial produce different statuses and audit evidence.
- A cancellation request races with natural success and resolves deterministically.
- A tool call retries without duplicate irreversible side effect.
- Prompt/model/config/evaluator versions remain visible through drill-down and export.
- Redacted users cannot obtain raw prompt/tool payload through alternate APIs or streams.

## Accessibility manual charter

Execute critical journeys using keyboard only and at least one screen reader:

1. Enter through skip link and identify page/scope/freshness.
2. Read headline status without relying on color.
3. Operate filters and reset them.
4. Traverse chart summary and accessible data alternative.
5. Open an affected run from an exception.
6. Inspect timeline/tool/evaluation evidence.
7. Complete a confirmation dialog; verify focus restoration.
8. Trigger and recover from validation/server error.
9. Zoom/reflow and repeat the action at narrow width.

Record browser, assistive technology, theme, locale, viewport, result, and defect evidence.

## Realtime resilience assertions

Do not assert only WebSocket message receipt. Assert:

- resulting cache entity version;
- terminal/nonterminal invariant;
- final REST/durable state agreement;
- disconnected/stale UI indication;
- bounded requests and memory;
- no duplicate command effect;
- cross-tab/replica behavior;
- recovery time and event-to-paint SLO.

## Performance workload model

Define at least three profiles:

| Profile | Example |
|---|---|
| Typical | 20 agents, 5 concurrent runs, 1 tab |
| Heavy tenant | 500 agents, 100 concurrent runs, 10 operators |
| Hot investigation | 1 run with high-frequency events/logs, long transcript, 3 tabs |

Measure cold/warm load, sustained live updates, filtering, navigation, transcript retention, reconnect storm, and export. Record server query count/latency and browser CPU/memory/frame behavior together.

## Security payload corpus

Include inert test strings for:

- HTML/script/event handlers;
- markdown links with dangerous schemes;
- ANSI/control characters and bidi overrides;
- spreadsheet formulas beginning with `=`, `+`, `-`, or `@`;
- oversized nested JSON/log chunks;
- prompt-injection-like tool output;
- secrets and PII requiring redaction;
- malformed Unicode and filenames;
- cross-tenant entity IDs and stale/revoked credentials.

## Release scorecard

```markdown
# Dashboard Release Gate

- Metric correctness: PASS/FAIL
- Authorization and tenant isolation: PASS/FAIL
- Privileged actions and audit: PASS/FAIL
- Realtime resilience: PASS/FAIL
- Accessibility critical paths: PASS/FAIL
- Visualization integrity: PASS/FAIL
- Performance budgets: PASS/FAIL
- Security rendering/export: PASS/FAIL
- Browser/theme/locale matrix: PASS/FAIL
- Open P0/P1 defects: <count>
- Rollback criteria verified: YES/NO
- Decision: SHIP / HOLD
```

## Source repositories

All listed repositories exceed 5 stars and/or forks:

- `microsoft/playwright` — isolated browser E2E, network mocking, multi-context, visual and accessibility-oriented workflows: https://github.com/microsoft/playwright
- `dequelabs/axe-core` — automated accessibility rules integrated across test layers: https://github.com/dequelabs/axe-core
- `grafana/k6` — load and performance testing with thresholds: https://github.com/grafana/k6
- `GoogleChrome/lighthouse` — accessibility, best-practice, and performance audits: https://github.com/GoogleChrome/lighthouse
- `paperclipai/paperclip` — concrete agent dashboard failure, authorization, polling, and realtime hypotheses: https://github.com/paperclipai/paperclip
- `OWASP/ASVS` — application security verification requirements: https://github.com/OWASP/ASVS
- `OWASP/www-project-web-security-testing-guide` — web security testing methodology: https://github.com/OWASP/www-project-web-security-testing-guide

This playbook complements existing `test-master`, `playwright-expert`, `web-design-guidelines`, and security skills by specializing their use for operational and AI-agent dashboards.
