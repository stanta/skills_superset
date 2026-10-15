# Recurring payments, deferred charges and token lifecycle

Sources: G14, G15 and G16 in [sources.md](sources.md). This is an online Google Pay capability, not a replacement for store billing eligibility or a guarantee that every PSP/wrapper supports it.

## Current request model

Google announced enhanced merchant-initiated transaction (MIT) support on 2026-04-15. The guide checked on 2026-10-15 describes these request alternatives:

| Intent | Top-level request object |
| --- | --- |
| Immediate customer-initiated purchase | `transactionInfo` |
| Repeating charges | `recurringTransactionInfo` |
| One charge at a future time | `deferredTransactionInfo` |
| Balance-triggered replenishment | `automaticReloadTransactionInfo` |

Use **exactly one** transaction-info object per request. Validate the complete current schema for the target surface and adapter rather than transplanting a Web example into an older mobile plugin. Dynamic price updates are currently not supported for MIT requests. [G14]

The new fields describe future billing to the customer and support appropriate credentials; they do not schedule or collect the money. The merchant/PSP remains responsible for charging according to the agreement. Capture the schedule, amount or variable-amount rules, trial/introductory terms, cancellation/management route and evidence of consent. [G15]

## Implementation checklist

1. Establish policy eligibility and processor support for the specific recurring/deferred/reload model.
2. Confirm how the PSP stores the authorized credential and how subsequent MIT operations are marked and linked to the original customer interaction.
3. Build the appropriate request and validate displayed billing terms in `TEST`; do not add `transactionInfo` beside the chosen MIT object as a workaround.
4. Persist the agreement/version, customer and merchant bindings, provider vault reference, lifecycle state and next billing decision. Avoid storing raw one-time wallet payloads.
5. Implement the merchant/PSP billing schedule, bounded retries, receipt/invoice, cancellation, refund and off-session authentication recovery. Do not repeatedly charge on a revoked or disabled credential.
6. Test trial transition, price changes, cancellation races, failed renewal, card replacement, expired credentials and device changes. A valid credential does not authorize charging outside the agreement.

## Token lifecycle management (TLM/LCM)

To receive Google token lifecycle notifications, include the appropriate `tokenUpdateUrl` in the selected MIT transaction-info object. Confirm who owns this URL: a gateway merchant often relies on its PSP for decryption and downstream notifications, rather than building a parallel direct-crypto endpoint. [G14]

For an integrator that owns Google's callback endpoint, the current notification specification requires signature/decryption handling, intended URL validation, `messageId` deduplication and token-state updates ordered by original `timestamp`. Correlate `merchantTokenId` to the right account. The response must echo `requestMessageId`; status values include `SUCCESS`, `TOKEN_NOT_IN_USE` and `TOKEN_NOT_FOUND`. Delivery is best effort with retries, so retain reconciliation and failed-renewal recovery. [G16]

**Observed documentation conflict:** the `targetNotificationUrl` field text mentions HTTP 400 for an incorrect URL, while the same page's response table specifies 401. Reject an invalid target and record this as a source conflict; confirm the expected response with Google/PSP before implementing that branch. Do not invent a definitive wire contract. [G16]

Never confuse token lifecycle notification with a payment-success webhook. A token being active, updated or disabled says nothing by itself about whether an invoice was paid. Likewise, canceling a subscription and disabling a credential are different operations with different authority.
