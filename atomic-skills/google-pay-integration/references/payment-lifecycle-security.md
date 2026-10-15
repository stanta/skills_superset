# Payment lifecycle and security

These are recommended architecture controls, adaptable to the selected processor, not Google-defined endpoint names. Sources: [sources.md](sources.md), especially G01, G09, G13, S01 and S02.

## Contracts and state

Use money types appropriate to the PSP/currency: integer minor units where applicable, or validated exact decimal types. Never calculate commercial totals with binary floating point or assume every currency has two decimal places.

A portable contract can expose the following conceptual operations:

| Operation | Responsibility |
| --- | --- |
| Create/refresh quote | Server calculates price, tax, shipping and currency; binds cart, user, merchant, version and expiry. |
| Create/confirm attempt | Authenticates ownership, reserves one logical operation, accepts the opaque credential through the selected adapter. |
| Read order status | Lets the client recover after timeout, redirect, app restart or unknown outcome. |
| Receive PSP notification | Verifies authenticity and applies an idempotent provider-state transition. |
| Capture/void/refund | Authorized server operation with amount limits, persistent idempotency and audit trail. |

Do not blindly trust the client to choose tenant/merchant, PSP account, price, currency, refund recipient or provider transaction ID. Validate body size and schema, CSRF where applicable, order ownership, quote freshness and allowed transitions.

Model payment state separately from order fulfillment. An illustrative model:

```text
CREATED -> REQUIRES_ACTION -> PROCESSING -> AUTHORIZED -> CAPTURED
              |                  |             |
          CANCELED/FAILED      UNKNOWN         VOIDED

CAPTURED -> PARTIALLY_REFUNDED -> REFUNDED
```

This is not an exhaustive provider state machine. Some flows skip authorization-only states, some remain asynchronous, and refunds/disputes may need separate records. Define which authoritative event allows fulfillment. If a business fulfills on authorization, record that risk decision; authorization still must not be labeled capture or settlement.

## Persistent idempotency

Create a server-side attempt before the external economic operation. Bind its key to merchant/tenant, buyer, order, operation and immutable request/quote version. Enforce unique constraints or equivalent atomic storage. Repeated identical calls return the recorded result; a reused key with changed parameters is rejected. Coordinate multiple distinct attempts for one order so that different keys cannot purchase the same order twice.

Use the PSP's own idempotency mechanism where supported and document its retention window, supported operations and error semantics. Stripe's documented mechanism is one concrete example, not a universal PSP contract. [S01]

On a connection failure after submitting a payment, treat the outcome as unknown. Retrieve the existing provider operation, reconcile notifications, or retry the **same** supported idempotent operation. Never create a fresh charge solely because the client did not see success. Retain enough durable state to recover across process crashes and provider idempotency expiry.

Refunds and captures require their own operation keys, permissions and amount checks. Total refunds must not exceed the refundable captured amount; reconcile partial and pending refunds with the provider.

## Notifications and recovery

Use the processor's documented signature validation on the required raw request bytes; support key rotation and replay/time checks as defined by that processor. Validate the intended environment and merchant account. Parse only bounded payloads and validate event types and identifiers. [S02]

Persist a verified event/inbox record before acknowledging, then process idempotently; keep request handling short. Deduplicate by a provider-scoped event identity and by the economic transition where different events describe the same change. Do not assume event order or one-time delivery. Re-fetch the provider resource when necessary; do not regress captured state to pending from an older notification.

Have retry/backoff, dead-letter investigation and a scheduled reconciliation path. Reconcile provider authorization, capture, settlement, fees, refunds and disputes with the internal ledger. Google Pay itself is not the settlement ledger. [G01]

## Authentication, fraud and sensitive data

A device cryptogram is not blanket proof that all transactions meet SCA or liability-shift conditions. Preserve processor-required authentication fields and ECI without inventing values. Use the provider's documented risk/3DS continuation flow, especially for `PAN_ONLY`, and current regional requirements. Client-visible assurance fields must not become a trusted server authorization bypass. [G09, G13]

For gateway integrations, keep tokenization output opaque and short-lived; process it through the exact PSP contract. Never store the raw wallet payload in localStorage, analytics, support tickets or exception attachments. Future charging uses provider-approved vaulted credentials/merchant tokens and a valid agreement, not the original one-time payload.

Keep PSP API secrets and direct-mode private keys in server-side secret management. Separate public configuration (merchant name/ID, allowed networks, public provider parameters) from secrets. Restrict secret access, establish rotation/revocation and redact request bodies before telemetry leaves the trust boundary.

Minimize billing address, shipping address, phone and email collection. Use payment data only for permitted purposes; additional uses may require separate express consent. Mask payment forms and sheets in replay tools. Do not send card details, wallet tokens, addresses or raw error payloads to GA, Sentry, GlitchTip or other analytics/observability vendors. [G12]

## Marketplace and direct-mode boundaries

For platforms, specify merchant-of-record, connected-account ownership, split settlement, chargebacks and refunds using the PSP's supported model. Never put an arbitrary submerchant ID into a Google field to emulate a marketplace.

For approved `DIRECT`, use the documented ECv2 processing implementation and operational key lifecycle; verify signatures before trusting plaintext, recipient/environment binding, key/message expiry and replay defenses. Rotate encryption keys according to current Google requirements and keep attestation obligations current. Gateway mode reduces direct handling but does not erase all merchant PCI/security obligations. [G09, G12]
