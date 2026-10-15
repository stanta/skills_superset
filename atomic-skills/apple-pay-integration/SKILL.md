---
name: apple-pay-integration
description: >
  Plan, implement, audit, troubleshoot and optimize Apple Pay on the web and in native applications. Use for ApplePay, PassKit, merchant validation, payment certificates, wallet checkout, recurring merchant tokens, PSP integration and payment reliability. Includes a digital-goods versus StoreKit eligibility gate, provider-neutral backend contracts and optional Stripe/Adyen adapters. Russian queries: интеграция Apple Pay; Эпл Пэй; оплата на сайте; платежи iOS; проверка мерчанта.
metadata:
  reviewed: "2026-10-15"
  scope: "cross-project, cross-agent, provider-neutral"
---

# Apple Pay integration

Deliver a source-backed integration decision and an implementation that cannot confuse wallet authorization with a completed business payment. Adapt to the actual product, merchant, distribution channel and processor; never transplant another project's identifiers, deployment layout, currency, legal entity or billing rules.

## Scope and routing

Use for a new integration, an existing checkout audit, missing-button or payment-sheet failures, native entitlement setup, recurring billing, or checkout performance. This skill covers online acceptance, not Tap to Pay terminals, payment-card issuing, Wallet passes, Apple Cash transfers, or a complete StoreKit implementation. A digital-goods request may terminate with a StoreKit handoff rather than Apple Pay code.

No proprietary agent runtime, connector, shell, payment account or SDK is presumed. Read/search the actual repository with available tools. Use provider consoles and signing operations only when authorized. Never request private keys or production secrets in chat.

## Load only the relevant references

| Subtask | Read |
| --- | --- |
| Decide whether and where Apple Pay is appropriate | [Eligibility and architecture](references/eligibility-and-architecture.md) |
| Configure domains, certificates, web sessions or native targets | [Web and native integration](references/web-and-native.md) |
| Design payment APIs, webhooks, idempotency and trust boundaries | [Backend and security](references/backend-security.md) |
| Renewals, test environments, rollout, incidents and optimization | [Recurring, testing and operations](references/recurring-testing-operations.md) |
| Map the portable contract to a selected processor | [Provider adapters](references/provider-adapters.md) |
| Verify current rules and API details | [Primary sources](references/sources.md) |

Detailed instructions use source IDs from the source register. Re-open the relevant current source before implementation or launch; a review date is not a promise that policies, supported markets or SDKs remain unchanged.

## Workflow

### 1. Establish the decision boundary

Inspect only relevant manifests, payment APIs, checkout UI, signing configuration, billing models and tests. Record revision and evidence paths. Identify goods consumed, platforms, storefronts, merchant country, currencies, provider, payment-account model, capture policy, subscription requirements and existing entitlements. Unknown prerequisites become named blockers, not guessed defaults.

Complete the eligibility matrix before selecting a button or SDK. Keep policy eligibility, merchant underwriting, device/browser capability and issuer authorization as separate decisions. The person approving a commercial/legal exception must be identifiable.

### 2. Select the smallest supported integration

Compare hosted checkout, a provider-managed component/native sheet, and direct Apple APIs. Prefer an existing supported payment stack when it meets requirements. Document why custom orchestration is necessary before taking ownership of merchant validation or token processing. Select one owner for each certificate, validation step, payment object, webhook and subscription lifecycle.

Do not assume that a web-only provider-managed checkout needs the same Apple account and certificate work as a self-managed native integration. Keep provider-specific details in the chosen adapter.

### 3. Build an evidence-backed implementation plan

Use [the plan template](templates/integration-plan.md). Name artifacts, owners, dependencies, tests and acceptance evidence for each step. Separate read-only investigation, sandbox work, commercial onboarding, production secret provisioning and explicitly approved live tests. Use [the configuration example](templates/env.example) as a contract sketch, not a ready-to-deploy configuration.

### 4. Implement trust boundaries before the visible button

Make quotes, order ownership, payable amount and currency server-authoritative. Define durable payment attempts, provider-reference mapping, stable idempotency, authenticated status retrieval, webhook verification, reconciliation and fulfillment. Implement cancellation and unknown-outcome recovery. Connect client presentation only after these invariants are testable.

Keep the payment adapter replaceable without changing the order ledger. Do not automatically switch processors after an ambiguous authorization result or replay an encrypted wallet token.

### 5. Configure the selected client path

Follow the web/native reference for capability detection, direct user activation, certificate ownership, target entitlements, origin validation and lifecycle cleanup. Adapt examples to the pinned SDK and actual deployment targets. Keep a supported alternative payment path for eligible users who cannot use Apple Pay.

### 6. Validate before rollout

Run deterministic backend tests, callback and webhook failure cases, real-device/provider-specific sandbox tests, and an approved production smoke payment/refund when required. Record exactly which evidence exists. Unit tests, a simulator screenshot and a synthetic webhook cannot individually prove end-to-end payment acceptance.

Use [evaluation cases](evals/cases.json) to assess agent behavior as well as implementation plans. The bundled repository tests check packaging and navigation; they are not payment execution or an empirical model benchmark.

### 7. Roll out with measurable guardrails

Release behind an explicit feature flag. Establish an eligible-user baseline, checkout-stage latency, confirmed-payment conversion, duplicate-effect count and reconciliation lag. Use a canary and a rollback plan that disables new checkout while retaining webhooks, refunds, status lookup and pending-order recovery. Do not claim an optimization benefit without measurements.

## Non-negotiable review checks

- No frontend-controlled prices, identity certificates, decryption keys or fulfillment decisions.
- No wallet token, full contact payload, client secret or sensitive business context in analytics, crash reports or ordinary logs.
- No merchant-validation endpoint that proxies arbitrary URLs or follows arbitrary redirects.
- No new charge merely because a payment sheet, browser or network timed out.
- No production assumption inferred from a sandbox success, language, IP address or historical support list.
- No undocumented digital-goods policy bypass through a WebView, external link or regional flag.
- No credential revocation, account changes, production deployment or live charge without the appropriate approval.

## Required output

Return: the eligibility decision with source/date; the chosen ownership model and alternatives; implementation steps and sanitized configuration; test results versus unexecuted tests; rollout/rotation/reconciliation runbooks; and unresolved commercial or policy blockers. Preserve sources and relevant repository revisions, not raw private transcripts.

## Definition of done

All applicable decision gates have evidence, payment effects are replay-safe, secrets remain outside client/repository/logs, failure recovery and refunds are defined, the selected client/provider combination is tested, and remaining unverified conditions are explicit. For research-only work, provide a complete plan and clearly state that no live integration or payment was executed.
