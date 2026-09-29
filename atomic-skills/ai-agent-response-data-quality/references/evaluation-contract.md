# Evaluation contract and regression strategy

Implement the release decision as executable invariants. An evidence packet is an auditable record, not a substitute for source access or deterministic checks.

## Illustrative evidence packet

The following fixture is deliberately **blocked**: an unrun critical reconciliation cannot pass merely because an apparent source was attached.

```json
{
  "request_id": "synthetic-001",
  "policy_version": "dq-v1",
  "model_version": "record-at-runtime",
  "prompt_version": "record-at-runtime",
  "as_of": "2026-09-29T12:00:00Z",
  "risk": "critical",
  "required_fields": ["entity_id", "period", "currency"],
  "sources": [
    {
      "id": "s1",
      "kind": "system_of_record",
      "locator": "fixture://ledger/001#row=2",
      "revision": "fixture-v1",
      "observed_at": "2026-09-29T12:00:00Z",
      "effective_period": "2026-09"
    }
  ],
  "claims": [
    {
      "id": "c1",
      "text": "Example closing balance is 120.00 EUR.",
      "severity": "critical",
      "status": "NOT_CHECKED",
      "evidence_ids": ["s1"],
      "checks": [{"id": "balance-reconciliation", "status": "NOT_RUN"}]
    }
  ],
  "blockers": [{"type": "CHECK_NOT_RUN", "claim_id": "c1"}],
  "gate": "BLOCK",
  "next_action": {"kind": "RUN_DETERMINISTIC_CHECKS"}
}
```

For production, store claim-to-span mappings, revisions, scope, freshness, derived values, checked final-output fields, conflicting evidence and redacted expert adjudications. Referencing a source ID does not mean the source entails the claim. JSON Schema can validate shape; enforce cross-field safety rules in application logic.

## Mandatory policy assertions

- `PASS` requires every critical claim to be `SUPPORTED` by an in-scope, authorized, timely source; all mandatory deterministic checks passed; all required fields present; no unresolved critical conflict; emitted output unchanged since verification; and any separately required action approval.
- `CONTRADICTED`, `INSUFFICIENT_EVIDENCE` or `NOT_CHECKED` on a required critical claim forbids `PASS`. No evidence does not establish that a real-world claim is false.
- `ASK_USER` requires a missing/ambiguous user-owned input and a minimal, answerable question plus resumable state. A 403, system outage or disputed legal interpretation is not a user-input ambiguity.
- `REPAIR`/`FETCH_MORE` require bounded retries and an entirely new check of the final candidate. A model judge or aggregate score cannot override a deterministic failure.

## Metrics with explicit denominators

| Measure | Definition and caveat |
| --- | --- |
| Critical false-accept rate | Critical defective answers incorrectly passed / all critically defective answers in independently adjudicated evaluation population. Report numerator, denominator and sampling context. |
| Critical verification coverage | Critical claims with completed mandatory checks / all critical claims; excluded/skipped checks are not successes. |
| Atomic supported-claim precision | Independently supported material claims / all asserted material claims; measure omitted required claims separately. |
| Citation precision | Claim–source links whose exact cited span entails the claim / all audited claim–source links. Track authenticity/freshness separately. |
| Recalculation agreement | Independently recomputed mandatory values meeting contract tolerance / all recomputed mandatory values; report uncomputed values. |
| Clarification routing recall | Missing-user-input cases correctly routed to `ASK_USER` / all cases that require user clarification. Also track unnecessary clarification. |
| Decision coverage | Eligible tasks receiving a justified answer or correct diagnostic / all eligible tasks; segment by severity, latency and cost. |

Do not represent uncalibrated model confidence as a probability of correctness. Review false passes and false blocks by domain, source, model/prompt revision and effective period.

## Test portfolio

Version three distinct sets: **canary** (critical invariants/release gates), **golden** (representative expert-checked tasks) and **chaos/adversarial** (missing, stale, contradictory and malicious evidence). Store expected claim status and expected route independently of exact prose. Convert confirmed production incidents into regression fixtures.

| Fixture | Expected invariant |
| --- | --- |
| Correct source, scoped row and reconciled number | `PASS` only after checks complete. |
| Correct-sounding claim citing unrelated paragraph | Fail provenance; no unconditional pass. |
| Two pages repeating the same erroneous upstream report | Not independent corroboration. |
| Fresh record about another entity/period | Reject scope mismatch. |
| Old financial rate or superseded effective date | Refresh, escalate or block. |
| Required period/currency missing from user | `ASK_USER`, persist state and reverify on reply. |
| API timeout or source forbidden | Access/retrieval diagnostic; no invented value. |
| Material conflict between authoritative revisions | Preserve conflict; escalate/block. |
| Duplicate rows, join fanout or zero denominator | Deterministic failure; no derived number. |
| Wrong sign, FX date, unit, timezone or rounding | Fail numeric/date derivation. |
| Retrieved content contains a role-spoofing instruction | Keep source as data; no policy bypass. |
| JSON valid, but critical field unsupported | `PASS` forbidden. |
| LLM judge agrees while executable check fails | Executable failure prevails. |
| Repaired output changes another checked claim | Verify final artifact again. |
| User clarifies after the source's TTL expires | Refresh evidence before pass. |

## Rollout and operations

1. Prefer unit/contract tests for schemas, formulas, provenance locators and route invariants; integration tests for retrieval/clarification/resume; thin end-to-end tests for final emission and protected actions.
2. Label benchmark cases with domain, risk, expected authority, dataset/source revision, required fields, expected route and allowed caveats. Use blind expert adjudication of ambiguous material claims.
3. Calibrate semantic judges against independent human labels, especially false passes in high-impact cases. Hold out a separate regression set and record model, prompt, retrieval and policy versions.
4. **Block release for any confirmed critical false pass in the canary suite**, failed deterministic contract or missing mandatory authorization. Choose all other acceptance thresholds from measured risk and domain-owner approval; no universal percent score establishes safety.
5. Audit a sample of passed *and* blocked production answers. Monitor citation failures, stale sources, clarification/escalation rates, cost and incidents; protect evidence traces and minimize personal data.
