# MCP Server Engineering Best Practices

Use this reference after locking the target MCP protocol era and SDK major version. Normative requirements come from the selected specification, not from copied snippets or framework memory.

## 1. Protocol and capability discipline

- Record the protocol date/version and SDK package/version in the design brief, lockfile, tests, and release notes.
- Do not mix lifecycle or transport assumptions across protocol eras. Some eras negotiate capabilities through initialization; newer eras may carry version and client capabilities per request.
- Advertise only implemented server capabilities. Invoke client capabilities such as elicitation, roots, sampling, or task support only after verifying that the current request/client declares support.
- Reject unsupported versions and malformed requests with the correct protocol error rather than attempting a best-effort interpretation.
- Paginate list operations (`tools/list`, `resources/list`, `prompts/list`, and domain listings) when the catalog can grow.
- Emit list-changed or resource-updated notifications only when declared and when state genuinely changes.
- Keep version-sensitive details in `research_sources.md` and re-verify them before every substantive skill update.

## 2. Design primitives around control ownership

- Use **tools** for model-controlled parameterized actions and dynamic queries.
- Use **resources** for client-controlled, URI-addressable context and reusable large results.
- Use **prompts** for user-controlled reusable message templates; keep prompt handlers free of side effects.
- Use **elicitation** for simple structured user input only when supported. Never use form elicitation for passwords, API keys, access tokens, or other secrets.
- Use **MCP apps/extensions** for rich visual or interactive UI beyond a simple form.
- Use asynchronous task support only when it exists in the locked protocol/SDK/client matrix; define ownership, TTL, cancellation, result authorization, and cleanup.

## 3. Tool contract quality

Treat the tool catalog as a model-facing API and part of the prompt budget.

### Names and descriptions

- Prefer stable verb-resource names such as `search_issues`, `get_issue`, and `create_issue`.
- Prefix with the service/domain only when hosts are likely to merge conflicting catalogs.
- State purpose, selection criteria, return shape, exclusions, side effects, and important preconditions.
- Disambiguate sibling tools in their descriptions without embedding prompt-injection-like behavioral instructions.
- Keep a small catalog. For large APIs, use a hybrid or search-and-execute pattern and authorize the resolved operation.

### Inputs

- Use strict schemas and reject unknown fields where supported.
- Encode enums, bounds, formats, regexes, defaults, nullable/optional distinctions, and mutually exclusive parameters.
- Keep secrets out of ordinary tool arguments unless the explicit product contract requires them and the host provides a protected secret channel.
- Bound text, arrays, binary data, nesting depth, requested time windows, and computational complexity.
- Validate URLs against schemes, host allowlists, DNS/IP policy, redirect policy, and network boundaries; schema-level URI validation alone does not prevent SSRF.
- Resolve filesystem paths canonically and enforce approved roots after symlink resolution.

### Outputs

- Define `outputSchema` and return `structuredContent` for stable data contracts when supported.
- Also return concise text content for backward compatibility and human inspection.
- Validate output before returning it; do not trust upstream API response shapes.
- Include identifiers and continuation handles required for follow-up calls.
- Prefer resource links for large or reusable content.
- Return explicit metadata for truncation, pagination, warnings, partial completion, and data freshness.
- Set byte/item/token-oriented budgets based on host constraints; do not treat a hardcoded 25,000-character threshold as universally correct.

### Side effects and retries

- Split read and write tools.
- Set `readOnlyHint`, `destructiveHint`, `idempotentHint`, and `openWorldHint` accurately, while treating them as untrusted UX hints rather than policy.
- Add idempotency keys or conditional version checks for retryable mutations.
- Return the created/updated resource identifier and version after mutations.
- Require explicit confirmation or a product-approved approval flow for destructive, financial, publishing, or external-communication actions.

## 4. Errors and recovery

- Use protocol errors for malformed or unsupported protocol requests.
- Return expected operation failures as tool errors with `isError` (or the selected SDK equivalent), not transport crashes.
- Include a stable safe code/category, concise message, retryability, and an actionable next step.
- Map authentication, authorization, not-found, conflict, validation, timeout, cancellation, rate-limit, and upstream-unavailable failures distinctly.
- Preserve retry hints such as `Retry-After` without exposing raw upstream bodies.
- Never return stack traces, secrets, SQL, internal paths, infrastructure names, or cross-tenant details.
- Attach a correlation ID safe for user support; keep details in redacted logs.

## 5. Transport selection and implementation

### Stdio

Use for local subprocesses, development, and controlled single-user installations.

- Reserve stdout exclusively for protocol frames; write diagnostics to stderr.
- Validate environment/configuration before serving while avoiding secret values in failures.
- Handle parent termination, signals, EOF, cancellation, and cleanup.
- Package distributable local servers as MCPB when users should not install runtimes manually.

### Streamable HTTP

Use for remote, multi-user, managed integrations.

