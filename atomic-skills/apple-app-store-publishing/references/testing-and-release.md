# TestFlight, review, release and recovery

Primary workflow references: [S05](sources.md#s05), [S06](sources.md#s06), [S19](sources.md#s19), [S15](sources.md#s15). Evidence requirements below are recommended release-engineering controls, not a claim that Apple mandates one particular CI suite.

## Candidate verification

Associate every result with source revision, version/build, artifact identity, backend version/configuration, device/OS, locale and test date. Define project-appropriate thresholds before testing; do not invent universal acceptable crash or latency percentages.

Cover the applicable critical journeys: fresh installation, upgrade with existing data, first launch, onboarding, login/re-authentication, core function, purchases/restore, account deletion, offline/error recovery, denied permissions and accessibility. Add deep links, push delivery, extensions, background work, media and multi-device behavior when present. Test both supported older targets and current OS behavior, including platform-specific layout changes.

Use physical-device and release-configuration evidence for device-dependent behavior. Simulator/unit success does not establish signing, real push delivery, production permissions, performance or real purchase entitlement correctness. Preserve symbol files and confirm a controlled test error can be symbolicated without exposing personal data.

## Beta distribution

Validate and upload the intended candidate, then wait for actual processing results rather than equating a successful transfer with an available build. Inspect warnings and errors. Provide beta test information and select the correct internal/external groups.

External beta review and App Store release review are distinct. TestFlight builds expire; keep tester access and candidate identity explicit. The dated limits are in the [source ledger](sources.md). Collect structured feedback and test purchase behavior in the appropriate sandbox environment. [S05](sources.md#s05), [S06](sources.md#s06)

## Submission packet

Confirm the exact app record, platform, version and build. Complete required metadata, territories, age-rating answers, privacy/export declarations, applicable purchase products and review details. Validate live support/privacy links and localized assets. Use [review-notes.md](../templates/review-notes.md).

Provide a synthetic demo account or a genuinely usable demo route. Verify access from a fresh device/session and a reviewer-accessible network. Explain special configuration, hardware, geofencing, authentication and feature navigation. Do not put production/customer data or reusable credentials in repository documentation; store reviewer credentials only in the intended authorized channel.

Keep backend services and configured features available throughout review. Document real limitations rather than disguising them with review-only behavior. Confirm the final release option with the operator: automatic approval-to-release and manual release have materially different effects. [S19](sources.md#s19), [S11](sources.md#s11)

## State model

Track independent transitions and their evidence:

`built -> validated -> uploaded -> processed -> beta-ready -> submitted -> in-review -> approved -> released -> verified-live`

This is a task-tracking model, not a claim that these are exact App Store Connect API enum names. Read actual server statuses from the current interface/API. Beta distribution is an optional path, not a mandatory production state transition.

Record authorized actor and receipt/time for each external write. Before retrying a timeout, inspect whether the operation already succeeded. Never claim `released` from an upload log or `approved` from a TestFlight approval.

## Rejection triage

1. Preserve the exact reviewer message, cited guideline, submitted build and reproduction context.
2. Reproduce independently; distinguish product defects, inaccessible review setup, metadata mismatch, missing evidence and policy interpretation.
3. Map each concern to one concrete change or a concise evidence-backed explanation. Avoid speculative blanket rewrites.
4. Re-test affected and neighboring flows. Update declarations/screenshots when behavior changes.
5. Reply point by point with navigation steps and evidence; use Apple's current review/appeal process when appropriate.

Do not guarantee approval or a precise review duration. A newer binary does not by itself answer an unresolved policy objection. Avoid repeated submissions with unchanged explanations.

## Launch and update rollout

For an initial launch, use an approved release mode and a monitored launch checklist. For supported version updates, evaluate Apple's phased automatic-update release. It is not a hard limit on who can install: users can manually obtain an available update. Pausing a phase does not remove builds already installed. [S15](sources.md#s15)

Before release, record baseline metrics, incident owner, observation windows and explicit stop/escalation criteria. Monitor availability, crashes/hangs, startup and critical-flow failures, purchase reconciliation and backend health. Segment by actual app version, OS and device family while minimizing identifiers and respecting consent.

Verify the live storefront and installation/version after release. Track availability propagation separately from review approval. Keep metadata experiments separate from binary rollout decisions.

## Recovery without an imaginary instant rollback

Plan for pausing rollout, disabling a problematic server-controlled feature safely, restricting availability when warranted, restoring compatible backend behavior and submitting a forward-fix build. None of these guarantees downgrading binaries already on devices. Keep old clients and entitlements supported during migration; avoid destructive database changes coupled to a store launch.

Use feature flags for controlled product operation, not to hide unreviewed functionality. Protect user access and paid entitlements during incidents. Exercise the recovery plan with a synthetic failure before a high-risk release.

## Evidence to retain

Retain the candidate revision, toolchain/dependency locks, archive/export identity, symbols, test reports, declarations, metadata snapshot, reviewer communications, authorization records and release observations according to the project's security/retention policy. Redact credentials and personal data. A go/no-go report should distinguish observed passes from unexecuted tests and human decisions.
