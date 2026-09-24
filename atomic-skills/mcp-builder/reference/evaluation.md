# MCP Server Verification and Evaluation Guide

Use layered verification. Agent evaluations complement protocol, security, and business-logic tests; they do not replace them.

## Release-gate matrix

| Layer | Purpose | Minimum evidence |
|---|---|---|
| Static | Catch type, lint, dependency, secret, and unsafe-code defects | Clean type/lint/build; reviewed dependency/secret/SAST results |
| Unit | Verify schemas, policy, pagination, output shaping, idempotency, and errors | Deterministic tests for success and boundary/failure cases |
| In-process | Verify SDK registration and request/result contracts | SDK client can discover and call every representative primitive |
| Transport | Verify stdio or Streamable HTTP framing/lifecycle | Startup, discovery, call, cancellation, shutdown, malformed input tests |
| Conformance | Verify protocol interoperability | Official MCP Inspector manual and scripted evidence |
| Security | Verify trust boundaries | Authn/authz, audience, tenant, Origin/Host, SSRF/path/command, leakage tests |
| Agent | Verify model usability | Tool-selection and task-success suite with frozen fixtures |
| Host smoke | Verify real integration | At least one smoke test per supported client/host family |

## Contract and conformance tests

Test at least:

- Protocol-version success and unsupported-version failure.
- Capability advertisement and capability-gated behavior.
- Paginated `tools/list`, `resources/list`, and `prompts/list` where applicable.
- Valid, invalid, unknown, missing, oversized, and adversarial tool arguments.
- Agreement between `outputSchema`, `structuredContent`, and text fallback.
- Expected tool errors versus protocol errors.
- Resource URI parsing, templates, MIME types, roots, and authorization.
- Prompt argument validation and side-effect freedom.
- Elicitation accept/decline/cancel and unsupported-client fallback.
- Timeouts, cancellation, retries, progress, connection close, and lifecycle cleanup.
- Concurrency, tenant isolation, pagination cursor isolation, and partial failures.
- Stdio stdout cleanliness or HTTP status/header/body correctness.

Use the official MCP Inspector to inspect discovery metadata and exercise representative calls. Pin the Inspector version in CI or record it in the test report.

## Security test cases

Require negative tests for:

1. Missing, expired, wrong-issuer, wrong-audience, wrong-scope, wrong-tenant, and revoked tokens.
2. Inbound-token passthrough attempts and upstream credential confusion.
3. Confused-deputy/OAuth state, redirect URI, PKCE, and client-consent failures where applicable.
4. Invalid Origin/Host, DNS rebinding assumptions, untrusted forwarded headers, and loopback exposure.
5. SSRF to loopback, private ranges, cloud metadata, redirects, alternate IP encodings, and DNS changes.
6. Path traversal, absolute paths, symlink escapes, unsafe archive extraction, and unauthorized roots.
7. Command/SQL/template injection and unsafe deserialization.
8. Prompt/tool/resource injection attempts that try to override server policy.
9. Oversized text, arrays, binary payloads, deep nesting, expensive filters, and decompression bombs.
10. Cross-tenant resources, task handles, cursors, caches, logs, and error disclosures.
11. Secrets in stdout, logs, traces, exceptions, tool content, structured content, fixtures, and reports.
12. Destructive/retry behavior, idempotency-key reuse, and concurrent mutation conflicts.

Use dedicated scanners as supporting evidence, not as substitutes for threat-model-driven tests.

## Agent evaluation design

Measure whether a model can use the visible contract correctly. Include these categories:

- **Selection:** choose the correct tool among siblings and avoid tools outside scope.
- **Arguments:** produce valid constrained inputs without repeated correction.
- **Composition:** complete realistic multi-call workflows.
- **Recovery:** follow actionable validation, not-found, rate-limit, and conflict errors.
- **Safety:** seek approval where required and avoid destructive alternatives.
- **Efficiency:** minimize calls, latency, and input/output tokens while preserving correctness.
- **Output use:** consume structured output, identifiers, cursors, resource links, and freshness metadata correctly.
- **Compatibility:** run representative cases across supported hosts/models because tool-use behavior differs.

Use frozen fixtures, recorded/mock upstream responses, fixed time windows, and deterministic expected results. Keep a small live smoke suite separate from deterministic regression tests.

## Evaluation dataset format

Prefer JSONL or YAML with explicit metadata rather than a bare question/answer pair. Example:

```yaml
- id: issue-search-001
  category: selection
  prompt: Find the closed authentication issue from April 2025 and return its issue number only.
  expected:
    final: "431"
    required_tools: [search_issues, get_issue]
    forbidden_tools: [create_issue, update_issue]
    max_calls: 6
  fixture: github-april-2025-v1
  tags: [read-only, pagination, multi-hop]
```

A legacy XML dataset may be retained for the bundled harness, but document its limitations: exact string comparison alone does not detect unsafe calls, unnecessary calls, invalid intermediate arguments, leakage, or partial correctness.

## Scoring

Track separately:

- Final-answer/task success.
- Correct first tool selection.
- Valid arguments on first attempt.
- Required/forbidden tool compliance.
- Safety/approval compliance.
- Error-recovery success.
- Call count and wall-clock latency.
- Input/output token or byte cost.
- Tool-level error and retry counts.
- Cross-host/model pass rate.

Do not collapse all signals into one score without preserving the components. Define release thresholds by risk; mutation and security cases require stricter thresholds than read-only convenience tools.

## Evaluation development loop

1. Snapshot the visible tool/resource/prompt catalog.
2. Create realistic tasks from user workflows and known failure modes.
3. Freeze or mock underlying data and independently verify expected results.
4. Add near-neighbor tools and ambiguous wording to test selection without making the expected result ambiguous.
5. Run a baseline across target hosts/models.
6. Inspect full traces for wrong selections, malformed inputs, oversized outputs, unsafe actions, and misleading errors.
7. Improve names, descriptions, schemas, result shapes, or tool boundaries—not only the evaluator prompt.
8. Re-run and compare against the versioned baseline.
9. Gate releases on no critical regression and on defined per-category thresholds.

## CI recommendations

- Start the built artifact, not source-only development entry points.
- Allocate random ports or use in-process transports; enforce hard test timeouts and guaranteed cleanup.
- Scrub credentials and response bodies from artifacts.
- Save catalog snapshots, Inspector version, protocol/SDK versions, fixture hash, model/host identifier, metrics, and redacted traces.
- Separate deterministic checks from paid/non-deterministic model evaluations; run deterministic gates on every change and broader cross-model suites on release or scheduled builds.
- Quarantine only demonstrably flaky external smoke tests; never quarantine authz or destructive-action tests.

## Exit criteria

Release only when:

- Static, unit, integration, transport, conformance, and critical security gates pass.
- All tools have representative success, validation, authorization, upstream-failure, timeout, and cancellation coverage.
- Agent evaluations meet category-specific thresholds and contain no forbidden mutation or data-leak event.
- Published package/Registry/MCPB installation passes the smoke suite.
- Results and known limitations are documented in a reproducible report.
