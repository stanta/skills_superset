---
name: mcp-builder
description: This skill should be used when designing, building, reviewing, securing, testing, packaging, publishing, or modernizing Model Context Protocol (MCP) servers in Python or TypeScript, including tool/resource/prompt interfaces, stdio or Streamable HTTP transports, OAuth, elicitation, structured outputs, protocol compatibility, Inspector validation, agent evaluations, MCPB packaging, and Registry metadata.
license: Complete terms in LICENSE.txt
metadata:
  category: development
  version: "2.0.0"
  updated: "2026-09-14"
  source:
    repository: https://github.com/ComposioHQ/awesome-claude-skills
    path: mcp-builder
  research:
    - https://github.com/modelcontextprotocol/modelcontextprotocol
    - https://github.com/modelcontextprotocol/python-sdk
    - https://github.com/modelcontextprotocol/typescript-sdk
    - https://github.com/modelcontextprotocol/inspector
    - https://github.com/modelcontextprotocol/registry
    - https://github.com/anthropics/claude-plugins-official/tree/main/plugins/mcp-server-dev
---

# MCP Server Builder

Design MCP servers as agent-facing products rather than mechanical API wrappers. Optimize for correct tool selection, bounded context use, explicit side effects, secure authorization, protocol interoperability, and observable operation.

## Mandatory workflow

Follow these phases in order. Skip discovery questions already answered by the user.

### Phase 1 — Discover the integration

Determine:

1. **System boundary** — cloud API, database, local process, filesystem, desktop application, hardware, or pure computation.
2. **Users and trust boundary** — one developer, an internal team, tenants, or public distribution.
3. **Required primitives** — tools for actions, resources for addressable context, prompts for user-invoked templates, elicitation for mid-flow user input, or an MCP app for rich UI.
4. **Action-surface size** — dedicated tools for a small stable surface; search-and-execute or progressive discovery for a large or dynamic catalog.
5. **Authentication** — none, setup-time API key, user-scoped OAuth, service identity, or delegated upstream access.
6. **Data sensitivity and side effects** — PII, secrets, regulated data, writes, destructive actions, money movement, publication, or external communication.
7. **Deployment and compatibility targets** — local stdio, remote Streamable HTTP, MCPB, target hosts, protocol era, SDK major version, and runtime constraints.
8. **Success criteria** — correct tool selection, task completion, latency, output size, failure behavior, auditability, and release gates.

Produce a brief design decision before writing code: deployment model, protocol/SDK baseline, primitive map, tool pattern, auth model, and test strategy.

### Phase 2 — Lock the protocol era and current documentation

Treat MCP and its SDKs as version-sensitive. Before scaffolding:

1. Fetch the current MCP specification and changelog.
2. Fetch the documentation for the exact Python or TypeScript SDK major version selected.
3. Record the protocol date/version, SDK package/version, runtime version, and supported client hosts.
4. Do not combine lifecycle, transport, auth, or API examples from different protocol eras without an explicit compatibility adapter.
5. Treat SSE as a legacy compatibility transport unless the chosen SDK/client matrix explicitly requires it. Prefer stdio for local subprocesses and Streamable HTTP for remote servers.
6. Load `reference/research_sources.md` to verify source provenance and version-sensitive claims.
7. Load the matching language guide: `reference/python_mcp_server.md` or `reference/node_mcp_server.md`.

### Phase 3 — Design the agent-facing contract first

Draft the interface visible to clients before implementation:

- Use stable, specific, action-oriented tool names. Add a service/domain prefix only when collision risk justifies the extra tokens.
- State what each tool does, when to use it, what it returns, important exclusions, and side effects.
- Split read and write operations. Never hide arbitrary HTTP methods, shell execution, SQL, paths, or URLs behind a broad tool unless the use case explicitly requires a constrained expert interface.
- Express constraints in JSON Schema/Pydantic/Zod: enums, formats, bounds, patterns, defaults, mutually exclusive fields, and unknown-field rejection where supported.
- Prefer opaque cursors over offsets when the upstream API supplies cursors. Bound every collection and return continuation metadata.
- Define `outputSchema` and return `structuredContent` for data-bearing tools when the selected protocol/SDK supports them. Also provide a concise text content fallback for hosts that do not consume structured output.
- Return IDs, versions, timestamps, and next-step handles needed for follow-up calls; omit noisy upstream fields by default.
- Mark annotations accurately, but never use annotations as authorization controls.
- Use resource links for large reusable payloads instead of embedding them repeatedly.
- Keep normal tools stateless across calls. When cross-call state is unavoidable, return an explicit opaque handle with scope, TTL, authorization binding, and cleanup semantics.

Load `reference/mcp_best_practices.md` for the detailed contract, transport, security, and operations checklist.

### Phase 4 — Implement secure infrastructure before tools

Create shared components for configuration, upstream clients, authentication/authorization, retries, pagination, output shaping, errors, observability, and lifecycle cleanup.

Enforce these controls:

