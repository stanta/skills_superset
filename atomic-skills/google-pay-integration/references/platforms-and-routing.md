# Platforms, eligibility and integration routes

Source IDs: [sources.md](sources.md). Snapshot: 2026-10-15; refresh before implementation.

## Choose the product and payment policy first

| Context | Decision |
| --- | --- |
| Ordinary website, online card checkout | Evaluate Google Pay with the merchant's PSP and markets. |
| Android physical goods/services | Evaluate Google Pay; separately satisfy app distribution and acceptable-use requirements. |
| Play-distributed digital content, features or subscriptions | Analyze current Play Payments policy and any eligible/enrolled program; use Play Billing absent a verified applicable exception. |
| Mixed physical/digital basket | Classify each purchase and design policy-compliant billing boundaries; a physical item does not automatically exempt the digital component. |
| Flutter/React Native | Choose the actual native/web surface and compatible adapter, not a framework-wide promise. |
| iOS | Do not invent a global native Google Pay card SDK. Evaluate supported web checkout/PSP options and Apple store rules separately. |
| India UPI/intent/QR | Route to the Google Pay India APIs and acquiring PSP; do not reuse global card-token request fields. |
| Passes, loyalty cards, card provisioning, NFC acceptance | Different Google Wallet/issuer/acquirer product; out of scope. |

These are routing rules, not legal advice. Record the specific policy sections, enrollment evidence and effective dates relevant to the merchant. External purchase links and alternative in-app billing are distinct program routes. Do not infer enrollment or quote timeless fee percentages. [P01, I01, G01]

## Adapter selection

**PSP-managed checkout or SDK (recommended starting point).** Reuse a suitable existing integration. Determine which button, readiness, domain registration, Google merchant identifiers and recurring features the provider handles. The PSP's supported countries, currencies, settlement account, capture/refund API and contractual terms remain material. Avoid installing a parallel raw Google Pay flow beside a PSP component without a justified need.

**Google Pay API + gateway.** Set `tokenizationSpecification.type` to `PAYMENT_GATEWAY` and obtain the exact gateway identifier and parameter schema from Google's processor list and the PSP. The generic `gatewayMerchantId` pattern is not the contract of every provider. Google `merchantInfo.merchantId`, gateway identifiers, PSP account IDs and app/package IDs have different roles. Forward the opaque payload in the format required by the PSP; do not decrypt or arbitrarily reserialize it. [G01, G03]

**DIRECT.** Reserve for an eligible PCI DSS-compliant merchant with an assessor-validated environment, operational cryptography ownership and Google's required approval. Third-party gateways cannot treat this route as merchant eligibility. Use maintained Google-compatible verification/decryption libraries and current protocol guidance; validate signatures, recipient binding and expiration, prevent replay and plan key rotation. Do not teach hand-written cryptography or store decrypted credentials casually. [G01, G09]

## Web implementation sequence

1. Serve checkout via HTTPS and check supported platform requirements. Load the official Google-hosted JavaScript library; avoid untrusted mirrors. [G02, G03]
2. Create/reuse the client for the chosen environment. Define API version and `CARD` parameters; the current examples use `apiVersion: 2` and `apiVersionMinor: 0`. Match `PAN_ONLY`/`CRYPTOGRAM_3DS` and networks to actual PSP support. [G03]
3. Evaluate `isReadyToPay` for that configuration; render an official button only on success. Readiness is not authorization or assurance of a successful charge. Do not require an existing saved card by default when an add-card flow is appropriate. [G04, G12]
4. Fetch a server-priced quote before the user clicks. Call `loadPaymentData` directly from user activation; do not insert an unrelated awaited network call before opening the sheet. Disable duplicate launch while a sheet/attempt is active. [G04]
5. Use currency-safe decimal formatting for the display total and persist the authoritative money representation on the server. Set final/estimated status truthfully; handle changes by re-quoting and obtaining the user's approval, never silently increasing a charge.
6. Send wallet output to the backend/PSP adapter. If using authorization callbacks, derive the reported result from authoritative processing. Both authorization and dynamic-update callbacks currently have a 30-second response limit; budget dependencies below it and recover unknown outcomes. [G04]
7. For shipping/promotions, support recalculation and relevant error intents; process out-of-order quote responses safely. Intermediate data is not a paid order. Avoid dynamic pricing in a MIT request where currently unsupported. [G14]
8. Test CSP, frame/permissions policy, redirects, user activation and fallback in the actual deployment. Apply the current Google/PSP framing requirements rather than guessing that all iframes are supported.

A schematic flow, **not a complete runnable integration**:

```text
server quote + configured PSP adapter
  -> capability check -> official button
  -> synchronous user-gesture wallet request
  -> opaque credential -> authenticated payment attempt
  -> PSP authorization / required action / capture
  -> verified server state -> fulfillment + receipt
```

## Android

Use the Google/PSP-supported native integration, current wallet dependency, capability check, official button and a lifecycle-safe payment result handler. Handle configuration changes, app backgrounding and process death without generating a second charge. Always re-read server order status on resume.

The Android setup page body checked on 2026-10-15 specifies `minSdkVersion 23`, `compileSdkVersion 34` and illustrates `play-services-wallet:20.0.0`; its generated summary still says minimum SDK 21. Treat the body as the stronger source, verify the selected dependency's actual requirements, and separately satisfy the current Play target-SDK policy. These are a dated snapshot, not permanent dependency pins. [G06]

Production uses the release signing identity, not the debug key, and `WalletConstants.ENVIRONMENT_PRODUCTION`. Confirm the actual package and Play-distributed artifact, including Play App Signing where used. Test the real release delivery route, not just a debug APK. [G08]

## Flutter and React Native

Google's Android guides link official Flutter and React Native resources. Use those or a suitable maintained PSP SDK, inspecting current platform/SDK support and request-field coverage. A plugin's Apple Pay support on iOS is not proof of Google Pay native-card support there. [G06, F01, F02]

Inventory native build configuration, resolved dependency versions, state restoration, environment-specific configuration and the exact token-forwarding contract. Test readiness false, widget/view unmount, canceled sheets and interrupted returns. Verify that newer MIT fields survive the wrapper unchanged; use a supported alternative or explicitly defer the feature if the wrapper lacks it.

## Android WebView

Complete Web integration **and** required Android app approval. The current guide requires Play services 25.18.30+ and WebView 137+, with a WebKit 1.14.0 dependency example. Feature-detect `PAYMENT_REQUEST`, explicitly enable it, and declare the documented payment intents in manifest queries. Custom user agents need the documented `GOOGLE_PAY_SUPPORTED` marker only on a genuinely supported integration. Do not spoof support to bypass checks. [G07]

Do not intercept payment traffic into a third-party HTTP client; the guide explicitly excludes that pattern. Restrict navigation to trusted checkout origins and remove unneeded JavaScript bridges. Older devices get a supported alternative, not a broken button. PWA/TWA packaging does not remove store payment rules.
