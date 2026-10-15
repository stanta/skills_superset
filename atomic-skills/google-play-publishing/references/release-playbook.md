# Release playbook

Use with [the skill](../SKILL.md), [policy snapshot](policy-snapshot.md) and [sources](sources.md). The sequence is framework-neutral. Commands below are patterns: select the repository's real module, variant, tools and permissions before running them.

## Phase A — Scope and slow prerequisites

Inspect the source revision, existing release documentation and console state. Record account type/date, public/private distribution, first release/update, package ID, form factors, markets, audience and business model. Identify who owns legal declarations, signing, payments and production approval. Start legitimate identity/organization verification and applicable closed testing early; work on assets and technical fixes independently. Do not invent completed external tasks. [S02–S04]

Produce a dependency-aware checklist: task, prerequisite, owner, blocking condition, acceptance evidence. Separate hard release gates from desirable optimization. A verified build is not proof of policy readiness; a complete listing is not proof the backend works.

## Phase B — Artifact and signing

1. Read build files, dependency locks, flavors, release environment, merged manifest and prior version codes. Preserve an existing package/signing identity; do not create a new app to work around an update failure.
2. Check target API by form factor, current SDK/toolchain compatibility and Android behavior changes. Raising targetSdk without regression tests is insufficient. Do not raise minSdk merely to match targetSdk. [S01]
3. Configure release signing through protected secret storage. Distinguish upload-key recovery from app-signing-key upgrade. Register Play app-signing fingerprints with identity/API providers and domain association files where required; a locally signed APK is not equivalent to a Play-installed build. [S14]
4. Inspect the actual AAB and generated APKs: package/version, no debugging, production endpoints, permissions, native ABIs, size, SDK inventory and symbol mappings. Check transitive native libraries used by frameworks, engines, media, databases and monitoring. [S05, S12, S15]
5. Attach source commit, resolved dependency versions, build commands/toolchain, artifact SHA-256 and certificate fingerprints to the release packet. Store no signing passwords, access tokens or raw user data.

### Stack adapters

| Stack | Inspect | Candidate commands / caution |
| --- | --- | --- |
| Native Android / bare React Native | Gradle wrapper, real application module and flavor, JDK/AGP, release signing | `./gradlew :<module>:lint<Variant> :<module>:test<Variant>UnitTest :<module>:bundle<Variant>`; first confirm these tasks exist. Use the detected wrapper and build profile, not a downloaded arbitrary Gradle. |
| Flutter | pubspec/lock, Flutter version, Android Gradle configuration, plugins and release signing | `flutter analyze`, `flutter test`, then `flutter build appbundle --release`; add the actual flavor/entry point when required. Native plugins and engine libraries still require inspection. [S20] |
| Expo / EAS | app config, package ID, SDK, native plugins, eas.json build and submit profiles | `eas build --platform android --profile <reviewed-build-profile>`; submit only a selected verified artifact/build ID. EAS is optional and does not remove console gates. [S21] |
| Unity / another engine | engine release, Android export/build options, scripting backend, ABI list, plugins | Follow that engine's current official AAB/signing instructions. Do not assume the engine version alone guarantees all bundled libraries comply. |
| PWA / web-backed wrapper | actual Android package/build pipeline, app links/domain proof, offline/error handling and native integration | A website URL alone is not an AAB. Assess useful app functionality and applicable policies; a wrapper is neither automatically acceptable nor automatically forbidden. |

For EAS/API-based first submissions, inspect current bootstrap requirements and whether the app/package already exists in Play Console. Do not promise that one CLI command creates all console records or completes declarations. [S18, S21]

### Artifact checks (only when installed and authorized)

```sh
# Inspect rather than install arbitrary tooling; use your verified bundletool version.
java -jar "$BUNDLETOOL_JAR" validate --bundle="$AAB_PATH"
java -jar "$BUNDLETOOL_JAR" dump manifest --bundle="$AAB_PATH" --module=base
sha256sum "$AAB_PATH"

# Check a generated APK, not the AAB, with apksigner/zipalign.
apksigner verify --print-certs "$APK_PATH"
zipalign -c -P 16 -v 4 "$APK_PATH"

# Verify the actual test device's page size before calling a runtime test a 16-KB test.
adb shell getconf PAGE_SIZE
```

Use the current official ELF-alignment procedure for every relevant `.so`; APK ZIP alignment by itself is insufficient. Test on a verified 16-KB environment and on supported ordinary devices. Do not treat a compatibility/back-compat mode as proof that native code was repaired. [S05, S14, S15]

## Phase C — Behavior, declarations and access

Build a data inventory from code, resolved SDK documentation and authorized runtime observation. For each data type record collection/sharing, purpose, off-device path, processor, consent/optional behavior, retention, deletion and security. Include server-mediated and third-party AI data flows rather than checking only Android permissions. Keep sensitive payloads out of logs and release evidence. [S06–S08, S22]

