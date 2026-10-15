# Recurring payments, testing and operations

Source IDs resolve in [sources.md](sources.md). Operational controls and metrics below are recommended design practices, not vendor guarantees.

## Recurring and merchant tokens

Distinguish a short-lived merchant session, a one-time encrypted payment token, a processor vault reference, and an Apple merchant token (MPAN). For supported recurring, deferred or automatic-reload use cases, merchant tokens allow a merchant-specific credential lifecycle. Their availability depends on the integration and payment network; a device token may be returned where merchant-token support is absent. Wallet payment-authorization revocation and the underlying subscription contract are separate concerns. [A13]

Before offering recurring billing, document what the person sees and agrees to: initial charge, trial, regular amount or calculation, interval, next billing date, cancellation method and management URL. Store a consent/version record and a provider-supported reusable reference, not a token captured from the first payment sheet for repeated submission.

The subscription system owns renewal scheduling, merchant-initiated transaction parameters, retries, required customer authentication recovery, cancellation and receipts. Decide whether Apple lifecycle events are handled by the PSP or directly, and implement the corresponding authenticated notification/status contract. Stop using revoked credentials; expose a genuine customer-management flow and avoid equating a removed Wallet authorization with an automatically canceled contract.

Test renewals independently of the initial checkout: replaced device/card, revoked token, failed off-session authorization, duplicate invoice events, cancellation near renewal, amount changes and partial refunds. Do not enable automatic retries until the processor's mandate and network requirements are met.

## Separate test-environment axes

Record all four dimensions: application environment, PSP API mode, Apple Wallet/account environment and Apple merchant-session endpoint. They are not a single `sandbox=true` switch. See the dated environment change in [web and native integration](web-and-native.md).

| Route | Test setup | Important limitation |
| --- | --- | --- |
| Apple sandbox-supported processor flow | Apple sandbox tester, supported test device/card, matching Apple sandbox session and PSP test setup | Follow both Apple's and the processor's current procedure |
| Stripe Apple Pay test flow | Standard Wallet with a real supported card, Stripe test API keys and the corresponding Apple session flow | Stripe test cards and Apple sandbox test cards are not the documented Wallet setup for this route; test-mode processing does not charge the real card |
| Simulator/unit harness | Mock payment adapter and deterministic events | Does not prove device security, live issuer support or settlement |
| Approved live smoke | Explicitly authorized small purchase, verified capture, receipt and refund | Real money and operational approval required |

Apple's sandbox guide describes test accounts/cards and test-device configuration. A passing sandbox purchase is evidence of that test path only. Stripe documents a different test setup, so do not copy Apple sandbox instructions indiscriminately into every PSP integration. [A10, P1]

## Minimum acceptance matrix

| Case | Required evidence |
| --- | --- |
| Eligible purchase on each selected platform | Sheet/SDK result plus matching verified server state and one business effect |
| Digital product in an App Store app | Eligibility decision and correct StoreKit/approved-program routing, not an unconditional wallet button |
| Device without a usable wallet, unknown capability, unsupported browser | Correct presentation/fallback without a broken checkout |
| Domain, certificate, iframe or environment mismatch | Actionable sanitized diagnostics; no insecure bypass |
| Stale quote, changed shipping/tax, non-two-decimal currency | Server validation and exact displayed/authorized amount agreement |
| Double-click, two devices, retried API operation | Stable processor reference and one allowed business effect |
| Network loss after authorization | Unknown state, subsequent reconciliation, no blind second charge |
| Duplicate/out-of-order webhook, worker crash after persistence | Replay-safe recovery and no status regression |
| Invalid signature, wrong account/environment/order | Rejection or isolation without granting access |
| User cancellation versus issuer decline | Distinct UX and metrics; no claim that closing UI reversed a payment |
| Authorization without capture, expired authorization | Correct capture/void/recovery policy |
| Partial/full refund, repeat refund request, dispute | Correct residual amount, auditable ledger and business response |
| Renewal, revocation and cancellation boundary | Recorded mandate, appropriate retry/stop behavior and customer recovery |
| Telemetry and crash report inspection | No tokens, secrets, full contacts or sensitive domain metadata |

Document untested browser/device/issuer combinations rather than labeling them supported. The [agent evaluation cases](../evals/cases.json) are a review rubric, not executed financial transactions.

## Optimization with guardrails

Establish a baseline before making a performance claim. Measure separately: eligible sessions, rendered button, sheet requested, authorization attempted, verified payment, and fulfilled order. Use the appropriate denominator; a larger population of unsupported browsers should not look like a payment decline spike.

Track p50/p95 time to usable checkout, quote latency, merchant-validation latency where owned, confirmation latency, provider error class, webhook-to-ledger lag and fulfillment lag. Separate user cancellation, configuration failure, issuer decline and unknown outcome. Correlate with opaque order/attempt IDs rather than payment payloads.

Useful experiments include: loading the selected SDK once near checkout rather than throughout the app; prefetching a versioned quote without breaking direct user activation; reducing unnecessary contact collection; reusing secure server connection pools; moving noncritical fulfillment behind an outbox; and repairing slow validation or configuration checks before redesigning the button.

Do not cache a shared merchant session, skip signature verification, grant access before server confirmation, retry with fresh payment keys, or hide a legitimate fallback to improve a dashboard number. Choose latency/availability targets from business requirements and observed provider behavior, not invented universal thresholds.

## Release and incident runbook

Assign owners for certificates/domains, payment reconciliation, subscriptions, refunds and customer support. Alert before actual credential expiry, on rising unknown outcomes, duplicate business effects, webhook backlog and unfulfilled confirmed payments. Test certificate replacement with overlap where supported before retiring the old credential.

Roll out by an explicitly chosen canary population and compare against an eligible baseline. A kill switch should stop new Apple Pay initiation while leaving status lookup, webhooks, captures/voids as appropriate, refunds and reconciliation operational. Keep account management and essential nonpayment flows available.

Triage by layer: policy/merchant eligibility -> domain/certificate/environment -> capability/origin -> user gesture/sheet lifecycle -> provider confirmation -> webhook/ledger -> fulfillment. Inspect configuration fingerprints and sanitized correlation IDs, not raw tokens. For a lost response, first retrieve the original payment; do not tell the customer to pay again until the outcome is known.
