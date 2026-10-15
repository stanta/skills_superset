# Primary-source ledger

Research verified on **2026-10-15**. Descriptions below are original summaries/navigation, not copied policy text. This independently authored skill is not affiliated with Google and does not certify compliance. Reopen the linked primary pages before a real submission. A URL and verification date describe evidence inspected, not an assurance that the page cannot change later.

## S01 — Target API levels

[Google Play target API requirements](https://support.google.com/googleplay/android-developer/answer/11926878?hl=en). Submission versus existing-app availability; form-factor exceptions; effective dates and extension process. Recheck every submission.

## S02 — Developer account setup

[Get started with Play Console](https://support.google.com/googleplay/android-developer/answer/6112435?hl=en). Account registration, fee, identity/device verification and linked testing requirements. Recheck onboarding and country/payment eligibility.

## S03 — Required publisher information

[Required information to create an account](https://support.google.com/googleplay/android-developer/answer/13628312?hl=en). Personal/organization identities, D-U-N-S, documented alternatives, verified contacts and merchant setup. Recheck publisher/account changes; never copy private identity evidence into the skill.

## S04 — Personal-account testing

[App testing requirements for new personal developer accounts](https://support.google.com/googleplay/android-developer/answer/14151465?hl=en). Closed-test eligibility, continuous opt-in, feedback and production-access application. Recheck account creation date and current console eligibility.

## S05 — Native page-size compatibility

[Support 16 KB page sizes](https://developer.android.com/guide/practices/page-sizes). Native/transitive library detection, ELF and package alignment, build guidance, runtime tests and current Play enforcement language. High-volatility deadline: recheck every release and preserve any conflicting official notices.

## S06 — Data safety

[Provide information for the Data safety section](https://support.google.com/googleplay/android-developer/answer/10787469?hl=en). Collection/sharing definitions, SDK responsibility, disclosures and scope/exemptions. Recheck after a feature, SDK, processor or data-flow change.

## S07 — AI-generated content

[AI-Generated Content policy](https://support.google.com/googleplay/android-developer/answer/13985936?hl=en). Scope, prohibited output and in-app reporting requirements. Read together with S22 for third-party AI/user-data responsibility.

## S08 — Account deletion

[Understanding app account deletion requirements](https://support.google.com/googleplay/android-developer/answer/13327111?hl=en). Applicability, in-app and external request paths, retention and non-mobile/private exceptions. Recheck against the actual account lifecycle.

## S09 — Payments policy

[Understanding Google Play's Payments policy](https://support.google.com/googleplay/android-developer/answer/10281818?hl=en). Digital versus physical purchases, consumption-only scenarios and conditions for other payment paths. Follow its current policy/program links; geography and enrollment matter.

## S10 — Billing Library support window

[Google Play Billing Library version deprecation](https://developer.android.com/google/play/billing/deprecation-faq). Version-specific submission and extension deadlines. The inspected page was updated 2026-09-09. Recheck the resolved Android dependency, not just a wrapper package.

## S11 — Health declaration

[Health apps declaration form](https://support.google.com/googleplay/android-developer/answer/14738291?hl=en). Covered tracks/developers, explicit no-health declarations and health-feature categories. Additional medical/privacy requirements must be checked through the live policy links for the specific functionality.

## S12 — App setup and store assets

[Create and set up your app](https://support.google.com/googleplay/android-developer/answer/9859152?hl=en) and [preview assets](https://support.google.com/googleplay/android-developer/answer/9866151). Package/version rules, store text fields, contact details, localization and form-factor-specific asset constraints.

## S13 — Review preparation

[Prepare your app for review](https://support.google.com/googleplay/android-developer/answer/9859455). App access, ads, target audience/content, privacy and sensitive-permission declarations. Recheck the actual App content queue; the list may evolve.

## S14 — Signing

[Sign your app](https://developer.android.com/studio/publish/app-signing). Play App Signing, upload versus app-signing keys, certificates, recovery and supported legacy paths. Keep key material outside documentation and source control.

## S15 — Bundle inspection

[bundletool](https://developer.android.com/tools/bundletool). AAB-to-APK testing, device-specific sets and size inspection. The inspected page was updated 2026-08-28. APK tools must not be misapplied to AAB signatures.

## S16 — Release process

[Prepare and roll out a release](https://support.google.com/googleplay/android-developer/answer/9859348?hl=en). Track/release setup, review errors, notes and first-release versus update rollout options. Recheck the console's current state before any write.

## S17 — Publication timing

[Control review and publishing](https://support.google.com/googleplay/android-developer/answer/9859654?hl=en). Managed-publishing eligibility and processing/review behavior. Do not promise an exact approval date or initial-publication availability of managed publishing.

## S18 — Publisher API setup

[Google Play Developer API getting started](https://developers.google.com/android-publisher/getting_started). Authentication, API access and Play permissions. Use least privilege and the actual supported credential mechanism.

## S19 — Transactional edits

[Publisher API edits](https://developers.google.com/android-publisher/edits). Grouping changes, commit semantics, bootstrap limitations and invalidation from concurrent console/API changes. Check resource reference pages: not every API method belongs to an edit.

## S20 — Flutter adapter

[Build and release an Android app](https://docs.flutter.dev/deployment/android). Flutter's supported release/signing/build workflow and Android configuration. This is an optional stack adapter, not a mandatory technology choice.

## S21 — Expo adapter

[Submit to Google Play with EAS Submit](https://docs.expo.dev/submit/android/). Optional hosted submission, profile/credential setup and CI integration. Recheck bootstrap and profile details; do not assume the example's automatic main-branch submission is appropriate for a project.

## S22 — Policy changes and live domain routing

[Policy announcement: July 15, 2026](https://support.google.com/googleplay/android-developer/answer/17134731). Links to live user-data, Families, child-safety, age-restricted-content and console policies; clarifies third-party AI responsibility. Use the live linked policy section plus S23, not the announcement alone, to determine enforcement.

## S23 — Policy deadlines

[Policy Deadlines](https://support.google.com/googleplay/android-developer/table/12921780). Announcement/effective dates, app registration, child-safety and upcoming permission changes. Recheck every release. This table is the source for the dated reminders, not a hardcoded permanent calendar.

## S24 — Android developer verification

[Android developer verification](https://developer.android.com/developer-verification). Identity/app registration and regional/store/device rollout. Distinguish this from Play Console onboarding and from Play app registration obligations.

## S25 — Android vitals

[Android vitals](https://developer.android.com/google/play/vitals), [crashes](https://developer.android.com/google/play/vitals/crash) and [ANRs](https://developer.android.com/google/play/vitals/anr). Metric definitions, bad-behavior thresholds and current/upcoming visibility effects. Check per-device and form-factor scope; internal SLOs are separate decisions.

## S26 — Pre-launch reports

[Use a pre-launch report to identify issues](https://support.google.com/googleplay/android-developer/answer/9842757). Automated testing capabilities, configuration and limitations. Supplement with risk-based real-user/device tests.

## S27 — Alternative billing/program eligibility

[Enrolling in the billing choice program](https://support.google.com/googleplay/android-developer/answer/17161464?hl=en). Current eligibility, APIs, reporting and applicable terms. Do not assume availability or fees are global; follow the relevant program for the actual user's market and transaction.

## S28 — Secure billing

[Fight fraud and abuse](https://developer.android.com/google/play/billing/security). Purchase verification before entitlement, backend protections and voided purchases. Follow linked lifecycle documentation for the specific product/subscription integration.

## S29 — Halt and recovery

[Halting a fully rolled-out release](https://support.google.com/googleplay/android-developer/answer/16285429?hl=en). Eligible release types, halt behavior and limits. A distribution halt is not a forced downgrade of installed applications.

## S30 — Android release optimization

[Enable app optimization with R8](https://developer.android.com/topic/performance/app-optimization/enable-app-optimization). Code/resource optimization and release-build guidance. Verify framework compatibility and regressions instead of blindly changing flags.

## S31 — Startup optimization

[Baseline Profiles overview](https://developer.android.com/topic/performance/baselineprofiles/overview). Profiles, Android code-path performance and measurement. Benefits are workload-dependent; the skill makes no universal speedup claim.

## S32 — Store experiments

[Run A/B tests on your store listing](https://support.google.com/googleplay/android-developer/answer/12053285). Store-listing experiments and measurement options. Statistical design and downstream business guardrails remain explicit project decisions.

## S33 — Review requests

[Google Play In-App Reviews API](https://developer.android.com/guide/playcore/in-app-review). Supported UX and quota constraints for requesting reviews. Do not treat a requested prompt as guaranteed display or manipulate feedback selection.

## S34 — Optional upstream policy-assistance skill

[Android's play-policy-insights skill](https://github.com/android/skills/tree/main/play/play-policy-insights). Linked by Google's July policy announcement. It can be evaluated as an optional supplemental checker when the host supports it; do not assume installation, run it without authorization, or treat generated findings as legal clearance. No upstream skill body is copied here.

## Maintenance record

When refreshing, record changed claim IDs, previous/current effective dates, affected gates and source revision or visible update date. Re-run structural tests and the behavioral evaluation cases relevant to changed rules. Do not mark behavioral evaluation as passed merely because Markdown links or JSON fixtures validate.
