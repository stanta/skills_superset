# GitLab Pipeline Design

## Target architecture

Prefer a DAG that fails fast and builds once:

```text
validate -> test/security -> build -> package/scan -> staging -> runtime verification -> production
```

Use `needs` to express true dependencies instead of serializing all jobs by stage.

## Branch and Merge Request model

Default recommendation for most product teams:

- short-lived feature/fix branches;
- protected default branch;
- no direct production-bound push;
- Merge Request review before merge;
- required pipeline success for merge where supported/configured;
- stronger review for CI, infrastructure, migration, auth, and payment code.

Do not encode environments as permanent branches such as `dev`, `stage`, and `prod` unless there is a clear release-management reason. Git branches represent source history; GitLab Environments represent deployment targets.

## Reusable CI

Prefer GitLab CI/CD Components or small, versioned include files over copy-pasted hundreds of lines.

For external/reusable components:

- audit source;
- minimize token access;
- pin to a release or commit SHA for high-assurance pipelines;
- avoid moving targets for critical deployment logic.

GitLab documents commit SHA as the strongest pin and recommends published release versions for normal component consumption.

## Workflow control

Use `workflow:rules` to avoid duplicate or irrelevant pipelines.

Example:

```yaml
workflow:
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
    - if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'
    - if: '$CI_COMMIT_TAG'
```

Use job-level `rules:changes` for monorepos and expensive jobs.

## DAG execution

Use `needs`:

```yaml
build:
  stage: build
  needs:
    - lint
    - unit-tests
```

Do not make a build wait for unrelated documentation or slow integration jobs if it does not depend on them.

## Cache versus artifacts

Use **cache** for reusable dependency/build acceleration:

- package-manager caches;
- compiler caches;
- Gradle/Maven/npm/pip caches.

Use **artifacts** for pipeline outputs:

- test reports;
- coverage;
- compiled binaries;
- SBOM;
- dotenv metadata;
- manifests;
- release evidence.

Never rely on cache as the authoritative production artifact store.

## Immutable artifacts

Tag an image with commit SHA for traceability, but deploy by digest where practical:

```text
registry.example.com/app:8f31ab2
registry.example.com/app@sha256:...
```

Rules:

- never deploy `:latest` to production;
- record the digest produced by the build;
- promote that same digest through staging and production;
- do not rebuild between environments.

## Minimal production-oriented skeleton

```yaml
workflow:
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
    - if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'
    - if: '$CI_COMMIT_TAG'

stages: [validate, test, build, deploy, verify]

default:
  interruptible: true

variables:
  IMAGE: "$CI_REGISTRY_IMAGE/app:$CI_COMMIT_SHA"

lint:
  stage: validate
  script: ./ci/lint.sh

unit:
  stage: test
  script: ./ci/test-unit.sh
  artifacts:
    when: always
    reports:
      junit: reports/junit.xml

build:
  stage: build
  needs: [lint, unit]
  script:
    - ./ci/build-and-push.sh "$IMAGE"
    - ./ci/image-digest.sh "$IMAGE" > build.env
  artifacts:
    reports:
      dotenv: build.env

staging:
  stage: deploy
  needs: [build]
  resource_group: staging
  script:
    - ./ci/deploy.sh staging "$IMAGE_DIGEST"
  environment:
    name: staging
    deployment_tier: staging
  rules:
    - if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'

staging-smoke:
  stage: verify
  needs: [staging]
  script: ./ci/smoke.sh staging
  rules:
    - if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'

production:
  stage: deploy
  needs: [staging-smoke]
  resource_group: production
  script:
    - ./ci/deploy.sh production "$IMAGE_DIGEST"
  environment:
    name: production
    deployment_tier: production
  when: manual
  allow_failure: false
  rules:
    - if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'
```

Treat this as a baseline, not a universal template.

## Production concurrency

For simple single-target deployments, `resource_group: production` is a useful guard against overlapping deployment jobs.

Also protect against stale/outdated deployment jobs so an older pipeline cannot overwrite a newer release.

For progressive delivery controlled by another system, coordinate ownership instead of blindly serializing unrelated rollout controllers.

## Review Apps

For web applications and APIs, create an environment per Merge Request when cost and data sensitivity allow.

Use:

- deterministic environment naming;
- automatic expiry;
- synthetic/non-production data;
- no production credentials;
- cleanup on close/expiry.

## Pipeline quality targets

Optimize for:

- fast developer feedback;
- deterministic builds;
- no hidden manual production mutation;
- clear failure reasons;
- reproducible artifacts;
- explicit ownership of deployment state;
- measurable queue time, duration, flaky-test rate, and failure rate.
