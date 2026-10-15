# Optimization without policy shortcuts

Use after blocking compliance/reliability issues are understood. These are recommendations, not promises of store ranking or mandatory numerical SLOs. Source IDs resolve in [sources.md](sources.md).

## 1. Reduce release lead time

Find the critical path before doing cosmetic work: account/organization verification, applicable closed testing, signing ownership, restricted permissions and unavailable reviewer access. Parallelize independent preparation only with available tools. Keep one explicit checklist and artifact identity instead of repeating a repository-wide audit for every question. [S02–S04, S13]

Build once after all approved code changes, verify the resulting hash, and promote the same candidate through tracks. Cache dependency downloads using lockfile/toolchain keys, but never treat a cache hit as a security check. Rebuild whenever the artifact changes; do not reuse old test evidence for a new binary. Use an independent release gate rather than allowing every main-branch push to publish automatically.

Automate deterministic checks: manifest/version/signature inspection, tests, asset/text validation and evidence completeness. Keep identity, legal attestations and go-live decisions with authorized people. API edits and console changes can invalidate one another, so serialize publishing per package and re-read state before retrying. [S18, S19]

## 2. Reduce review friction

Create a reviewer journey that works from a clean install and a clean account. Verify login, entitlement, test content and geographic/device prerequisites before submission. Align screenshots, listing claims, permissions, backend behavior and declarations. Document unusual but legitimate behavior with evidence instead of expecting a reviewer to infer it. [S12, S13]

Submit a coherent version rather than mixing unfinished flags and unrelated metadata changes. Keep security/privacy changes synchronized with Data safety and policy disclosures. Maintain a concise rejection log: exact issue, affected version, policy section, reproduction, fix, evidence and resubmission state. Appeal with relevant facts when appropriate; do not evade an enforcement decision by disguising the same app under a new account.

## 3. Optimize startup, size and runtime

Measure release builds on representative lower-end and current devices. Set internal budgets for startup, rendering, memory, download size, network work and battery use based on the app's real use cases. Compare before/after distributions and critical flows, not one favorable benchmark run. [S25]

Use app bundles' device-specific delivery and inspect delivered APK sizes rather than just the AAB archive. Remove unused assets/dependencies and avoid bundling multiple redundant SDKs. Consider feature/asset delivery only when the added complexity has measured value. [S12, S15]

Enable and test suitable Android code/resource optimization with current R8 guidance; preserve necessary keep rules for reflection/JNI and retain mapping/symbol files. Do not apply Android-only switches blindly to a cross-platform runtime. Follow Flutter's own release/size guidance for its Dart/native split. [S20, S30]

Evaluate Baseline Profiles and appropriate startup profiling for Android code paths. Measure the effect; do not promise an identical benefit for every app or claim a profile accelerates all Dart/JavaScript/game-engine execution. Keep expensive initialization and network work off the startup-critical path where possible. [S31]

For native libraries, upgrade the specific incompatible engine/plugin/SDK and verify the final binary on 16-KB devices. Suppressing a warning, checking only the main library or setting ZIP alignment is not a complete repair. [S05]

## 4. Use Play vitals as a release signal

Track crashes, ANRs, excessive wake locks and other applicable current core vitals by app version, OS and device model. Compare Play's user-perceived metrics with internal telemetry, recognizing that denominators and coverage differ. Protect sensitive data in breadcrumbs, exception messages and screenshots. A third-party crash tool does not replace Play's visibility metrics. [S06, S25]

Treat Google's bad-behavior thresholds as outer limits, not targets. Set stricter product SLOs with minimum sample sizes and meaningful observation windows. A small rollout with no observed crashes is not proof of safety when traffic is tiny. Include non-crash business failures such as login loops, lost data or failed purchases in halt decisions. Record who can halt and how users already on the bad build will be supported.

## 5. Improve store conversion honestly

Localize the value proposition, screenshots and terminology for the markets actually supported by the app. Show the first useful task, credible functionality and clear paid/free boundaries. Avoid keyword repetition, unrelated comparisons, unsupported performance claims and fabricated screenshots. Follow the current asset requirements of each form factor. [S12]

Use store-listing experiments with a prespecified hypothesis, primary conversion metric, exposure window and guardrails. Prefer a single interpretable change or a deliberate experiment design. Do not stop at the first favorable fluctuation. Segment by locale/source where the data supports it, and assess downstream activation/retention rather than optimizing installs that immediately churn. These experiment-design recommendations complement Play's own experiment tools. [S32]

Ask for reviews only at appropriate moments using the supported review flow. Respect API quotas and UX rules; do not buy ratings, offer rewards or pre-screen satisfied users to manipulate ratings. Keep customer-support recovery separate from public-review solicitation. [S33]

## 6. Avoid false optimization

Never trade away truthful disclosure, permission minimization, genuine testing or safety to ship sooner. Do not implement review-only behavior, conceal a prohibited payment route, manipulate ratings, fake engagement, or claim legal compliance from a technical checklist. Reduced latency, lower cost and better conversion are measured outcomes, not properties a skill can guarantee.

## Suggested experiment record

Record problem, affected cohort/version, baseline, proposed change, intended benefit, measurement method, privacy constraints, acceptance/stop criteria, result and decision. Label estimates and assumptions explicitly. Keep app-specific data in that app's artifacts; this skill contains only the reusable method.
