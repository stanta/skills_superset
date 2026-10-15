# Backend and security

These are recommended provider-neutral engineering invariants. Provider API details must be taken from the selected adapter. Source IDs resolve in [sources.md](sources.md).

## Minimal portable API contract

Names below are illustrative, not mandatory framework or route names.

| Operation | Client supplies | Server controls and verifies |
| --- | --- | --- |
| Create/update quote | Product choices, allowed quantity, shipping selection | Ownership, catalog prices, discounts, tax, currency, expiry and revision |
| Create payment attempt | Order ID, accepted quote revision, operation key | Payable state, processor account, amount, currency, capture mode and idempotency scope |
| Validate merchant, only for self-managed web | Required Apple event URL, order reference | Allowed origin, merchant identity, target endpoint and matching environment |
| Confirm through processor | SDK-defined wallet/confirmation data | Binding to the expected attempt and processor contract |
| Read payment status | Authenticated order/attempt reference | Object authorization and latest reconciled state; no private payloads |
| Process webhook | Processor event | Authenticity, account, environment, object binding and replay protection |
| Refund or cancel | Authorized business request | Remaining refundable/cancelable amount, permissions and separate operation idempotency |

Use a currency-aware decimal/minor-unit conversion; do not assume every currency has two decimals. Store monetary values without floating-point rounding and make the displayed quote correspond to the intended authorization. The server must reject a stale or tampered quote rather than silently authorizing a different amount.

## Durable idempotency

Recommended key scope: merchant account, environment, order, attempt revision and operation. Persist the key, canonical request fingerprint, provider reference and outcome. A repeated request with the same semantics returns the existing result; reuse with conflicting semantics is rejected. Use the provider's idempotency facility as an additional boundary, not as a replacement for your business ledger. Provider retention and error-caching semantics differ. [P7]

Disabling the button prevents some double-clicks but does not protect against retries, two devices or concurrent workers. Enforce database uniqueness and transactionally guard business effects.

After an ambiguous timeout, retain `unknown/reconciling`; retrieve the original processor object or wait for verified events. Never choose a new idempotency key, new processor or fresh wallet authorization just to clear a spinner. A new attempt requires evidence that the previous attempt cannot complete, or an explicitly controlled duplicate-payment handling policy.

## Financial state and fulfillment

Represent authorization, capture, settlement, cancellation, partial/full refund and dispute information separately where needed. Do not force them into a single numerically increasing status. An authorized payment may still need capture; captured funds may later be refunded or disputed.

A recommended flow is:

```
server quote -> durable attempt -> processor authorization/confirmation
                                      |
                         verified webhook or status reconciliation
                                      |
                    transactional financial event + business effect
                                      |
                              outbox -> downstream fulfillment
```

The payment sheet is a presentation surface, not the business source of truth. The server may reconcile through an authenticated provider status API as well as webhooks. Define the business's fulfillment point explicitly (for example, verified capture), and document how cancellations, refunds and disputes affect access, shipment or credits.

## Webhook handling

Follow the processor's signature scheme with its official verification library. For schemes such as Stripe's, preserve the raw request body before parsing; do not invent a universal JSON reserialization/HMAC format. Authenticate before treating event data as payment evidence. [P6]

Recommended processing pattern:

1. Validate signature, required freshness/replay controls, expected account and environment. Reject unsupported event types and unrelated objects.
2. Durably insert a sanitized inbox record with a unique provider/account/environment/event key before acknowledging receipt. If persistence fails, do not send a success acknowledgement.
3. Process in a retryable worker. Bind the event to the known attempt, check amount/currency and validate state against current provider evidence when events conflict.
4. In one transaction, append the financial event and apply each allowed business effect at most once; use an outbox for asynchronous downstream work.
5. Dedupe by business effect as well as event ID: two different event types can describe the same payment success. Handle late and out-of-order events without rolling a refunded payment back to paid.

Delivery is not magically exactly-once. The goal is replay-safe business effects on top of retryable delivery, plus monitoring and reconciliation for incomplete work.

## Merchant-validation SSRF boundary

A customer-controlled `validationURL` is not permission for a general outbound proxy. Build a maintained allowlist from the current Apple documentation for the selected integration/environment. Validate parsed HTTPS scheme, exact approved host, port and permitted path; disallow userinfo, misleading suffixes, private/local destinations and unsupported URL forms. Reject redirects rather than forwarding client certificates to another host. Protect DNS resolution/rebinding, apply outbound network restrictions, bound time/body size, and keep TLS verification enabled. [S1]

Authenticate and rate-limit the endpoint, authorize the order, and enforce allowed application origins with appropriate CSRF protection for cookie-based sessions. Origin headers alone are not merchant identity. The server, not an arbitrary request body, chooses the merchant account, certificate and verified domain.

## Privacy, compliance and key custody

Redact encrypted payment tokens, payment credentials, client secrets, contact details and certificate material from tracing, logs, analytics and crash reports. Do not add health, identity, family or other sensitive domain context to processor metadata. Use opaque internal references and a minimal operational error taxonomy.

Use a secret manager or similarly controlled facility for server credentials, with rotation, access audit and separate environments. Browser publishable keys and merchant identifiers are not decryption keys; do not accidentally expose secret keys through public environment-variable prefixes.

Tokenization does not by itself establish PCI compliance, remove authentication obligations, or eliminate disputes. Determine the applicable scope with the processor/acquirer and security/compliance owner. Self-managed token decryption is a deliberate scope increase, not a performance shortcut. Never implement custom payment cryptography from an illustrative snippet.
