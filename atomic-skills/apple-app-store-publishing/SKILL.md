---
name: apple-app-store-publishing
description: >
  Plan, audit, prepare and operate Apple App Store submissions and updates: developer enrollment, App Store Connect, signing, privacy, payments, TestFlight, review, release and App Store optimization. Use for App Store publishing, AppleStore publication, rejection remediation, submission readiness and release automation across native and cross-platform applications. Russian queries: публикация в App Store; AppleStore; подготовка к ревью Apple; выпуск iOS приложения.
metadata:
  category: mobile-release
  last_verified: "2026-10-15"
  portability: framework-and-agent-neutral
---

# Apple App Store Publishing

Turn an application into an evidence-backed submission and release plan. The common workflow applies across projects; platform, framework, business model and jurisdiction are inputs, not assumptions.

## Scope and boundaries

- Primary path: public App Store distribution, especially iOS/iPadOS. Re-evaluate platform-specific packaging and policies for macOS, watchOS, tvOS and visionOS.
- Support first releases, updates, transfers/readiness audits and rejection remediation. Native Swift/Objective-C, Flutter, React Native/Expo, game engines and hybrid applications share policy gates but not build commands.
- Do not confuse the App Store with Apple's hardware retail store, Apple Pay integration, Google Play, enterprise distribution, alternative marketplaces or standalone macOS notarization. Route those separate tasks appropriately.
- No repository name, product category, bundle ID, account, service provider, branch, domain or infrastructure belongs in this reusable skill. Discover these in the target project; put values only in task-local artifacts.
- Preparation is not permission to pay fees, accept agreements, change ownership, upload sensitive data, submit for review or release publicly. Use the operator's actual authorization and the least-privilege tools available. Account Holder and legal decisions remain explicit human gates.

## Read selectively

| Current subtask | Read |
| --- | --- |
| Enrollment, distribution, signing, SDK deadlines, stack adapters | [requirements-and-build.md](references/requirements-and-build.md) |
| Privacy, account lifecycle, login, monetization, regulated categories | [privacy-and-policy.md](references/privacy-and-policy.md) |
| TestFlight, submission, rejection, staged release, recovery | [testing-and-release.md](references/testing-and-release.md) |
| Store assets, localization, conversion, runtime and pipeline optimization | [optimization.md](references/optimization.md) |
| Evidence-backed backlog and review packet | [release-plan.md](templates/release-plan.md), [review-notes.md](templates/review-notes.md) |
| Authoritative references and dated facts | [sources.md](references/sources.md) |
| Skill regression scenarios | [cases.json](evals/cases.json) |

## Procedure

### 1. Discover and classify

Read project instructions, manifests, release configuration and existing App Store records through available authorized tools. Record source commit and inspection date. Identify platform targets, framework/toolchain, distribution method, new app versus update, publisher entity, storefronts/locales, account features, data flows, third-party SDKs, payment categories, user-generated content, AI processing and regulated functionality.

Prefer a compact inventory over loading the whole repository. Split the work into Start (release workflow), Support (framework/privacy/payments) and Check (QA/evidence). Unknown inputs stay unknown; continue independent preparation and create an owner-assigned blocker for decisions that cannot be inferred safely.

### 2. Refresh requirements

Open Apple's current submission page, upcoming requirements, App Review Guidelines and applicable App Store Connect help. Record URL, accessed date, effective date, platform/storefront scope and evidence. Distinguish requirements already effective, future announcements, recommendations and unresolved interpretations. Do not treat a dated snapshot in this skill as evergreen authority.

Separate the build SDK, Xcode version, deployment target, upload client and test OS. Resolve apparent conflicts by matching scope and effective date; escalate genuine conflicts instead of silently guessing. See [sources.md](references/sources.md).

### 3. Build a release gate matrix

Create one row per applicable requirement:

`ID | requirement | mandatory/conditional/recommendation | applicability | source/date | implementation evidence | test evidence | owner | status`

Use only `PASS`, `FAIL`, `BLOCKED` or `NOT_APPLICABLE`. A missing observation is not a pass; a justified non-applicable feature is not a failure. Track app, SDK and backend behavior together. Prioritize rejection, privacy, financial and safety blockers before cosmetic improvements.

### 4. Close account, technical and policy gaps

Follow the relevant references. Inventory identifiers and signing without copying secrets. Produce the least-change implementation plan, with dependencies and acceptance criteria. Require explicit evidence for store declarations; do not invent privacy labels, export answers, regulatory status, age ratings, entitlement eligibility or reviewer credentials.

### 5. Verify the release candidate

Run available static, unit, integration and device checks against the candidate revision. Validate the distributable artifact, its signing and actual included resources. Exercise critical flows using a TestFlight-delivered build where practical. Keep simulator results separate from physical-device results. Record what was not executed and why.

### 6. Prepare and, when authorized, submit

Assemble metadata, assets, privacy/export/compliance declarations, purchase products and a reviewer access packet. Confirm backend availability and feature parity. Track upload, processing, beta approval, submission, App Review approval and public availability as different states. Review the final app/version/build/storefront/release-mode selection before each external write.

### 7. Release and learn

Require a recorded go/no-go decision. Observe the released build and storefront availability, not just an accepted upload. Maintain compatible backend behavior, crash symbolication, privacy-safe telemetry, incident ownership and a forward-fix plan. Treat store conversion and product retention as separate outcomes.

## Required outputs

Use task-local paths chosen from project conventions:

1. Release inventory and source/effective-date ledger.
2. Applicability/gap matrix with an ordered, dependency-aware agent backlog.
3. Candidate evidence, completed metadata checklist and reviewer packet with secret references rather than secret values.
4. Release/incident runbook and an explicit list of human decisions and unverified items.

Every task needs an owner, inputs, dependencies, concrete change, acceptance criteria, evidence artifact and authorization boundary. The templates provide this contract without imposing any project architecture.

## Completion and anti-patterns

Completion means all applicable blocking gates have evidence, or the report explicitly identifies the blockers. Claim publication only after verifying the live store/version. Do not promise approval or an exact review duration.

Never: bypass review with hidden behavior; substitute Apple Pay for digital In-App Purchase without a verified applicable rule; equate ATT with every analytics event; present a privacy manifest as a privacy policy; declare medical compliance from a disclaimer; regenerate shared signing assets blindly; expose API keys in examples; claim an instant downgrade of installed apps; require a proprietary CI service or agent runtime.
