# Google Pay integration plan

Use in a consuming project. Replace placeholders with authorized evidence, not guesses. Status vocabulary: `unknown`, `requires_verification`, `planned`, `implemented`, `tested`, `submitted`, `approved`, `blocked`, `not_run`.

## Context and decision

- Merchant entity/account region: `<unknown>`; customer markets: `<unknown>`.
- Surfaces and distribution channels: `<unknown>`; sale/charge models: `<unknown>`.
- PSP and tested SDK versions: `<unknown>`; existing payment service: `<unknown>`.
- Google Pay versus store billing decision: `<source + date + enrollment evidence>`.
- Adapter: `<PSP-managed | PAYMENT_GATEWAY | approved DIRECT>`; rationale: `<evidence>`.
- Unknowns and launch blockers: `<owner + evidence required>`.

## Responsibility and source ledger

| Requirement | Google/PSP/application owner | Source, section, checked date | Evidence/status |
| --- | --- | --- | --- |
| Merchant eligibility and acquiring | `<owner>` | `<source>` | `<status>` |
| Store payment route and enrollment | `<owner>` | `<source>` | `<status>` |
| Token processing and authentication | `<owner>` | `<source>` | `<status>` |
| Future-charge consent and scheduling | `<owner>` | `<source or not applicable>` | `<status>` |
| Capture, refunds and reconciliation | `<owner>` | `<source>` | `<status>` |
| Domain/app approval and release signing | `<owner>` | `<source>` | `<status>` |

## Implementation tasks

| Step | Dependencies | Work and artifact | Completion evidence |
| --- | --- | --- | --- |
| 1. Eligibility | Context | Dated platform/policy/PSP decision | Supported route or explicit blocker |
| 2. Backend | Step 1 | Quote/version, buyer/tenant binding, attempt and idempotency contract | Tamper and concurrent-attempt tests |
| 3. Payment state | Step 2 | Authorize/action/capture/refund transitions, verified notifications | Duplicate, out-of-order and unknown-outcome tests |
| 4. Client | Steps 1–3 | Official button, readiness, correct request, lifecycle-safe return | Actual browser/device evidence |
| 5. MIT, when needed | Steps 1–4 | Consent/version, supported transaction object, PSP vault and schedule, token lifecycle | Renewal/cancellation and lifecycle tests |
| 6. Observability | Steps 2–5 | Sanitized funnel, alerts and reconciliation | No sensitive payloads; deduplicated server-confirmed conversion |
| 7. Approval | Completed test evidence | Google/PSP review artifacts and actual status | Approval recorded, not merely submission |
| 8. Rollout | Step 7 and explicit authority | Coherent production config, feature flag, fallback, smoke/refund | Authorized real-money evidence or `not_run` |

## Payment and security contract

Specify authoritative money representation; quote expiry/version; idempotency identity and retention; tenant/account binding; provider operations; raw-body signature verification; durable event deduplication; unknown-outcome reconciliation; fulfillment trigger; partial/full refund rules; and secret/data retention controls. State whether authorization or capture permits fulfillment for this business. Do not mark settlement as complete based only on capture.

## Acceptance and execution ledger

| Case | Environment/SDK/device | Expected economic effect | Actual evidence | Result |
| --- | --- | --- | --- | --- |
| Unsupported runtime / cancel | `<test>` | No charge; alternative route | `<evidence>` | `not_run` |
| Success / SCA action / decline | `<PSP sandbox>` | Correct state and fulfillment policy | `<evidence>` | `not_run` |
| Double click / concurrent distinct keys | `<test>` | No duplicate order payment | `<evidence>` | `not_run` |
| Timeout after authorization / app death | `<test>` | Recover same attempt, no blind recharge | `<evidence>` | `not_run` |
| Forged/duplicate/out-of-order event | `<test>` | No unauthorized or duplicate transition | `<evidence>` | `not_run` |
| Wrong amount/currency/buyer/tenant | `<test>` | Reject without fulfillment | `<evidence>` | `not_run` |
| Refund / partial refund / reconciliation | `<sandbox>` | Correct ledger and status | `<evidence>` | `not_run` |
| MIT / lifecycle / cancellation race | `<when applicable>` | Agreement respected; token update is not payment | `<evidence>` | `not_run` |
| Production smoke and refund | `<explicitly authorized>` | Controlled charge/refund | `<evidence>` | `not_run` |

## Optimization and rollback

Baseline and cohort: `<unknown>`. Measure eligible exposure, readiness, sheet launch, authoritative payment conversion, latency and failure category. Hypothesis: `<one measurable bottleneck>`. Guardrails: duplicate charges, fraud/SCA failures, privacy, refund/reconciliation gaps. Rollout/rollback thresholds: `<chosen from baseline>`. Hiding the button must not stop payment events, refunds or reconciliation.

## Handoff

List actual changed files, commands/tests executed, evidence artifacts and remaining account-owner actions. Separate implementation, test, submission and approval. Do not claim live integration from a completed research document.