- Read secrets from environment injection or a secret manager; never hardcode, log, return, or request credentials through ordinary form elicitation.
- Validate identity, token signature/expiry/issuer/audience, tenant, scopes, and resource-level authorization on every protected operation.
- Never pass an inbound MCP bearer token through to an upstream API. Obtain or exchange a separate upstream token for the intended resource.
- Apply least privilege, SSRF defenses, path/root containment, command allowlists, parameterized queries, payload limits, timeouts, bounded concurrency, rate limits, and redacted logs.
- For Streamable HTTP, validate `Origin` and host expectations, reject invalid origins, bind local-only services to loopback, use HTTPS remotely, and follow the selected protocol era's session rules exactly.
- For stdio, reserve stdout exclusively for protocol messages and send diagnostics to stderr.
- Honor cancellation and deadlines. Report progress only when requested/supported.
- Gate elicitation and other client-provided capabilities on declared support and provide a deterministic fallback.
- Keep health/readiness endpoints separate from the MCP endpoint.

### Phase 5 — Test at four levels

1. **Unit tests** — schemas, authorization, output shaping, pagination, idempotency, and error mapping.
2. **In-process/transport integration tests** — discovery, valid and invalid calls, cancellation, timeouts, concurrent requests, lifecycle cleanup, and protocol-version mismatch.
3. **Conformance and security tests** — inspect tools/resources/prompts with the official MCP Inspector; test malformed JSON-RPC, stdout cleanliness, Origin/Host validation, token audience, SSRF/path traversal, secret leakage, and dependency findings.
4. **Agent evaluations** — measure correct tool choice, valid arguments, task success, recovery from actionable errors, call count, latency, and output/token cost across realistic hosts/models.

Do not define quality as “the server starts.” Require repeatable automated checks and at least one real-host smoke test. Load `reference/evaluation.md` for the release-gate workflow.

### Phase 6 — Package, publish, and operate

- Package local distribution as MCPB when a runtime-bundled local installation is required; retain raw stdio for development and controlled environments.
- For Registry publication, create and validate `server.json`, ownership verification metadata, package integrity hashes where applicable, version alignment, repository/license/support links, transport declarations, and configuration variables.
- Pin production dependencies with a lockfile, generate an SBOM when appropriate, scan dependencies and secrets, and use provenance-aware CI publishing rather than long-lived registry tokens.
- Publish tool and schema changes with semantic versioning and compatibility notes. Treat renames, removed fields, stricter validation, changed side effects, and changed defaults as compatibility risks.
- Instrument request counts, latency, upstream errors, authorization failures, rate limits, cancellations, payload sizes, and redacted audit events.
- Define rollback, revocation, key rotation, incident response, and deprecation procedures.

## Primitive selection

| Need | Primitive |
|---|---|
| Model invokes a parameterized action or query | Tool |
| Client browses or reads URI-addressable context | Resource or resource template |
| User starts a reusable message workflow | Prompt |
| Server needs simple structured user input mid-flow | Elicitation with capability check and fallback |
| User needs rich interactive UI | MCP app/extension |
| Operation runs asynchronously for a long time | Task support only when available in the locked protocol/client matrix |

Do not use resources or prompts merely to demonstrate protocol coverage. Add primitives only when they improve a real workflow.

## Tool-surface patterns

- **Dedicated tools:** Prefer for roughly 1–15 clear operations.
- **Hybrid catalog:** Promote the common 3–5 operations and place the long tail behind discovery.
- **Search + execute:** Use for dozens or hundreds of dynamic actions. Validate the selected action's schema server-side and authorize the resolved operation, not only the generic executor.

Avoid using a universal executor as a shortcut around careful tool design or security policy.

## Error contract

Distinguish:

- **Protocol errors** for malformed/unsupported JSON-RPC or protocol requests.
- **Tool execution errors** as tool results with the protocol's error indicator, a safe code/category, concise explanation, retryability, and an actionable next step.
- **Transport/auth HTTP errors** with standards-compliant status and challenge headers where required.

Never expose stack traces, secrets, raw upstream bodies, SQL, internal paths, or tenant data. Preserve detailed correlation-aware diagnostics only in redacted server logs.

## Required deliverables

Produce or update:

1. Interface/design brief and threat model.
2. Runnable server implementation using the selected official SDK or justified framework.
3. Typed input/output contracts and primitive registrations.
4. Deployment/client configuration with secret placeholders only.
5. Unit, integration, conformance, security, and agent-evaluation assets.
6. README with install, configuration, permissions, tool catalog, examples, limitations, and troubleshooting.
7. Registry/MCPB metadata when distribution requires it.
8. Version/compatibility ledger and release checklist.

## Completion gates

Do not declare completion until:

- The exact protocol/SDK baseline is documented.
- Discovery and calls pass through the intended transport.
- Inputs and structured outputs validate.
- Read/write boundaries and annotations match actual behavior.
- Authentication and resource-level authorization fail closed.
- Pagination, output budgets, timeouts, cancellation, and cleanup are tested.
- No secret reaches source, stdout protocol frames, tool results, or unredacted logs.
- Inspector/conformance checks and agent task evaluations pass defined thresholds.
- Distribution metadata validates, when applicable.
- Documentation enables another developer to add or modify a tool without rediscovering core decisions.

## Reference files

Load only the references needed for the task:

- `reference/mcp_best_practices.md` — protocol, interface, security, transport, and operations rules.
- `reference/python_mcp_server.md` — current Python SDK workflow and verification gates.
- `reference/node_mcp_server.md` — current TypeScript SDK workflow and verification gates.
- `reference/evaluation.md` — layered testing and agent-evaluation process.
- `reference/research_sources.md` — authoritative sources, qualifying repositories, evidence, and update procedure.
