---
name: google-pay-integration
description: >
  Research, plan, implement, review and optimize Google Pay online payments across
  Web, Android, Flutter, React Native and supported WebViews. Covers provider
  selection, Google Play Billing boundaries, tokenization, server-side payment
  state, subscriptions/MIT, testing and production approval. Use for Google Pay,
  GooglePay, GPay, интеграция Google Pay, платежи Google Pay. Do not use as a
  Google Wallet passes, NFC issuing, Google Play publishing or India UPI tutorial.
metadata:
  version: "1.0.0"
  researched-at: "2026-10-15"
  portability: "project-, provider-, framework- and agent-runtime-neutral"
---

# Google Pay integration

Produce an evidence-backed integration or implementation plan, not merely a payment button. Adapt to the actual merchant, jurisdiction, platform and processor. Never assume a particular repository, product, cloud, currency, PSP or agent tool.

## Load only the needed reference

- [Platforms and routing](references/platforms-and-routing.md): eligibility, billing boundary, gateway versus direct, Web/Android/wrapper implementation.
- [Payment lifecycle and security](references/payment-lifecycle-security.md): backend contracts, idempotency, authentication, webhooks, refunds and privacy.
- [Recurring payments and token lifecycle](references/mit-and-token-lifecycle.md): subscriptions, deferred charges, automatic reloads and 2026 MIT capabilities.
- [Testing, production and optimization](references/testing-production-optimization.md): acceptance matrix, approval, performance, metrics and rollback.
- [Sources and freshness](references/sources.md): primary references, observed conflicts and revalidation rules.
- [Integration-plan template](assets/integration-plan.template.md), [configuration example](assets/google-pay.env.example) and [evaluation cases](evals/cases.json).

Read the core, the applicable platform section, and the lifecycle reference first. Load MIT only when future charging is in scope. Source IDs below resolve in `references/sources.md`; detailed engineering controls are recommendations, not invented Google API requirements.

## Invariants

1. **A wallet result is not a charge.** Google Pay supplies payment credentials; the merchant's server/PSP completes payment. Fulfillment depends on authoritative server-side payment state, never a client success flag. [G01]
2. **Resolve the billing route before coding.** Google Pay is not Google Play Billing. Digital in-app purchases require current policy/program analysis; eligibility for alternative billing is not a universal exemption. [P01]
3. **Choose the smallest compliant integration.** Prefer a supported PSP's hosted checkout/component/native SDK when it meets the requirements. Otherwise use Google Pay API with a supported gateway. `DIRECT` requires qualifying PCI DSS controls and review; it is not a workaround for an unsupported merchant. [G01, G09]
4. **Use runtime capability detection and retain another payment route.** Do not promise support from browser brand, nationality, Android presence, or an old country list alone. [G02, G04, G07]
5. **Server owns money and identity.** Recalculate amount, currency, tax, shipping and eligibility; authenticate the buyer and bind every attempt to the right order and merchant account.
6. **One logical attempt, one economic effect.** Use persistent scoped idempotency, verified/deduplicated notifications and recovery after unknown outcomes. No blind re-charge on timeout. [S01, S02]
7. **No payment secrets in the client or telemetry.** Keep PSP private keys, direct decryption keys, raw wallet payloads and sensitive addresses out of bundles, logs, error reports, replay and analytics.
8. **Separate environments and authorities.** `TEST` does not prove production processing. Console approval, PSP activation, release signing and store-policy compliance are separate gates. An agent must not accept contracts, enroll in billing programs, charge real cards or enable production without explicit authority. [G05, G08, G10]

## Workflow

### 1. Establish a portable context contract

Read authorized repository/configuration and merchant documentation before asking for information already available. Record unknowns; proceed with a conditional plan rather than inventing missing values.

```yaml
integration_context:
  merchant_entity_country: unknown
  customer_markets: []
  currencies: []
  sale_type: physical_goods | physical_services | digital | mixed | unknown
  surfaces: [] # web, android, flutter_android, react_native_android, webview
  distribution: unknown # ordinary web, Google Play, other store/channel
  charge_model: one_time | recurring | deferred | automatic_reload | mixed
  psp_and_account_region: unknown
  integration_owner: merchant | psp | platform
  existing_payment_state_and_webhooks: unknown
  required_authentication_and_capture: unknown
  production_approval: unknown
  source_checked_at: YYYY-MM-DD
```

