# Releases, Source Maps, Debug Symbols, and CI/CD

## Release identity

Choose one release identifier and use it everywhere.

Good patterns:

```text
frontend@2.14.3
api@4f3a8c12
worker@2026.09.20.1
```

Requirements:

- deterministic;
- unique for the deployed artifact;
- available at build time and runtime;
- unchanged between source-map upload and deployment;
- searchable in the source repository.

A commit SHA is robust. A semantic version is human-friendly. A combined service/version form works well in monorepos.

## Release pipeline order

Preferred sequence:

```text
checkout
  -> test
  -> build immutable artifact
  -> determine release ID
  -> create/record release
  -> associate commits if supported
  -> inject debug IDs into JS artifacts when required
  -> upload source maps/debug symbols
  -> deploy the same artifact
  -> record deploy/environment
  -> smoke test
  -> verify telemetry
```

Do not build a second artifact for production after source maps were generated for staging.

## Sentry releases

Sentry releases correlate events with deployed versions and support release/deploy workflows. Current API documentation states that releases are also required for some source-map and debug workflows.

Where useful:

- create a release;
- associate commits;
- upload source maps/debug files;
- record deploy metadata with the production/staging environment.

Use least-privileged CI tokens. Current Sentry API documentation exposes release-oriented scopes such as `project:releases` and CI scope `org:ci`; exact requirements vary by operation.

Never use a personal owner/admin token when a narrower integration token is available.

## JavaScript source maps

Readable production JavaScript traces require matching generated artifacts.

Current Sentry guidance favors modern debug-ID workflows. With CLI-based flows, inject debug IDs before upload and before deploying the generated files.

Important ordering:

1. production build;
2. debug-ID injection if required by the chosen toolchain;
3. source-map upload;
4. deploy the exact processed bundle.

Do not modify/minify the bundle again after debug-ID injection unless the documented integration explicitly supports it.

Validate using the vendor CLI or a controlled test error.

Sentry's troubleshooting guidance notes that source maps uploaded after an error has already been captured do not retroactively fix already-ingested events. Upload first.

## GlitchTip source maps

Current GlitchTip CLI supports:

```bash
glitchtip-cli sourcemaps inject ./dist
glitchtip-cli sourcemaps upload ./dist \
  --release "$APP_RELEASE" \
  --org "$GLITCHTIP_ORG" \
  --project "$GLITCHTIP_PROJECT"
```

Configure CI with:

- `SENTRY_URL` pointing to the GlitchTip instance where required;
- `SENTRY_AUTH_TOKEN`;
- organization and project identifiers;
- the same `APP_RELEASE` used at runtime.

Even though the environment variable prefix is `SENTRY_`, the target can be GlitchTip because of its Sentry-compatible API/CLI conventions.

## Native debug information

Upload platform-appropriate symbols:

- Apple: dSYM;
- Windows: PDB;
- Linux/native: ELF/debug files;
- Android: ProGuard/R8 mappings and native symbols as applicable.

GlitchTip CLI currently provides `debug-files upload` for native debug symbols.

Do not discard build symbols until their retention and rollback window has passed.

## Source-map security

Prefer uploading source maps privately to the observability backend rather than publishing them to the public CDN merely for monitoring.

Remember that source maps may contain `sourcesContent`, which can include original source code.

Never embed secrets in frontend source; source-map privacy is not a substitute for secret-management discipline.

## Deploy metadata

A deploy should answer:

- which release;
- which environment;
- when deployment started/finished;
- which pipeline/commit produced it;
- who/what approved it;
- which region or target changed.

Use deploy metadata during incident triage: compare first-seen time with the deployment window and inspect suspect commits.

## GitLab CI sketch

Vendor-neutral shape:

```yaml
variables:
  APP_RELEASE: "$CI_PROJECT_PATH_SLUG@$CI_COMMIT_SHA"

build:
  stage: build
  script:
    - npm ci
    - npm run build
  artifacts:
    paths:
      - dist/

observability_artifacts:
  stage: deploy
  needs: ["build"]
  script:
    - ./scripts/upload-observability-artifacts.sh "$APP_RELEASE"
  rules:
    - if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'

deploy:
  stage: deploy
  needs: ["observability_artifacts"]
  script:
    - ./scripts/deploy-existing-artifact.sh "$APP_RELEASE"
```

Keep the auth token in protected/masked CI secrets. Do not print it.

## Release verification

After deployment:

- trigger one controlled error or use a smoke path;
- confirm `release` and `environment`;
- confirm stack trace source resolution;
- confirm the event links to the expected code/release;
- confirm deployment metadata exists;
- confirm new errors are distinguishable from previous releases.

## Sources

- https://docs.sentry.io/api/releases/
- https://docs.sentry.io/api/releases/create-a-new-release-for-an-organization/
- https://docs.sentry.io/api/releases/create-a-deploy/
- https://docs.sentry.io/api/releases/upload-a-new-project-release-file/
- https://docs.sentry.io/platforms/javascript/sourcemaps/
- https://glitchtip.com/documentation/cli/
- https://glitchtip.com/sdkdocs/javascript/
