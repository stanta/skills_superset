# Dated Google Play policy snapshot

Verified: **2026-10-15**. Source IDs link through [sources.md](sources.md). This is a research snapshot, not a substitute for the app's current console notices or a guarantee of review acceptance. Check primary pages again before every submission, and after a policy notification, SDK change or material feature/data-flow change.

## Numeric and time-sensitive gates

| Topic | Observed rule | Applicability and caution | Source |
| --- | --- | --- | --- |
| Target API for submissions | From 2026-08-31, new mobile apps and updates target Android 16 / API 36 or higher. Wear OS and Automotive OS require API 35; TV and XR require API 34. | Do not copy mobile values to every form factor. minSdk and compileSdk are different settings. Private-app exceptions must be evidenced. | S01 |
| Existing-app availability | Ordinary existing mobile apps need API 35 for continued discovery by new users on newer Android versions. | Availability of an old release is not permission to submit an API-35 update. Existing users and other form factors have distinct rules. | S01 |
| API extensions | The target-API page lists 2026-11-01 as an extension endpoint. | An offered extension is not automatic approval. Record the actual console grant and scope. | S01 |
| Personal-account testing | Personal accounts created after 2023-11-13 require at least 12 testers continuously opted in to a closed test for the preceding 14 days before applying for production access. | Genuine testing, engagement and feedback matter. Meeting this minimum enables an application, not guaranteed access or app approval. Do not invent a required daily session duration. | S04 |
| Developer fee | Play Console registration has a one-time US$25 fee. | Payment methods and country eligibility vary. Do not confuse this with service fees or other Android distribution programs. Payment requires owner authorization. | S02 |
| App registration | The policy-deadline page lists 2026-09-30 for Play app registration under developer-verification requirements. | Check even an existing Play app: automatic registration should not be assumed. This Play obligation is distinct from regional protections for installs outside Play. | S03, S23 |
| Android verification rollout | Protections began 2026-09-30 in Brazil, Indonesia, Singapore and Thailand for participating stores on certified Android 7+ devices; broader expansion is described for 2027. | Do not tell every publisher to create a second account; inspect whether Play Console already handles verification/registration. Recheck region/store scope. | S24 |
| 16 KB page sizes | The current Android compatibility page requires support for apps targeting API 35+ on 64-bit devices; it states that incompatible app updates cannot be released starting 2027-02-01. | Older material cites a 2025 date. Record the live page and app-specific warning, not an assumed universal extension. Verify APK packaging AND ELF alignment AND runtime behavior. Pure Java/Kotlin is not proof that transitive SDKs contain no native code. | S05 |
| Billing Library | Version 7's new-app/update deadline was 2026-08-31, with an extension endpoint of 2026-11-01; version 8's ordinary deadline is 2027-08-31. | For new submissions using Play Billing, use a supported version (normally 8+ at this snapshot) unless the specific app has a valid extension. Inspect the resolved native dependency, not only a Flutter/JS wrapper version. | S10 |
| Listing text | Name: 30 characters; short description: 80; full description: 4,000. Release notes: 500 Unicode characters per language. | Recheck current field rules and localization; these are limits, not targets for keyword stuffing. Asset rules differ by form factor. | S12, S16 |
| Core stability vitals | Overall bad-behavior thresholds: user-perceived crashes 1.09%; user-perceived ANRs 0.47%. Per-phone-model thresholds: 8% for each. | Play visibility thresholds are not good internal SLOs. Rates use Play definitions, not arbitrary session-based crash metrics. Watch models differ. | S25 |
| Battery and upcoming quality gates | Excessive partial wake locks have a 5% overall threshold. Current vitals docs describe possible visibility impact for memory/bitmap/code-optimization issues from February 2027. | Load current metric definitions and exclusions before making a quantitative gate. Measure by version/device, and use stricter evidence-backed internal budgets. | S25 |

## Common requirements and conditional work

### Account, ownership and signing

Choose the account type that truthfully represents the publisher. Organization onboarding normally requires a D-U-N-S number with consistent legal details; documented government/unsupported-region alternatives exist. Verify contacts, payment/merchant information when monetizing, and device verification where required. Never put identity documents or private keys into a skill or repository. [S02, S03]

A new public Play app normally uses Android App Bundle and Play App Signing. Package names are permanent; updates need an increasing versionCode. An upload certificate is not necessarily the certificate signing an installed Play build. Legacy apps created before August 2021 have documented APK/signing exceptions. [S12, S14, S16]

### Data, privacy and reviewer access

Complete applicable Data safety declarations based on actual first-party and third-party behavior, including analytics, crash reporting, ad SDKs and AI processors. A privacy policy must describe real practices, not just repeat a boilerplate. Review current test-track exemptions rather than treating an internal-only exemption as production compliance. [S06, S07, S22]

If account creation falls within the account-deletion policy, provide discoverable in-app initiation and an external deletion-request resource for ordinary mobile apps. Deactivation or uninstalling is not account deletion. Explain legitimate retention and applicable non-mobile/private exceptions; an external flow need not be a fully automated self-service API. [S08]

Complete audience/content-rating/ads and app-access sections accurately. Reviewer credentials must reach the full reviewable experience without inaccessible OTPs, expired invitations or an unavoidable subscription purchase. Use synthetic data and normal documented reviewer access, not a hidden reviewer-only bypass. [S13]

### Conditional modules

- **Digital monetization:** classify every SKU and country/program first. Play Billing is the default for covered in-app digital purchases; physical goods/services are different. Alternative billing and external links require checking the current applicable program, enrollment, APIs/reporting and terms. Google Pay is not a blanket substitute for Play Billing. Do not freeze regional fees into this skill. [S09, S10, S27]
- **Health:** developers on covered closed/open/production tracks complete the Health apps declaration even when the truthful answer is that no health features exist. Additional health-policy obligations apply only where relevant. Assess claimed functionality, health-data access and regulated-device status from evidence; obtaining a store approval is not regulatory clearance. [S11, S22]
- **AI-generated content:** assess policy scope, implement in-app reporting for covered generation, moderation and prohibited-content safeguards. Third-party AI integration does not transfer the developer's user-data obligations to the vendor. [S07, S22]
- **Children, UGC and social:** determine actual target audience and functionality. Do not infer a child-directed audience merely because an adult uses the app to manage family information. Covered apps need the relevant child-safety, Families and UGC controls; anonymous/random chat changes effective 2026-08-26 require particular attention. [S22, S23]
- **Sensitive permissions:** justify necessity against the current permitted use cases. Prefer narrower system APIs and requests at the point of use. Current deadlines include 2027-01-27 changes affecting location, call-log verification and foreground-service geofencing; check exact scope rather than treating every announcement as already enforced. [S13, S23]
- **Other restricted verticals/form factors:** finance, loans, gambling, VPN/accessibility, news, government, health-data APIs, Wear/TV/Auto/XR and games may introduce additional gates. This list is not exhaustive: inspect the live policy index and console declaration queue. [S01, S22, S23]

## Refresh and conflict protocol

For each volatile claim record `source_url`, `verified_at`, `effective_at`, affected apps/tracks/regions, observed console status, approved exception (if any), and next action. Prefer applicable official policy/help pages and account-specific enforcement evidence; use Android technical docs for implementation. A community reply is a lead, not controlling policy. When official pages conflict, preserve both observations, check revision and applicability, and mark the gate unresolved until the controlling source or support clarifies it. Never fabricate a console observation.
