# Optional provider adapters

Source IDs resolve in [sources.md](sources.md). These are examples, not a default provider selection or an endorsement. Confirm current merchant-country eligibility, supported product category, API version and contract before choosing a processor. Do not make a provider-specific route part of the portable core.

## Adapter contract for any PSP

Record supported channels; account/submerchant model; hosted versus embedded versus native UI; certificate/CSR/key ownership; domain registration; merchant-validation owner; payment-object creation and confirmation; idempotency semantics; authenticated events/status APIs; authorization/capture/refunds; recurring vault/MPAN behavior; testing; and SDK lifecycle/deprecation policy.

Implement domain operations such as `create_attempt`, `retrieve_status`, `capture`, `cancel`, `refund` and `verify_event` behind a typed adapter. Map provider states explicitly to the internal financial model. Do not pass one provider's encrypted token, client secret or idempotency key to another provider.

## Stripe: web

Stripe's Apple Pay web route manages merchant validation, Merchant IDs and related certificate plumbing; do not add a parallel custom validation server. Hosted Checkout/Payment Links differ from Elements or embedded checkout, where your relevant domains must be registered. Direct charges in Connect require the appropriate connected-account domain registration rather than assuming platform registration covers everyone. Testing is described in the separate environment matrix. [P1, P3]

For new custom web checkout, evaluate Checkout Sessions with Express Checkout Element first. Stripe also supports a lower-level PaymentIntents route for requirements that need it. Choose the matching current initialization and confirmation contract; do not splice code from the two flows. Express Checkout Element is the modern wallet component to consider instead of starting with legacy Payment Request Button examples. Browser/device availability depends on the actual component configuration and version, not a handwritten Safari filter. [P4]

Recommended adapter acceptance tests: top-level/iframe origin variants; direct versus platform charge ownership; stable server-created payment objects; duplicate webhook effects; cancellation; return/status recovery; and unknown confirmation outcomes. Keep Stripe client secrets scoped to their intended client operation and out of logs.

## Stripe: native

Use the selected supported Stripe iOS payment UI or Apple Pay context integration. Configure Merchant ID, Stripe-generated CSR and processing certificate, then the correct Xcode capability. Keep server-side PaymentIntent creation, native SDK confirmation and completion callbacks on the same documented flow. Flutter/React Native wrappers must be checked against their underlying SDK. Do not assume web-managed certificates eliminate native setup, and do not revoke production credentials as a first debugging step. [P2]

## Adyen: web

Choose the Sessions or advanced payments flow deliberately and use the matching Apple Pay Component lifecycle, including its availability check. Determine whether Adyen or the merchant owns certificates and merchant validation. Adyen documents third-party-browser/cross-device support in its Apple Pay web component from version 6.10.0; this is a documented minimum for that feature, not a claim about the latest release. Earlier versions and embedded origins need their own compatibility checks. Use Adyen's documented Apple sandbox testing route, and separately verify recurring/tokenization support before advertising renewals. [P5]

## Other providers or direct acquiring

Do not claim compatibility merely because a provider accepts cards. Ask for explicit Apple Pay support for the merchant country, currencies, networks, platform and recurrence model. Prefer provider-maintained documentation and SDKs over an old third-party plugin tutorial. For direct decryption, obtain a reviewed acquiring/cryptographic design and compliance scope; this skill intentionally supplies no custom token-decryption implementation.

## Migration review

When replacing an SDK/provider, compare capabilities, callback timing, token/vault portability, certificate owners, saved mandates and domain onboarding. Existing recurring credentials may not be portable. Preserve the old processor's reconciliation, refund and dispute support while new attempts move to the new adapter. Never use a timeout as an automatic cross-provider failover signal.
