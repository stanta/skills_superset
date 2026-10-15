# Web and native integration

Source IDs resolve in [sources.md](sources.md). Follow only the route selected in the architecture decision; do not combine a PSP-managed session with custom merchant-validation callbacks.

## Credentials and prerequisites

For a self-managed/native setup, establish the Apple developer team and Merchant ID, enable Apple Pay for the correct app identifier, and configure its Payment Processing Certificate. Match the CSR and private-key owner to the processor that will decrypt payment data. Processing certificates have a 25-month validity period; use actual certificate metadata and a tested rotation procedure rather than a calendar reminder alone. [A4]

For self-managed web acceptance, also configure a Merchant Identity Certificate and verified merchant domains. The identity certificate authenticates server-to-Apple merchant validation; it is not the certificate used to encrypt payment data. HTTPS and domain ownership are prerequisites. Domains and certificates require lifecycle management. A provider may assume some of these responsibilities, so establish ownership before provisioning duplicates. [A5]

Recommended inventory: environment, Apple team, merchant identifier, certificate purpose, key custodian, serial/fingerprint, actual expiry, affected origins/targets, PSP account, rotation owner, replacement test and rollback method. Never put private keys in source control or ship them in a client. Do not revoke the active certificate merely to troubleshoot a new one.

## Web setup checklist

1. Inventory the exact checkout origins, including relevant subdomains, staging, embedded-frame and top-level origins. Register domains through the integration owner's prescribed procedure.
2. Where a domain association file is required, serve the provider/Apple-issued bytes at the prescribed `/.well-known/apple-developer-merchantid-domain-association` location. Test the public HTTPS response, not only a local filesystem file. Check status, redirects, SPA rewrites, authentication, content replacement, CDN caching and WAF challenges.
3. Select the current supported Apple/PSP SDK and record its version or controlled upgrade policy. Load it once. Keep Content Security Policy and iframe permissions as narrow as the supported integration requires.
4. Prepare a server-priced quote before the customer activates payment, with a revision and expiry. Revalidate shipping, tax and discounts when user choices change; do not treat a partial pre-authorization shipping contact as the final address.
5. Present a supported Apple Pay button with accessible labeling and relevant localized totals. Request only contact fields needed to complete this transaction. Preserve another eligible payment option.

For embedded Stripe/Adyen routes, follow their iframe and domain rules rather than assuming that any WebView is equivalent to Safari. Safari 17 introduced the relevant cross-origin `allow="payment"` support; earlier supported combinations have stricter same-origin requirements. The exact processor component and version still matter. [P3, P5]

## Capability detection

Use the actual supported API or PSP component availability result, not a Safari-only user-agent allowlist. Where credential-aware presentation is appropriate, current Apple documentation uses `applePayCapabilities(merchantIdentifier)`; `canMakePaymentsWithActiveCard` is deprecated. `canMakePayments()` tests device support, not a guaranteed usable card. Credential-aware checks also carry Apple's presentation obligations. [A6]

Interpret the statuses deliberately: `paymentCredentialsAvailable` supports a primary but not exclusive option; `paymentCredentialStatusUnknown` still permits offering Apple Pay; `paymentCredentialsUnavailable` can support setup without making it the sole/default choice; `applePayUnsupported` means do not offer it. Unknown credentials are not a failed payment. Supported third-party-browser experiences may complete on another Apple device. [A6, A12]

Keep capability results out of advertising profiles. Feature-detect optional APIs and supported request versions; test the selected PSP fallback when a capability method or SDK cannot load. Do not announce payment success from any capability result.

## Self-managed web session sequence

Create the payment session in a direct user gesture with a supported version and valid request. Avoid unrelated asynchronous work between the click and presentation. Register handlers before beginning; complete each invoked selection/authorization handler using the selected API's current contract. Provider-managed components own their own equivalent lifecycle. [A7]

On merchant validation, send only the required event data plus an authenticated order reference to your server. The server selects the allowed merchant and domain; it must not trust client-selected certificate paths, merchant accounts or arbitrary URLs. Apply the SSRF controls in [backend security](backend-security.md).

Request an opaque merchant session server-side with the identity certificate and the documented fields, including the exact verified domain as `initiativeContext`. It is short-lived (five minutes), must be generated for the transaction, and should not become a shared cache. Return the session without modifying its signed content. Keep it separate from a PSP payment object. [A8]

**Environment change effective 2026-10-01:** Apple no longer supports cross-environment merchant sessions. The Wallet account environment and Apple validation endpoint must agree; PSP test mode is a separate axis. Follow the validated Apple event URL and the provider's testing procedure instead of mechanically replacing production hosts when test keys are used. Apple's TN3174 also notes the migration from `/startSession` to `/paymentSession`. A payment-sheet completion deadline can expire while processing continues, so reconcile ambiguous outcomes instead of issuing a new charge. [A9]

After authorization, submit the token exactly as required by the selected PSP. Complete the UI callback within the applicable deadline; any final order effect must still use verified server evidence. Cleanup handlers/session state on cancellation, navigation or unmount. A customer dismissal does not reverse a charge that already succeeded.

## Native and cross-platform setup

For Swift/UIKit/SwiftUI, use a supported PSP sheet or PassKit flow. Verify Merchant ID consistency across the signed target, Apple account, processing setup and payment request. Include `com.apple.developer.in-app-payments` with the intended merchant IDs in the actual signed entitlements; regenerate/update provisioning as required for each target or flavor. A development setting is not proof that the distribution archive is correctly signed. [A4]

Native Stripe provides a documented Merchant ID/CSR/certificate setup and Apple Pay context integration. Its server-side payment object, SDK confirmation and native completion callback must form one coherent flow; do not mix an old sample with another API version. A processor-generated CSR belongs to that processor's certificate workflow. [P2]

Recommended native implementation controls:

- Build displayed totals from a server quote and use decimal-safe money types, not binary floating-point arithmetic.
- Check device, networks and requested feature support before presenting the sheet. Unsupported Apple Pay does not disable the entire checkout.
- Retain the controller/context for the operation; finish callbacks exactly once and handle cancellation separately from decline or unknown network outcomes.
- Reconcile when the app resumes after termination, backgrounding or loss of connectivity. Do not grant access solely from an in-memory callback.
- Test the release target on physical devices and the actual distribution configuration.

For Flutter or React Native, inspect the maintained wrapper and its underlying native SDK. Record feature parity, minimum deployment targets, plugin version, required entitlements and callbacks. Do not assume that an arbitrary plugin supports merchant tokens, cross-device web checkout, current regional programs or every PassKit field. Keep unsupported platform imports out of shared builds and avoid WebView-based policy workarounds.
