# Requirements, enrollment and reproducible builds

Read the [source ledger](sources.md), especially S02-S05, S18 and S21-S23. This is a workflow, not a preconfigured project.

## Distribution and publisher decisions

Confirm public App Store, unlisted/custom distribution or a different distribution route before preparing records. A macOS notarization result alone is not Mac App Store acceptance. A web/PWA project needs an appropriate Apple-platform application/distribution strategy; adding a WebView does not by itself establish review readiness.

Select individual versus organization enrollment deliberately. Organization enrollment involves legal-entity verification, binding authority and normally a D-U-N-S number; individual seller naming differs. Verify two-factor authentication and current membership. The Account Holder handles contracts; paid offerings may require additional commercial, tax and banking setup. Never create a second developer account merely because access to the correct team is missing. [S04](sources.md#s04)

Inventory team ID, bundle IDs for app/extensions, store record ID, version/build, capabilities and associated domains. Store only public identifiers or secret-manager references. Changing identifiers or ownership is not routine release cleanup. For transfers, run Apple's current transfer criteria and service-migration checks separately.

## Toolchain freshness gate

Record these independently:

| Dimension | Evidence |
| --- | --- |
| Xcode and SDK used to build | Version output and archive provenance |
| Deployment target | Actual target/build settings, including extensions |
| Upload channel/client | Installed version and supported authentication |
| Test coverage | Physical devices, OS versions, platform families |
| Policy minimum and effective date | Current S02/S03 reference |

Do not copy a future requirement into today's blockers. Do not mistake the minimum upload-client version for the minimum build SDK. Record a migration task for announced changes even when the current candidate remains compliant.

## Signing and artifact gates

Inspect existing configuration before editing. Confirm the selected team, distribution signing, provisioning/capability alignment and expiration for all included targets. Check push environment, associated domains and other entitlements only when used. An App Store Connect API key authenticates supported account/API operations; it is not a replacement for binary code signing.

Keep certificate private keys, provisioning material and `.p8` keys out of repositories, app bundles, logs and generated plans. Use narrowly scoped secret storage, short-lived/ephemeral build environments where practical, and explicit access ownership. Never revoke or regenerate shared signing assets without checking their consumers.

Build from a known commit with reviewed dependency locks and production configuration. Inspect the actual archive/export: identity, version, minimum OS, entitlements, privacy manifests, extension contents, assets and debug/sensitive leftovers. Preserve archive, symbol files and dependency/toolchain provenance. Uploading the wrong flavor with the right version is still a release failure.

## Optional stack adapters

Commands below are patterns. Resolve paths, schemes, tools, signing and authorization first; do not blindly execute or assume a host has macOS/Xcode.

### Native Apple / React Native without managed submission

Use the project's existing Xcode workspace or project and scheme. Start with available version/build-setting inspection; then archive and export through reviewed settings. Example for an already configured workspace:

```sh
xcodebuild -version
xcodebuild -showsdks
xcodebuild -list -json -workspace "$WORKSPACE"
xcodebuild -workspace "$WORKSPACE" -scheme "$SCHEME" \
  -configuration Release -destination 'generic/platform=iOS' \
  -archivePath "$ARCHIVE_PATH" archive
xcodebuild -exportArchive -archivePath "$ARCHIVE_PATH" \
  -exportOptionsPlist "$REVIEWED_EXPORT_OPTIONS" -exportPath "$EXPORT_PATH"
```

Validate current export options with the installed Xcode documentation. Do not add automatic provisioning mutations merely to silence signing errors. For non-iOS platforms, replace destination and packaging with their verified platform flow. [S05](sources.md#s05)

### Flutter

Inspect the iOS host project as well as Dart configuration, plugins and flavor selection. A Flutter build does not bypass native signing or SDK privacy obligations. A configured release can use:

```sh
flutter build ipa --release --build-name "$VERSION" --build-number "$BUILD"
```

Adapt approved flavor/entrypoint and signing/export options to the actual project; inspect the resulting archive. [S22](sources.md#s22)

### Expo / managed cross-platform services

Inspect app configuration, native plugins, release channel and provider build identity. EAS Submit is optional, not a prerequisite for this skill. Select an explicit verified build rather than an ambiguous latest build. Provider submission/upload must be followed by App Store Connect processing, metadata, review and release checks. [S23](sources.md#s23)

### Other frameworks, games and hybrid apps

Trace the framework export to the final Apple archive. Verify native dependencies, extension targets, privacy manifests and entitlements after export. Keep framework-specific implementation in a separate adapter; never assume all projects share a folder layout or build vendor.

## Efficient and safe release automation

Separate unprivileged pull-request tests from signing/upload/release jobs. Pin toolchains and reviewed dependencies; cache by their actual versions and lockfiles. Serialize version/build allocation and duplicate-sensitive submissions. Keep logs and artifacts redacted. Prefer immutable artifact promotion where the distribution workflow permits; revalidate any rebuilt candidate rather than assuming it is identical.

Automate deterministic checks, metadata linting, artifact validation and authorized API operations. Use backoff and inspect server state before retrying writes. Keep agreements, classification decisions and public release behind explicit authority gates. Consult the actual API surface rather than inventing endpoints. [S21](sources.md#s21)

## Exit evidence

A build gate passes only with the candidate commit/artifact identity, toolchain, target settings, signing validation and applicable policy minimum recorded. Unsupported tooling is a blocker or authorized handoff, not a fabricated successful build.
