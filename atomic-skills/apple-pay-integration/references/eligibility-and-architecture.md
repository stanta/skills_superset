# Eligibility and architecture

Reviewed 2026-10-15. Source IDs resolve in [sources.md](sources.md). The decision workflow below is a recommended engineering control; it does not replace Apple agreements, processor underwriting or professional legal review.

## Classify the transaction before the technology

Apple Pay supplies a wallet payment experience and token; a payment service provider (PSP), acquirer and merchant account still determine processing and settlement. It is not a substitute name for Apple's in-app purchasing system. [A1]

For App Store distribution, classify each product separately. Digital functionality, content and subscriptions consumed in the app generally belong on the in-app purchase path. Physical goods or services consumed outside the app use other payment methods. Real-time one-to-one services have a distinct exception; one-to-many services and automated AI responses should not be relabeled as that exception. Approved nonprofit fundraising has separate requirements. External-purchase links or alternative payment programs are storefront- and agreement-specific; a US linking allowance is not global permission for an embedded wallet checkout. Verify current sections 3.1.1, 3.1.1(a) and 3.1.3 rather than freezing an exception matrix here. [A2]

A normal website may sell digital access through a PSP, but whether its purchase link, button or embedded flow can appear in a distributed native app is a separate review. For changing regional programs, record the applicable storefront, distribution method, entitlement/agreement, disclosures, reporting obligations, fees and policy-review owner. Re-check current developer terms, especially when their effective date changes. [A3]

## Required decision record

| Dimension | Evidence to collect | Do not infer from |
| --- | --- | --- |
| Product classification | What is purchased, who supplies it, where consumed | Marketing label such as membership or consultation |
| Distribution | Web, App Store, alternative distribution, embedded browser | Shared source code or common checkout UI |
| Merchant eligibility | Approved entity, PSP account, supported acquiring region | Customer language or developer residence |
| Wallet availability | Current country/issuer/device/network support | Test-card country lists or an old article |
| Currency and capture | PSP capabilities, quote currency, authorization/capture rules | UI locale or a fixed two-decimal conversion |
| Recurring billing | Consent, provider tokenization, renewal ownership | One successful initial wallet payment |
| Commercial ownership | Merchant of record, marketplace/submerchant, refunds and disputes | Which company hosts the frontend |

Apple's current supported-country list and its sandbox test-card catalog serve different purposes. A country or card appearing in a testing document is not proof of production acceptance. Check the processor and issuer as well as Apple. [A10, A11]

If a prerequisite cannot be established, continue with a provider-neutral plan and mark launch blocked. Do not fabricate a merchant country, processor approval, Apple entitlement or legal exception.

## Choose an ownership model

| Model | Appropriate starting point | Ownership to make explicit |
| --- | --- | --- |
| Hosted PSP checkout | Fastest supported path for a permitted web purchase | PSP-hosted origins, merchant account, return/status flow, webhook fulfillment |
| PSP-managed web component or native payment sheet | Branded checkout without owning all wallet plumbing | Your origins/app targets; PSP validation/token handling; your order ledger |
| Direct Apple Pay JS or PassKit plus PSP processing | A documented requirement not served by managed UI | Session/callback code, certificate roles, networking, provider token submission |
| Direct decryption/acquiring integration | Only with a supported acquiring contract and dedicated security ownership | Cryptography, key custody, payment-network integration and assessed compliance scope |

Prefer the least custom implementation that satisfies the actual requirements. Apple documents multiple PSP and platform integration options; do not make one vendor mandatory. [A1]

A responsibility matrix should include: merchant identifiers; identity/processing certificate creation and renewal; domain registration; private-key custody; merchant validation; wallet token submission; payment authorization/capture; webhook authentication; order fulfillment; recurring mandates; customer support; refunds; disputes; incident response.

Keep these models separate in a shared backend:

- `order`: what the customer is buying and the authoritative price revision;
- `payment_attempt`: one scoped attempt and its processor reference;
- `financial_event`: authorization, capture, refund or dispute evidence;
- `entitlement` or `fulfillment`: the business effect, independently replay-safe;
- `subscription`: contract and renewal lifecycle, not a raw wallet token.

Shared application code may route to different payment mechanisms. Share domain contracts and reconciliation, not an unconditional Apple Pay button on every platform.
