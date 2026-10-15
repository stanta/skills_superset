# Primary sources and freshness ledger

Research snapshot: **2026-10-15**. This date is a retrieval/review date, not a promise of future validity. Use the current Google page body, current PSP contract and the actual released SDK for implementation. Recheck store policies, availability, SDK requirements, MIT coverage and approval requirements before release. No project-specific account eligibility was verified.

## Source map

| ID | Primary source | Used for |
| --- | --- | --- |
| G01 | [Google Pay Web overview](https://developers.google.com/pay/api/web/overview) | Token-to-processor flow; gateway versus DIRECT; merchant eligibility. |
| G02 | [Web setup](https://developers.google.com/pay/api/web/guides/setup) | HTTPS and supported web integration environment. |
| G03 | [Web tutorial](https://developers.google.com/pay/api/web/guides/tutorial) | Request construction, tokenization and processor-specific parameters. |
| G04 | [Web client reference](https://developers.google.com/pay/api/web/reference/client) | User activation, readiness, callbacks, errors and prefetch limitations. |
| G05 | [Publish a Web integration](https://developers.google.com/pay/api/web/guides/test-and-deploy/publish-your-integration) | Console registration, domain, review and production environment. |
| G06 | [Android setup](https://developers.google.com/pay/api/android/guides/setup) | Native dependencies, platform prerequisites and framework resources. |
| G07 | [Google Pay in Android WebView](https://developers.google.com/pay/api/android/guides/recipes/using-android-webview) | Runtime feature detection, versions, manifest queries, user agent and approval. |
| G08 | [Publish an Android integration](https://developers.google.com/pay/api/android/guides/test-and-deploy/publish-your-integration) | Application review, release signing and production configuration. |
| G09 | [Payment-data cryptography](https://developers.google.com/pay/api/web/guides/resources/payment-data-cryptography) | DIRECT verification/decryption, key lifecycle and authenticated payment data. |
| G10 | [Test card suite](https://developers.google.com/pay/api/web/guides/resources/test-card-suite) | TEST defaults; gateway cards versus mock data; testing limitations. |
| G11 | [Brand guidelines](https://developers.google.com/pay/api/web/guides/brand-guidelines) | Official buttons, presentation and brand requirements. |
| G12 | [Integration checklist](https://developers.google.com/pay/api/web/guides/test-and-deploy/integration-checklist) | UX, payment data minimization and release checks. |
| G13 | [Strong customer authentication](https://developers.google.com/pay/api/web/guides/resources/sca) | Authentication responsibility and assurance-related integration choices. |
| G14 | [Merchant-initiated transactions](https://developers.google.com/pay/api/web/guides/resources/merchant-initiated-transactions) | Recurring, deferred and automatic-reload request objects; current limitations. |
| G15 | [MIT enhancements announcement, April 15, 2026](https://developers.googleblog.com/new-enhancements-for-merchant-initiated-transactions-with-the-google-pay-api/) | Release context and merchant responsibility for future charging. |
| G16 | [Token lifecycle management](https://developers.google.com/pay/api/web/guides/resources/token-lifecycle-management) | Notification validation, ordering, response contract and retry behavior. |
| P01 | [Google Play Payments policy](https://support.google.com/googleplay/android-developer/answer/9858738) | Digital/physical purchase routing and program-dependent exceptions. |
| I01 | [Google Pay India Android overview](https://developers.google.com/pay/india/api/android/overview) | Separation of India UPI from global online card APIs. |
| F01 | [Google Pay Flutter plugin](https://github.com/google-pay/flutter-plugin) | Official framework reference; verify actual package/platform capabilities. |
| F02 | [Google Pay React Native integration](https://github.com/google-pay/react-native-make-payment) | Official framework reference; verify current bridge coverage. |
| S01 | [Stripe idempotent requests](https://docs.stripe.com/api/idempotent_requests) | A primary PSP example, not a universal retention or retry contract. |
| S02 | [Stripe webhooks](https://docs.stripe.com/webhooks) | A primary PSP example for signed delivery, duplicates and asynchronous handling. |

Sources are navigational references, not bundled third-party SDKs or copied documentation. Read the selected PSP's own documentation before mapping its token, capture, recurring and webhook APIs. Stripe is an example only; choosing it is not a requirement.

## Observed source conflicts

| Observation on research date | Treatment |
| --- | --- |
| G06 generated summary says minimum SDK 21, but page body says 23. | Prefer the body and verify resolved SDK requirements. Do not silently combine incompatible versions. |
| G10 generated summary retains opt-in-group wording, but page body says test cards are enabled by default in TEST. | Use the body and verify the actual test-account experience; mock output is still not PSP processing evidence. |
| G16 `targetNotificationUrl` text describes HTTP 400 for a mismatch; its response table describes 401. | Reject invalid targets; confirm the required error contract with Google/PSP before shipping that branch. |

An official page can contain stale examples or generated summaries. Record the URL, section, checked date, SDK/PSP version and the unresolved conflict. If a material requirement cannot be verified, mark the dependent step `blocked` or `requires_verification`; do not invent approval or compatibility.

## Fact versus design recommendation

The Google/Play sources establish API and policy constraints. Persistent order state, scoped idempotency, durable notification inboxes, tenant binding, consent records, reconciliation and feature-flag rollout are recommended application controls. Endpoint names, state diagrams, plan templates and metrics in this skill are illustrative engineering designs, not Google API mandates.

## Refresh protocol

At implementation kickoff and before production: revisit P01; verify Google and PSP merchant/market availability independently; check G02/G06/G07 and resolved dependencies; check G05/G08 approval status; and revalidate G14/G16 when MIT is in scope. Log changed facts and rerun affected acceptance cases. Do not assume a provider list, release date or a successful test proves a particular merchant account is approved.