- Prefer HTTPS and a single documented MCP endpoint; keep health/readiness endpoints separate.
- Validate `Origin` on incoming browser-capable connections and reject invalid origins. Validate Host/forwarded-host assumptions at the trusted proxy boundary.
- Bind local-only HTTP servers to loopback, not all interfaces.
- Follow the selected protocol era's session model exactly. If sessions exist, generate cryptographically secure IDs, bind them to authorization context, prevent fixation/hijacking, expire them, and never use them as authentication. If the era is stateless, pass explicit scoped handles rather than relying on connection affinity.
- Do not assume SSE is the preferred modern transport. Treat standalone SSE as legacy compatibility unless explicitly required.
- Apply request/body limits, connection limits, keepalive/idle timeouts, bounded queues, backpressure, and graceful shutdown.
- Configure CORS only for known browser origins; CORS is not authentication.

## 6. Authentication and authorization

- Distinguish MCP-server authorization from authorization to an upstream API.
- For protected HTTP servers, publish/discover the metadata required by the chosen MCP auth specification and send standards-compliant `WWW-Authenticate` challenges.
- Validate token signature, expiry, not-before, issuer, audience/resource indicator, scopes, tenant, and revocation policy.
- Accept only tokens intended for the MCP server. Never pass an inbound MCP bearer token through to an upstream API.
- Obtain a separate upstream credential through token exchange, delegated OAuth, workload identity, or a server-owned service account with least privilege.
- Bind authorization to each resolved resource and action; possession of a valid token is not sufficient.
- Protect OAuth state/PKCE/redirect URIs, prevent confused-deputy flows, and obtain per-client/user consent where proxy registration patterns require it.
- Store refresh tokens and keys in a managed secret store or OS keychain, encrypt at rest, rotate, revoke, and audit access.
- Avoid putting credentials in process arguments, URLs, repository files, client-visible logs, examples, or evaluation fixtures.

## 7. Injection and boundary defenses

- Treat user text, resource content, tool output, upstream API content, and tool descriptions from third parties as untrusted data.
- Keep authorization and safety policy outside model-generated content and outside annotations.
- Do not let resource content alter server policy or grant tool permissions.
- Use parameterized database queries; avoid shell invocation. When shell access is unavoidable, use fixed executables and argument arrays with allowlists, never string concatenation.
- Defend against SSRF, redirect bypass, DNS rebinding, local/cloud metadata access, path traversal, symlink escapes, archive bombs, decompression bombs, unsafe deserialization, and oversized payloads.
- Apply tenant isolation to caches, pagination cursors, task handles, resources, logs, and metrics.
- Minimize data returned to the model and redact sensitive fields before formatting.

## 8. Reliability and lifecycle

- Reuse bounded upstream clients and connection pools through SDK lifecycle/lifespan hooks; close them on shutdown.
- Set connect/read/write/pool timeouts and an end-to-end deadline.
- Retry only transient and idempotent operations with exponential backoff and jitter; honor upstream rate-limit headers.
- Propagate cancellation to upstream requests and long loops; roll back or clearly report partial mutations.
- Bound concurrency per process, tenant, user, tool, and upstream dependency.
- Use circuit breakers or load shedding for unstable dependencies where warranted.
- Avoid hidden cross-call state. Make handles opaque, authorized, expiring, revocable, and observable.

## 9. Observability and privacy

- Emit structured logs to stderr for stdio or a normal logging sink for HTTP.
- Record tool name, duration, result category, retry count, payload size, protocol/SDK version, and correlation ID.
- Record actor/tenant/resource/action/outcome for security-relevant mutations without logging sensitive content.
- Redact authorization headers, cookies, tokens, secrets, prompt/resource contents, and PII by default.
- Track SLIs for discovery availability, call success, latency, upstream failures, auth failures, cancellations, throttling, and output truncation.
- Make protocol logging level-aware and capability-aware for versions that support it.

## 10. Verification and release gates

Require:

1. Schema and business-logic unit tests.
2. In-process SDK client tests.
3. Stdio/HTTP transport integration tests.
4. Official MCP Inspector discovery and call checks.
5. Protocol-version and capability mismatch tests.
6. Authn/authz and tenant-isolation tests.
7. SSRF, path, command, injection, payload, and secret-leak tests.
8. Timeout, cancellation, retry, concurrency, and shutdown tests.
9. Agent-selection and end-to-end task evaluations.
10. Dependency, license, SAST, and secret scans.
11. A real-host smoke test for every supported client family.
12. Validated Registry/MCPB metadata when distributing.

## 11. Packaging and supply chain

- Use lockfiles and reproducible builds.
- Pin base images by digest for controlled releases and run as non-root with a read-only filesystem where practical.
- Generate an SBOM and provenance/signing evidence for public or sensitive deployments.
- Publish through short-lived OIDC/trusted publishing rather than static registry tokens.
- Create `server.json` for Official MCP Registry distribution and keep its version, packages, transports, environment variables, ownership marker, hashes, repository, license, and support links consistent with the artifact.
- Validate metadata before publication and verify install/start/call from the published artifact, not only from the source tree.

## 12. Compatibility and change management

Treat these as compatibility-sensitive: tool renames/removals, parameter requirements, enum narrowing, stricter validation, output-schema changes, default changes, side-effect changes, auth/scope changes, resource URI changes, and protocol/SDK upgrades.

- Prefer additive changes and deprecation windows.
- Version the server and distribution artifact coherently.
- Test old clients against new servers and new clients against the supported old baseline.
- Keep a version-sensitive claims ledger and re-run compatibility/conformance suites before release.