Keep consumer support, merchant onboarding availability, acquiring country, currency and store policy as separate questions. A Google Pay API gateway listing alone does not confirm that a specific merchant can onboard or transact.

### 2. Resolve the decision gates

Document `supported`, `unsupported`, or `requires_verification`, with sources and date, for each surface and business model. For Google Play digital goods, verify user market, enrollment, applicable alternative-billing/external-offers terms, disclosure, reporting and fees; otherwise route to Play Billing. For iOS app distribution, check that store's payment rules separately. Do not bypass rules through a WebView. [P01]

Distinguish online card payments from Google Wallet passes/issuing/NFC and the separate India UPI integration family. Route out-of-scope work explicitly. [G01, I01]

Choose one primary adapter: PSP-managed, Google API with `PAYMENT_GATEWAY`, or approved `DIRECT`. List who owns token processing, risk/SCA, recurring credentials, refunds and reconciliation.

### 3. Define backend contracts before the UI

Specify the order quote/version, payment-attempt identifier, idempotency scope, provider identifiers, transitions, webhook verification and fulfillment policy. Include canceled, declined, action-required and unknown/pending outcomes. Keep authorization, capture, settlement and refund distinct. See the lifecycle reference.

For subscriptions or later charges, add an explicit agreement, PSP vault/mandate contract, off-session authentication recovery and cancellation semantics. Read the MIT reference; never replay a one-time Google Pay payload as a subscription mechanism.

### 4. Implement the selected surface

Read current Google and PSP documentation for the selected route and pin the tested SDK versions in the actual project. Keep the reusable skill free of assumed dependency versions.

For a raw Google API integration, align allowed networks and authentication methods with the PSP, configure the correct tokenization parameters, and keep Google `merchantId` distinct from the PSP's merchant/account identifiers. Use official button APIs/assets and minimal requested user data. [G03, G11, G12]

For Web, preserve the click's user activation when calling `loadPaymentData`; prepare the server quote beforehand. For Android, test lifecycle and release signing. For wrappers and WebViews, confirm native capability and approval rather than assuming a web demo transfers unchanged. [G04, G07, G08]

### 5. Verify the whole money path

Use layered evidence: request/unit/contract tests; PSP-sandbox processing; real browser/device interaction; production-readiness review; then an explicitly authorized production smoke transaction/refund. A mock wallet token is not an end-to-end settlement test. [G10]

Test double clicks, concurrent attempts, duplicate/out-of-order webhooks, forged events, amount/currency tampering, timeouts after successful authorization, process death, SCA challenges, capture/refund failures and unsupported devices. Use `evals/cases.json` to evaluate agent behavior separately from payment-system tests.

### 6. Obtain approval and release safely

Prepare the Google Pay & Wallet Console evidence appropriate to the integration owner: business profile, domain or Android application, screenshots, integration type and test results. Track review status; do not equate submitting with approval. PSP-managed flows may delegate some steps: confirm the division with that PSP. [G05, G08]

Switch Google and PSP environments coherently, guard placeholders in release builds, retain a kill switch and fallback, and verify refunds/reconciliation. Do not disable webhook processing when hiding the Google Pay button.

### 7. Optimize using measured bottlenecks

Measure eligible checkout exposure, readiness, button click, wallet result, server-confirmed payment, latency and failures with sanitized identifiers. Deduplicate conversion events. Separate cancellations from integration/PSP failures, while remembering that a Web `CANCELED` code can also represent environment or request problems. [G04]

Prioritize readiness/render latency, valid totals, fewer unnecessary fields and reliable authentication. Use documented prefetch only where supported; do not promise a conversion uplift. Record experiment baseline, sample, metric, guardrails and rollback conditions.

## Required output

Return an eligibility/adapter decision, dated source ledger, implementation plan with dependencies and ownership, configuration inventory, payment-state contract, acceptance tests, production checklist and optimization plan. Every step needs a verifiable completion criterion. Separate `implemented`, `tested`, `submitted`, `approved`, `blocked` and `not_run`.

When only research is requested, produce the portable skill/plan; do not modify an application or merchant settings. Keep product names, domains, prices, repository paths and credentials in a consuming project's context, not in this skill.

## Definition of done

The selected route is evidenced; server-side payment integrity and recovery are specified; platform/PSP limits are explicit; examples contain no live credentials; relative references resolve; catalogs expose the skill; and test results state exactly what ran. Research/packaging success must never be described as a deployed or production-approved payment integration.