Match the inventory to Data safety and privacy disclosures. Review content ratings, target audience, ads, restricted-permission declarations, Health apps and other console forms. Record not-applicable decisions explicitly. A declaration is an attestation by the publisher, not something an agent should invent to unblock a button. [S11, S13, S22]

Create a synthetic reviewer account that reaches gated features using the ordinary supported experience. Supply reproducible steps and any region/device instructions. Test those instructions from a clean session. Do not expose production secrets, require a human to supply a short-lived OTP, or change behavior only when detecting review. [S13]

For account-deletion scope, test both required request entry points and the resulting lifecycle, including queued jobs, processor deletion and documented retention. Separate subscription cancellation, entitlement changes and account deletion; deleting an account must not silently create an unexplained recurring-charge trap. [S08]

For covered digital purchases, implement and test the applicable billing program. A secure backend should verify purchases and maintain idempotent entitlements; handle pending/canceled purchases, acknowledgment/consumption where applicable, restoration, renewal, grace/hold, refunds and revocation according to current billing documentation. Do not grant entitlement solely from an unverified client callback. [S09, S10, S28]

## Phase D — Test-track evidence

Use the track needed for the account and release; internal, closed, open and production are not four mandatory sequential steps. Internal testing is useful for fast smoke testing but is not a substitute for a mandated closed test. Eligible production-access applicants must preserve genuine participation/feedback evidence and explain changes made. No fabricated testers or purchased fake engagement. [S04]

Minimum risk-based matrix:

- Fresh install, upgrade from the currently published build, local-data migration and backend compatibility; launch on supported OS/device classes and with relevant 4-KB/16-KB native environments.
- Login/logout/recovery, deep links, notifications, permission denial/revocation, offline and reconnect, interrupted work, low-memory/process death and accessibility/text scaling.
- Conditional purchase, deletion, AI-reporting/moderation, child-safety, health-data, UGC and restricted-permission flows.

Run tests against the release artifact distributed by Play when available. Check pre-launch report coverage, failures and reviewer access; an automated crawler passing a login screen is not full functional coverage. Triage each warning with reproducible evidence. [S16, S26]

## Phase E — Listing and submission

Prepare localized name/descriptions, screenshots and required visual assets for the chosen form factors. Follow current dimensional/content rules. Use screenshots of real supported flows and distinguish free versus paid capabilities. Validate support/privacy/deletion links from outside a logged-in developer session. [S12, S13]

Keep review notes functional: where to log in, how to reach gated features, required inputs, relevant policy explanations and evidence. Avoid unsupported claims, review incentives and keyword stuffing. Recheck the console's pending changes as a whole: a metadata edit may travel with a release. [S12, S16]

CI sequence: unprivileged lint/test → trusted release build/signing → immutable artifact verification → authorized upload to a selected track → review/declaration steps → explicit production gate. Use least-privilege app/track access and scoped credentials; prefer short-lived identity where the actual tool supports it, otherwise protect and rotate the required service-account key. Never store publisher credentials in the app or run privileged release jobs on untrusted PR input. [S18, S21]

For direct Android Publisher API use, inspect existing edits/tracks first; use a deliberate edit/upload/track update/validation/commit lifecycle and record responses. Select explicit package, version and track; do not let `latest` accidentally pick another build. API edit validation is not policy review, and committing an edit can have externally visible effects. [S18, S19]

## Phase F — Publication and recovery

Record the actual transition: uploaded → sent for review → approved → published → verified live. Distinguish app production-access approval from individual release approval. Review time varies and approval cannot be guaranteed. First production rollout reaches all eligible users in selected markets; do not invent percentage rollout for a first release. Managed publishing is not available for initial app publication; inspect eligibility after testing/publication. [S04, S16, S17]

For updates choose an example progression such as 5% → 20% → 50% → 100% only after risk/traffic analysis and explicit approval. Set halt thresholds for critical flows and device-specific regressions, not just aggregate crash rate. Market restriction is a deliberate distribution decision, not a way to bypass policy. [S16, S25]

On incident: stop further rollout using the available console control; disable a risky feature only through a predesigned safe flag; preserve diagnostics; maintain backend compatibility; produce and test a forward fix with a larger versionCode. Where Play offers halting a fully rolled-out update, verify eligibility and what version will be served to new users. Already-upgraded devices are not remotely downgraded by a halt. [S16, S29]

## Final release evidence

Start from [the template](../assets/release-readiness.template.json). Every blocker needs an owner and acceptance criterion. Use unknown for unavailable console/build/runtime evidence. A research-only run can finish with a complete handoff while remaining explicitly not authorized/not ready to publish. A publishing run ends only at its authorized observed state, never at an assumed future approval.
