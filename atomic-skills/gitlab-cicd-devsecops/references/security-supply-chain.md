# GitLab DevSecOps and Software Supply Chain

## Secrets

Never place production secrets in:

- repository files;
- Docker build arguments that persist in layers/history;
- plaintext artifacts;
- copied `.env` files;
- reusable runner images.

GitLab secret detection should complement, not replace, proper secret storage.

If a secret is pushed:

1. revoke it;
2. rotate it;
3. investigate use;
4. remove it from active configuration;
5. rewrite history only when justified;
6. issue a new credential.

Deleting the file alone does not make the leaked secret safe.

## OIDC and short-lived identity

GitLab CI/CD ID tokens support OIDC authentication to third-party services. Prefer this to storing long-lived cloud credentials.

Pattern:

```text
GitLab job
  -> ID token with explicit audience
  -> cloud/Vault validates issuer, audience, subject/claims
  -> short-lived credential
  -> narrowly scoped operation
```

Example:

```yaml
deploy:
  id_tokens:
    CLOUD_ID_TOKEN:
      aud: https://cloud.example.com
  script:
    - ./ci/exchange-token.sh "$CLOUD_ID_TOKEN"
    - ./ci/deploy.sh
```

Bind cloud trust to project/group and protected branch/tag claims. Prefer stable identifiers such as project ID where the provider/GitLab configuration supports them.

Legacy `CI_JOB_JWT` / `CI_JOB_JWT_V2` should not be used; GitLab removed them in GitLab 17.0 in favor of ID tokens.

## CI_JOB_TOKEN

For GitLab-to-GitLab automation, prefer `CI_JOB_TOKEN` over personal tokens when it satisfies the use case.

Use:

- explicit project allowlists;
- minimum scope;
- fine-grained permissions when available;
- no unnecessary cross-project trust.

## Security scanning model

Layer controls rather than relying on one scanner.

Repository/static:

- SAST;
- secret detection;
- dependency scanning;
- IaC scanning.

Artifact:

- container scanning;
- SBOM generation;
- malware/signature checks where relevant.

Runtime/behavioral:

- DAST;
- API security testing;
- fuzzing where justified.

GitLab feature availability varies by tier; verify the current documentation before relying on a specific built-in scanner.

## Security gates

A useful default policy:

```text
critical: block release
high: block when exploitable or require explicit security exception
medium: ticket with remediation SLA
low: backlog/risk-based treatment
```

Tune to system criticality and exposure. Avoid blocking production on every informational finding.

## Central policy

For many projects, centralize security controls rather than copy-pasting pipeline YAML.

Objectives:

- scanner requirements cannot be silently removed by application teams;
- exceptions are explicit and auditable;
- policy changes are versioned;
- critical projects inherit stronger controls.

GitLab Ultimate merge request approval policies can require approvals based on scanner results and other conditions.

## Supply-chain chain of custody

A production release should preserve:

```text
source commit
 -> reviewed pipeline definition
 -> build job
 -> immutable artifact digest
 -> SBOM
 -> scan result
 -> signature/provenance
 -> registry
 -> approved deployment
 -> runtime version
```

## SBOM

Generate an SBOM for production artifacts where practical.

Use it to answer:

- which dependencies are present;
- which version introduced a vulnerability;
- which artifacts are affected;
- whether an incident requires rebuild/redeploy.

## Signing and provenance

For high-assurance systems:

- sign images/artifacts after successful build/security validation;
- record build provenance;
- verify signature before deploy;
- isolate signing identity from general runners.

Do not put master signing keys directly in build jobs. Prefer KMS/HSM or a dedicated signing service.

## Web3/FinTech hardening

CI should not receive master custody material such as:

- wallet mnemonic;
- validator seed;
- hot-wallet master private key;
- multisig owner private keys.

Prefer:

```text
CI -> short-lived authenticated request -> signing/KMS/HSM service -> limited signed operation
```

Test payment/webhook systems for:

- idempotency;
- duplicate callbacks;
- retries;
- replay resistance;
- signature verification;
- timeout recovery;
- reconciliation;
- chain reorg/finality assumptions.

A duplicated webhook must not duplicate settlement or accounting side effects.
