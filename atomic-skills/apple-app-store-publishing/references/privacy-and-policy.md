# Privacy, payments and conditional policy gates

Use [S01](sources.md#s01) for exact policy text and [S07-S10](sources.md#s07) for operational privacy guidance. All engineering controls below are recommended evidence practices unless a cited Apple requirement is identified. Do not present them as a substitute for legal advice.

## Data-flow evidence before declarations

Inventory every data path across the app, backend and third parties, including analytics, attribution, crash reporting, session replay, support tools and AI providers. Inspect versions and runtime configuration, not only package names.

Use a register with:

`data | collection point | purpose | linked to identity? | tracking? | recipients | retention/deletion | consent/permission | shipped SDK | declaration | evidence`

Reconcile four different surfaces: App Store privacy answers, the accessible privacy policy, runtime permission/consent behavior, and bundled privacy manifests/SDK requirements. They are not interchangeable. Include third-party behavior in the assessment. [S07](sources.md#s07), [S08](sources.md#s08)

Inspect the final archive for manifests, approved required-reason API declarations and applicable SDK signatures. Select reason codes only from current Apple documentation and only for the actual use. A copied manifest or an SDK vendor's marketing statement is not implementation evidence. Do not claim a complete required-reason API audit from a source-code grep alone.

Test denied, restricted, granted and revoked permission states where supported. Prefer data-minimizing system pickers over broad permissions where suitable. Review logs, screenshots, crash breadcrumbs and support exports for accidental sensitive content. Redaction and sampling are engineering choices that should have regression tests.

## Tracking and AI

ATT concerns tracking as Apple defines it; it is not a universal prompt required by all first-party analytics. Neither a non-advertising label nor an SDK name proves that tracking does not occur. Verify actual linking/sharing and SDK initialization before selecting the declaration. Do not fingerprint or condition ordinary access on ATT approval. [S09](sources.md#s09)

For personal data shared with third-party AI, evaluate the explicit disclosure and permission obligation in Guideline 5.1.2(i). Test the refusal path and verify the network boundary before permission. Do not assume a privacy-policy link, an OS camera prompt or a broad terms checkbox necessarily satisfies the specific data-sharing flow. [S01](sources.md#s01)

## Accounts and authentication

Map account creation to a discoverable account-deletion initiation flow, including temporary/automatically created accounts where applicable. Verify deletion semantics, permitted retention, processing status and affected processors. Deactivation is not automatically deletion. Account deletion and cancellation of an App Store subscription are separate operations; communicate the consequence clearly. For Sign in with Apple, include token-revocation handling where applicable. Use synthetic accounts for destructive tests. [S10](sources.md#s10)

Assess Guideline 4.8 for third-party/social primary login and its exceptions. Do not require Sign in with Apple merely because any login exists; document how an applicable equivalent-login requirement is met. [S01](sources.md#s01)

## Payment classification before implementation

Record `product -> consumption context -> customer type -> storefront -> applicable rule/entitlement -> payment method`.

Digital functionality/content generally follows In-App Purchase rules; physical goods/services consumed outside the app follow a different route. Apple Pay is not a generic replacement for digital IAP. Evaluate reader, enterprise, person-to-person and regional exceptions individually; external purchase links and native alternative payment processing are different capabilities. Never extrapolate a US-storefront or EU-specific rule worldwide. [S01](sources.md#s01)

Engineering recommendations for paid digital entitlements:

- Use supported StoreKit/purchase APIs and authoritative transaction verification; do not unlock durable access from an untrusted client Boolean.
- Isolate sandbox and production. Bind transaction ownership carefully; process retries, duplicates and out-of-order notifications idempotently.
- Test purchase success, cancellation, pending approval, restore/reinstall, renewal, expiration, refund/revocation, billing retry and grace-period behavior where applicable.
- Show localized price, duration, renewal/trial terms and access scope before commitment. Avoid accidental duplicate subscriptions. Provide appropriate restoration and subscription-management access.
- Reconcile product IDs, subscription groups, localization, availability, agreements and review state. Do not promise a particular commission rate without checking the publisher's current program and regional terms.

See [S20](sources.md#s20) and the current server documentation entry points in [sources.md](sources.md) before implementing exact notification schemas or endpoints.

## Conditional policy modules

Activate only the applicable rows; require a reason for non-applicability.

| Trigger | Assessment and evidence to produce |
| --- | --- |
| UGC, public chat or creator content | Moderation, reporting, abuse response and age/access controls assessment under 1.2/4.7. |
| Children as intended users | Kids Category and children's data requirements; distinguish a parental gate from legal consent. |
| Medical/health claims or sensitive records | Qualified classification, claims evidence, data restrictions, required publisher entity and current medical-device declaration. |
| AI or mini-app platforms | Evaluate data sharing and the actual applicability of 4.7; do not classify every AI-enabled app identically. |
| Financial, gambling, VPN or other regulated activity | Specialist review of licensing, publisher identity and territory restrictions. |
| Thin wrapper/template-generated app | Demonstrable value and completeness under 4.2/4.3; do not hide behavior from reviewers. |

Policy entry point: [S01](sources.md#s01). For medical declaration forms, use [S24](sources.md#s24). Store acceptance is not regulatory approval; a disclaimer alone is not evidence of classification or safety.

## Territory and export checks

For EU distribution, evaluate and verify the publisher's DSA trader declaration and contact information; legal status is a human decision. [S16](sources.md#s16)

For mainland China or other regulated markets, check current category-specific filings, licenses and availability restrictions before choosing worldwide distribution. Do not apply a China-only requirement to every release. [S17](sources.md#s17)

Determine export answers from cryptography actually present in the app and dependencies, applicable exemptions and Apple's questionnaire. Do not set `ITSAppUsesNonExemptEncryption` to false simply because the app uses HTTPS or because a template does so. Obtain qualified review when classification is unclear. [S18](sources.md#s18)

## Exit gate

Declarations, privacy policy, binary, SDK behavior and backend processing agree; applicable permission and deletion paths have test evidence; payment routing has a dated storefront-specific rationale; unresolved legal or regulatory decisions have named owners. Missing evidence remains `BLOCKED`, not a guessed pass.
