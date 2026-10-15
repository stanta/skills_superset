# Primary sources and freshness ledger

Research date: **2026-10-15**. Reopen applicable sources for each release. These links document evidence, not an authorization to operate an account. Apple rules and regional terms take precedence over framework tutorials. A page's retrieval date is not its effective date.

## Dated requirement snapshot

| Observation | Scope and effective date | Evidence |
| --- | --- | --- |
| Xcode 26 or later and the corresponding version-26-or-later SDKs are the published current minimum for the listed mobile/TV/watch/vision platforms. | Effective 2026-04-28; do not silently apply this list to macOS. | S02 |
| Uploaded iOS/iPadOS apps must target iOS 13 or later. | Effective 2026-09-09; deployment target is distinct from build SDK. | S02 |
| Version-27 SDK requirements and iOS/iPadOS minimum target iOS 15 are announced. | **Future: April 2027** on the inspected submission page; no exact day was stated there. Do not enforce as an October 2026 requirement. | S03 |
| Updated age-rating questionnaire deadline was 2026-01-31. | Existing apps should verify their responses before further submissions. | S02 |
| Developer Program price displayed was USD 99 per membership year. | Region/local currency and eligible fee waivers vary; verify before purchase. | S04 |
| TestFlight limits displayed were 100 internal users, 10,000 external testers and 90-day build availability. | Snapshot, not a capacity or approval guarantee. | S06 |
| Keyword field documentation specifies 100 bytes; the marketing guide says 100 characters. | Preserve this discrepancy. Use a conservative UTF-8 byte check and confirm actual App Store Connect validation for the chosen locale. | S11, S12 |

Do not invent additional deadlines, current commission rates, accepted payment exceptions, exact screenshot dimensions or new country requirements. Record their current authoritative evidence when applicable.

## S01
[App Review Guidelines](https://developer.apple.com/app-store/review/guidelines/). Applicability, completeness, UGC, payments, minimum functionality, login, AI data sharing and sensitive categories. Cite exact section identifiers in task-local assessments. Specialist legal review may be needed; store approval is not legal certification.

## S02
[Upcoming requirements](https://developer.apple.com/news/upcoming-requirements/). Effective dates and affected platforms. Read alongside S03 rather than assuming the newest announcement is already mandatory.

## S03
[Submitting apps](https://developer.apple.com/app-store/submitting/). Current preparation guidance and announced future submission requirements.

## S04
[Developer Program enrollment](https://developer.apple.com/programs/enroll/). Individual/organization eligibility, authority, identity, D-U-N-S, two-factor authentication, membership price and fee-waiver links.

## S05
[Upload builds](https://developer.apple.com/help/app-store-connect/manage-builds/upload-builds/). Supported upload channels, roles, build association and processing. Distinguish its build-tool and upload-client columns; consult S02 for deadlines.

## S06
[TestFlight overview](https://developer.apple.com/help/app-store-connect/test-a-beta-version/testflight-overview/). Tester groups, beta review, expiration and feedback.

## S07
[App Privacy Details](https://developer.apple.com/app-store/app-privacy-details/). Developer and third-party data disclosures, data categories, purpose, linking and tracking.

## S08
[Third-party SDK requirements](https://developer.apple.com/support/third-party-SDK-requirements/). Listed SDKs, manifests, signatures and responsibility for dependencies; inspect the actual versions shipped.

## S09
[User privacy and data use](https://developer.apple.com/app-store/user-privacy-and-data-use/). Tracking definitions, ATT and prohibited fingerprinting; SDK presence alone does not establish tracking.

## S10
[Account deletion](https://developer.apple.com/help/app-review/guideline-reference/5-1-1-account-deletion). Initiation, account/data deletion, subscription considerations and Sign in with Apple token revocation.

## S11
[Platform version information](https://developer.apple.com/help/app-store-connect/reference/app-information/platform-version-information/). Metadata field limits, support URL, previews and release settings. Follow linked screenshot specifications for the actual device families.

## S12
[Creating your product page](https://developer.apple.com/app-store/product-page/). Name/subtitle, screenshots, previews, keywords, localization and reviews. See the keyword-unit discrepancy above.

## S13
[Product Page Optimization](https://developer.apple.com/app-store/product-page-optimization/). Eligibility, treatments and experiment interpretation; recheck supported platforms and assets before proposing a test.

## S14
[Custom Product Pages](https://developer.apple.com/app-store/custom-product-pages/). Audience/campaign-specific product pages and measurement. Not a substitute for truthful app functionality.

## S15
[Phased version updates](https://developer.apple.com/help/app-store-connect/update-your-app/release-a-version-update-in-phases/). Automatic-update rollout, pauses and users' ability to download manually.

## S16
[EU Digital Services Act trader requirements](https://developer.apple.com/help/app-store-connect/manage-compliance-information/manage-european-union-digital-services-act-trader-requirements). Publisher status verification and displayed contact information; do not decide legal trader status from code alone.

## S17
[China mainland compliance](https://developer.apple.com/help/app-store-connect/manage-compliance-information/view-china-mainland-compliance-information). Evaluate required filings/licenses for the actual app and territory; do not generalize to all markets.

## S18
[Encryption documentation](https://developer.apple.com/help/app-store-connect/manage-app-information/determine-and-upload-app-encryption-documentation). Determine export declarations from actual cryptography, exemptions and distribution rather than guessing a Boolean flag.

## S19
[Submit an app](https://developer.apple.com/help/app-store-connect/manage-submissions-to-app-review/submit-an-app). Version/build selection, prerequisites, submission steps and authorized roles.

## S20
[Auto-renewable subscriptions](https://developer.apple.com/app-store/subscriptions/). Product experience, clear terms, subscription lifecycle, offers and testing.

## S21
[App Store Connect API](https://developer.apple.com/help/app-store-connect/get-started/app-store-connect-api/). Automation surface, key management and role boundaries. Discover current endpoints; do not invent API operations.

## S22
[Flutter iOS release guide](https://docs.flutter.dev/deployment/ios). Flutter-specific build, archive and App Store submission adapter; Apple policies remain independent.

## S23
[Expo EAS Submit for iOS](https://docs.expo.dev/submit/ios/). Optional Expo adapter; upload is not App Review submission or public release.

## S24
[Declare regulated medical device status](https://developer.apple.com/help/app-store-connect/manage-app-information/declare-regulated-medical-device-status). Check current form scope for medical functionality; classification requires qualified human evidence.

## Additional technical entry points

[Privacy manifests](https://developer.apple.com/documentation/bundleresources/privacy-manifest-files), [required-reason APIs](https://developer.apple.com/documentation/bundleresources/describing-use-of-required-reason-api), and [App Store Server API](https://developer.apple.com/documentation/appstoreserverapi) were reachable documentation entry points, but their full JavaScript-rendered bodies were not available in this research extraction. Read their current full documentation before implementing exact reason codes, schemas or endpoints; this skill does not claim those details were independently verified.

## Maintenance protocol

Refresh S01-S03 before submission and whenever Apple announces changes. Refresh storefront/payment/export/category sources when those inputs change. Update only facts actually reverified; preserve unresolved conflicts and append effective dates. Re-run structural checks and the evaluation cases after changing guidance. Do not infer future rules from an annual release pattern.
