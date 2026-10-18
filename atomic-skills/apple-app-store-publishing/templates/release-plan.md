# App Store release plan

This template is project-neutral. Replace placeholders from observed project/account evidence. Keep secrets outside this document. Uninspected items start as `BLOCKED`, with the missing evidence stated.

## Release inventory

| Input | Observed value / evidence / owner |
| --- | --- |
| Assessment date and source revision | |
| Release goal: first release, update, readiness audit, rejection fix | |
| Platforms, device families, framework and toolchain | |
| Distribution route and publisher entity | |
| App record, public bundle/team identifiers, version/build | |
| Target storefronts, locales and supported OS versions | |
| Account/login features and intended audience | |
| Digital/physical products and payment architecture | |
| Data categories, processors, SDKs, AI and tracking | |
| UGC, medical/regulated or children's functionality | |
| Existing release automation and available agent tools | |
| Authorized external writes and prohibited actions | |

## Requirement evidence ledger

| ID | Claim / requirement | Source URL and section | Accessed date | Effective date | Scope | Fact / recommendation / unresolved |
| --- | --- | --- | --- | --- | --- | --- |
| R-001 | | | | | | |

Separate current requirements from announced future changes. Preserve conflicting sources and specify which interpretation requires confirmation.

## Applicability and readiness

| Gate | Mandatory / conditional / recommendation | Applicability and rationale | Source IDs | Implementation evidence | Test evidence | Owner | PASS / FAIL / BLOCKED / NOT_APPLICABLE |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Publisher, access and agreements | | | | | | | |
| Toolchain, SDK and deployment target | | | | | | | |
| Signing, identifiers and release artifact | | | | | | | |
| Privacy, permissions, manifests and data lifecycle | | | | | | | |
| Payment routing, products and entitlement lifecycle | | | | | | | |
| Conditional category and territory requirements | | | | | | | |
| Metadata, localization, assets and support | | | | | | | |
| Release-candidate/device verification | | | | | | | |
| Review access and backend availability | | | | | | | |
| Release authorization, monitoring and recovery | | | | | | | |

## Agent task contract

Repeat for each task; use actual project paths rather than assumed framework folders.

```yaml
task_id: T-001
goal: ""
priority: ""
owner: ""
depends_on: []
requirement_ids: []
inputs_and_evidence: []
paths_or_account_objects: []
authorized_actions: []
implementation_steps: []
acceptance_criteria: []
test_commands_or_manual_steps: []
expected_evidence_artifacts: []
human_gate: ""
external_side_effects: []
recovery_or_undo: ""
status: BLOCKED
blocker_or_result: "Not yet assessed"
```

Use a dependency graph rather than one unordered checklist. Independent metadata preparation may proceed while enrollment is blocked; submission must not proceed on guessed legal/account answers.

## Candidate and review packet

Record commit, artifact identity, build/version, backend compatibility, executed tests and unexecuted tests. Link the completed [review-notes template](review-notes.md), localized asset matrix, privacy/payment declarations and resolved findings. Store credential references only.

## Human decisions

| Decision | Authorized owner | Evidence needed | Decision/time |
| --- | --- | --- | --- |
| Publisher identity and agreements | | | |
| Legal/medical/export/trader classification, when applicable | | | |
| Paid products, regional payment rules and commercial terms | | | |
| Submission approval and selected release mode | | | |
| Public release and incident authority | | | |

## Release and recovery

Specify release mode, storefronts, observation windows, baseline/guardrails, incident owner and pause/escalation criteria. Document backend compatibility and forward-fix steps; do not assume installed binaries can be instantly downgraded.

## Final report

State the highest **observed** lifecycle state: built, uploaded, processed, beta-ready, submitted, approved, released or verified-live. These are reporting labels, not API enums. Include evidence and timestamp, unresolved blockers, explicit approvals and remaining observations. Do not equate a plan with completed account changes or publication.
