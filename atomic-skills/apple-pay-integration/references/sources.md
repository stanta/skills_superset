# Primary-source register

Research review date: **2026-10-15**. This is the date of source checking, not the publication date of every page. Sources are mutable; verify the applicable section again before coding, release, a provider upgrade or a storefront-policy decision. Version thresholds in references identify a documented feature boundary, not the latest available SDK.

The skill is an original synthesis. Source-backed product/policy facts are separated from recommended engineering controls. No private project source material or vendor implementation has been copied into the skill.

## Apple policy, platform and merchant setup

- **A1 — Apple Pay implementation options.** https://developer.apple.com/apple-pay/implementation/ — Integration models and the role of participating platforms/processors.
- **A2 — App Review Guidelines.** https://developer.apple.com/app-store/review/guidelines/ — Re-check sections 3.1.1, 3.1.1(a), 3.1.3 and applicable regional provisions. Policy facts are summarized only in the eligibility reference.
- **A3 — Apple Developer Program License Agreement.** https://developer.apple.com/support/terms/apple-developer-program-license-agreement/ — Agreements, attachments and effective dates; do not infer eligibility from a blog or an obsolete fee table.
- **A4 — Configure Apple Pay.** https://developer.apple.com/help/account/capabilities/configure-apple-pay/ — Merchant ID, processing certificate and app capability setup.
- **A5 — Configure Apple Pay on the web.** https://developer.apple.com/help/account/capabilities/configure-apple-pay-on-the-web/ — Web merchant identity, domains and certificate responsibilities.
- **A6 — ApplePaySession.applePayCapabilities.** https://developer.apple.com/documentation/applepayontheweb/applepaysession/applepaycapabilities — Capability API, credential states and presentation obligations; related deprecated API is identified on this page.
- **A7 — ApplePaySession initialization.** https://developer.apple.com/documentation/applepayontheweb/applepaysession/applepaysession — Request construction, supported version, secure context and user-activation requirements. Check the selected API's callback contracts as well.
- **A8 — Requesting an Apple Pay payment session.** https://developer.apple.com/documentation/applepayontheweb/requesting-an-apple-pay-payment-session — Merchant-validation request fields and opaque session lifecycle.
- **A9 — TN3174: Diagnosing payment-sheet issues.** https://developer.apple.com/documentation/technotes/tn3174-diagnosing-issues-with-the-apple-pay-payment-sheet-on-your-website — Especially the cross-environment session change effective **2026-10-01**, session endpoint migration and post-authorization dismissal diagnosis. This date is a migration boundary, not a forecast.
- **A10 — Apple Pay sandbox testing.** https://developer.apple.com/apple-pay/sandbox-testing/ — Sandbox accounts, devices and test cards. This is not a production country-support list.
- **A11 — Countries and regions that support Apple Pay.** https://support.apple.com/en-us/102775 — Current consumer support; merchant acquiring and issuer support still require separate verification.
- **A12 — What's new in Apple Pay.** https://developer.apple.com/apple-pay/whats-new/ — Browser/platform feature changes and cross-device experiences; confirm processor support separately.
- **A13 — Merchant tokens (MPANs).** https://applepaypartners.apple.com/merchants/features/merchant-tokens-mpans — Merchant-token use cases, availability and lifecycle. Apple's https://developer.apple.com/apple-pay/merchant-tokens/ entry point redirects here.

## Processor-specific documentation

- **P1 — Stripe Apple Pay, web.** https://docs.stripe.com/apple-pay?platform=web — Managed merchant validation, web setup and Stripe-specific testing.
- **P2 — Stripe Apple Pay, iOS.** https://docs.stripe.com/apple-pay?platform=ios — Native CSR/certificate/capability setup and confirmation integration. Verify the chosen SDK release rather than treating an example as a version pin.
- **P3 — Stripe payment-method domain registration.** https://docs.stripe.com/payments/payment-methods/pmd-registration?dashboard-or-api=api — Domain and account scope; applies to the selected UI/account model.
- **P4 — Stripe Express Checkout Element.** https://docs.stripe.com/elements/express-checkout-element — Current checkout integration choices, availability and browser considerations. Choose one documented API flow.
- **P5 — Adyen Apple Pay web component.** https://docs.adyen.com/payment-methods/apple-pay/web-component/ — Component availability, browser version boundaries, certificate options and testing.
- **P6 — Stripe webhooks.** https://docs.stripe.com/webhooks — A concrete primary example of signature verification, body handling and asynchronous event delivery. Other processors may sign different material.
- **P7 — Stripe idempotent requests.** https://docs.stripe.com/api/idempotent_requests — A concrete provider's idempotency contract; not a universal retention or retry guarantee.

## Security

- **S1 — OWASP SSRF Prevention Cheat Sheet.** https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html — URL parsing, allowlisting, redirect and network-layer defenses. Apply it to the merchant-validation boundary using current Apple endpoint information.

## Refresh procedure

Open the exact platform/provider variant, confirm effective dates and SDK versions, and compare against the recorded architecture. Record source URL, relevant section, retrieval date, affected decision and reviewer. Where official documents conflict, resolve the exact storefront/platform/version scope before selecting a rule. Do not let marketing summaries override policy or API reference contracts.

Priority refresh triggers: App Store terms changes; support-country changes; changes to merchant session endpoints/environments; certificate rotation; SDK/plugin upgrades; new embedded origins; processor/account-model changes; recurring features. Do not describe a date-sensitive rule as permanently universal.

## Verification boundary

Research and repository validation do not establish merchant approval, legal compliance, payment-network acceptance, successful sandbox execution or production readiness. Those require the environment-specific evidence listed in the plan and testing references. Agent evaluation prompts are provided for future measured runs; no baseline-versus-skill improvement is asserted without such a run.
