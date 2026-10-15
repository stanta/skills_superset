# Testing, production readiness and optimization

Sources: [sources.md](sources.md). Separate a prepared test case from evidence that it actually ran.

## Layered test strategy

**Local/contract tests:** request schema, money formatting, quote ownership, state transitions, replay protection, webhook signature checks and environment guards.

**Google TEST sheet:** validate readiness/button behavior, permitted fields, errors, returned data shape and billing terms. The current test-card guide says test cards appear by default in `TEST`; its generated summary retains older group-joining language. Use the body and current PSP instructions, not the stale summary. [G10]

**PSP sandbox:** eligible gateway test cards can exercise the processor's test responses. Unsupported-gateway mock cards only exercise the payment sheet and may fail at the processor. A production card used in `TEST` can return placeholder data. None of these proves real settlement. [G10]

**Browser/device checks:** test supported desktop/mobile browsers, Android release artifacts, wrapper lifecycle, WebView feature availability, accessibility, redirects and slow/interrupted networks. Record actual version/device and PSP environment rather than claiming all platforms are covered.

**Production smoke:** only with explicit authority, approved integration, approved merchant account and a controlled real transaction; verify capture/receipt/refund and reconciliation. A successful smoke payment is not a complete fraud or settlement audit.

## Minimum acceptance matrix

| Case | Required outcome |
| --- | --- |
| Readiness false or SDK unavailable | No unusable Google Pay button; another payment route works. |
| Eligible buyer without a saved card | Add-card path works when supported/configured; not excluded accidentally. |
| Both supported authentication modes | PSP receives and processes the expected credential type. |
| Cancel/close sheet | No fulfillment; order can be resumed. Investigate anomalous clusters of `CANCELED`. |
| Double click and parallel requests | One active launch and no duplicate economic effect. |
| Alter amount, currency, quote or merchant | Server rejects tampering and cross-account access. |
| Provider decline / 3DS required | Truthful recoverable UI; no premature paid state. |
| Timeout after provider approval | Existing operation reconciled; no fresh duplicate charge. |
| App killed / browser refreshed | Status recovered from backend, not stale client state. |
| Replayed, forged, wrong-account webhook | Rejected/deduplicated without changing another order. |
| Out-of-order events | State never regresses; capture/refund ledger stays consistent. |
| Changed shipping/expired quote | Recalculate and obtain approval for a new payable amount. |
| Refund, partial refund, void | Correct permissions, amount bounds and reconciliation. |
| MIT enabled | Correct single intent object, agreement, renewal and lifecycle tests. |
| Observability capture | No raw credentials, addresses, card data or sensitive payloads escape. |
| Kill switch | New Google Pay launches stop; pending operations and webhooks still reconcile. |

Add processor-specific settlement, dispute and multi-currency cases where applicable. Track each as `pass`, `fail`, `not_run` or `not_applicable` with justification.

## Production checklist

For merchant-owned integrations, Google production onboarding includes the business profile, applicable terms, integration type and screenshots in Google Pay & Wallet Console. Websites submit the relevant calling domain; Android apps are associated with their Play account and reviewed separately. Google approval and PSP activation are separate. For PSP-managed flows, confirm which obligations are delegated. [G05, G08]

Before activation, verify:

- Required domain/app review is **approved**, not merely submitted; merchant identity and visible business name are correct.
- Google `PRODUCTION` and PSP live configuration are coherently selected; no sample gateway or placeholder merchant IDs remain.
- Android uses release signing and the intended package. Approval of a website does not itself authorize its Android WebView host.
- Server secrets, notification verification, retry/reconciliation, capture/refund rules and fallback are operational.
- Support/refund contacts, consent/disclosures and any regional program reporting are ready.

Roll out behind a feature flag with a predeclared exposure plan and stop conditions. Disable new launches for material duplicate-charge, amount-integrity or sustained processing failures; retain reconciliation, support and refunds. Human approval is required for commercial agreements, production changes and real-money tests.

## Performance and conversion

Treat optimization as a measurable engineering hypothesis, not guaranteed uplift.

| Change | What to measure / guardrail |
| --- | --- |
| Load the official library early on relevant checkout paths | Readiness/button-render latency versus page performance and privacy requirements. |
| Reuse the client; avoid repeated readiness calls per render | Latency and error rate without caching capability indefinitely across context changes. |
| Prepare a current quote before the click | Sheet-open reliability and quote freshness; preserve user activation. |
| Use `prefetchPaymentData` where supported | Sheet latency on Chrome for Android; it does not authorize payment. |
| Request only necessary contact/address fields | Completion versus fulfillment/risk data requirements. |
| Use official localized, accessible buttons at payment-method parity | Eligible exposure, accessibility and click-through; no misleading branding. |
| Optimize callback dependencies | Tail latency below the documented deadline, without weakening fraud checks. |
| Provide clear decline/action/retry states | Recovery completion; no retry loop or duplicate charge. |

The client reference currently limits prefetch optimization to Chrome for Android; changes to `transactionInfo` do not affect its cached value. Always send the actual authoritative purchase request. Authorization and dynamic-update callbacks have a 30-second limit: budget below it, and do not claim success just to beat the timeout. [G04]

A sanitized funnel can use `gpay_eligible`, `gpay_button_rendered`, `gpay_clicked`, `gpay_result_received`, `payment_processing`, `payment_succeeded` and `payment_failed`. Define denominators explicitly. Count `payment_succeeded` from the server's authoritative event and deduplicate by stable order/payment identity. Do not equate wallet-sheet completion with conversion.

Track p50/p95/p99 sheet and PSP latency, readiness failures, provider declines, action-required recovery, duplicate attempts, webhook lag and reconciliation mismatches. Use coarse platform/environment/adapter labels and allowlisted error categories, not raw error text or card details. Keep commercial and sensitive user data out of analytics.

## Skill evaluation, not payment certification

Run the scenarios in `../evals/cases.json` against the same agent with and without this skill. Record model/runtime, prompt, output, required checks, forbidden actions, trigger decision and reviewer. Compare trigger precision/recall and critical-error counts; do not infer measured improvement from author review alone.

Static Markdown/JSON/link validation proves packaging only. Browser/device/PSP tests, production approval and comparative agent evaluations require separate recorded evidence.
