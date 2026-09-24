# MCP Builder Research Sources and Maintenance Ledger

Last reviewed: 2026-09-14 UTC.

## Source policy

Use the current official specification and exact SDK-major documentation as the authority for normative behavior. Use established open-source repositories for implementation, testing, security-scanning, packaging, and evaluation practices. Do not copy code or guidance from an external repository unless its license permits the intended use; summarize findings when license scope is uncertain.

The project requirement allows only GitHub repositories with at least 5 stars or 5 forks. Every repository below exceeded both thresholds when reviewed.

## Qualifying repositories

| Repository | Role in this update | Stars | Forks | Last checked |
|---|---|---:|---:|---|
| https://github.com/modelcontextprotocol/modelcontextprotocol | Specification, schema, protocol-era changes, security requirements | 9,202 | 1,794 | 2026-09-14 |
| https://github.com/modelcontextprotocol/python-sdk | Official Python SDK APIs, structured output, lifespan, in-process testing | 24,288 | 3,915 | 2026-09-14 |
| https://github.com/modelcontextprotocol/typescript-sdk | Official TypeScript SDK APIs, v1/v2 differences, Streamable HTTP | 13,389 | 2,176 | 2026-09-14 |
| https://github.com/modelcontextprotocol/inspector | Interactive/scripted conformance and transport testing | 10,873 | 1,516 | 2026-09-14 |
| https://github.com/modelcontextprotocol/registry | `server.json`, ownership verification, hashes, publishing workflow | 7,244 | 989 | 2026-09-14 |
| https://github.com/anthropics/claude-plugins-official | Reference MCP server development skill patterns and progressive disclosure | 36,245 | 4,068 | 2026-09-14 |
| https://github.com/ComposioHQ/awesome-claude-skills | Original skill provenance and baseline | 74,985 | 8,662 | 2026-09-14 |
| https://github.com/Jeffallan/claude-skills | Comparison with an alternate MCP developer skill | 11,455 | 1,100 | 2026-09-14 |
| https://github.com/cisco-ai-defense/mcp-scanner | MCP-specific security scanning categories | 1,071 | 137 | 2026-09-14 |
| https://github.com/snyk/agent-scan | Agent/MCP/skill scanning and safe consent defaults | 3,036 | 271 | 2026-09-14 |
| https://github.com/MCPJam/inspector | Cross-client agent evaluations and JSON-RPC/OAuth trace visibility | 2,203 | 278 | 2026-09-14 |

Counts are evidence of eligibility, not quality guarantees, and naturally change. Re-query GitHub before adding a new source.

## Authoritative documentation entry points

- Current MCP specification index: https://modelcontextprotocol.io/specification/
- Current MCP documentation export: https://modelcontextprotocol.io/llms-full.txt
- Official Python SDK documentation: https://py.sdk.modelcontextprotocol.io/
- Official TypeScript SDK documentation: https://ts.sdk.modelcontextprotocol.io/
- MCP Inspector documentation: https://modelcontextprotocol.io/docs/tools/inspector
- Official MCP Registry documentation: https://registry.modelcontextprotocol.io/docs
- MCP security best practices: use the security page under the selected protocol version rather than an unversioned cached copy.

## Findings incorporated

1. **Version/era locking:** Protocol lifecycle and transport semantics have changed enough that examples from different eras cannot safely be merged.
2. **Transport modernization:** Streamable HTTP is the modern remote transport; standalone SSE belongs in a compatibility path. Stdio remains appropriate for local subprocesses.
3. **HTTP hardening:** Validate Origin, trusted Host/proxy assumptions, loopback binding, HTTPS, body/connection limits, and the selected era's state/session semantics.
4. **Authorization:** Validate token audience/resource, issuer, expiry, scope, tenant, and resource-level access. Never pass inbound MCP tokens through to upstream APIs. Address confused-deputy risks.
5. **Structured outputs:** Use `outputSchema` and `structuredContent` where supported, validate output, and retain text fallback for host compatibility.
6. **Capability gating:** Elicitation, roots, sampling, progress, tasks, and other optional client features require protocol/SDK-specific support checks and fallback behavior.
7. **State discipline:** Prefer stateless calls. Represent necessary cross-call state through explicit opaque, scoped, expiring handles rather than connection affinity.
8. **Agent-centric tools:** Tool names, descriptions, schemas, result shape, and context size directly determine model success. Use hybrid/search-execute patterns for large action surfaces.
9. **Layered testing:** Combine static, unit, in-process, transport, Inspector/conformance, security, agent evaluation, and real-host smoke tests.
10. **Supply chain:** Validate Registry metadata, ownership markers, integrity hashes, artifact installation, lockfiles, secret/dependency scans, SBOM/provenance, and short-lived trusted publishing.

## Version-sensitive claims ledger

Verify these before changing examples or making recommendations:

| Claim | Verification target |
|---|---|
| Current stable MCP protocol date and lifecycle model | Specification index, changelog, and schema for that date |
| Whether initialize/session headers exist | Selected protocol transport and lifecycle pages |
| Whether sampling is current, deprecated, or replaced | Selected protocol client-capability pages and changelog |
| Tool task-support fields and task semantics | Selected protocol tools/tasks pages |
| Python package/import/decorator/context names | Exact Python SDK major-version docs and installed package |
| TypeScript package split/import paths/registration API | Exact TypeScript SDK major-version docs and installed package |
| Structured-output field names | Selected protocol schema plus exact SDK docs |
| Elicitation schema/modes and sensitive-input rules | Selected protocol elicitation page |
| OAuth metadata, CIMD/DCR, challenge, and resource indicator requirements | Selected protocol authorization/security pages |
| Registry `server.json` schema and ownership/hash rules | Current Official Registry docs/schema |
| MCPB manifest schema and packaging commands | Current MCPB repository/docs |
| Inspector CLI syntax and supported protocol eras | Installed Inspector version/docs |

## Update procedure

1. Record the review date.
2. Resolve the current stable specification and read its changelog from the previous skill baseline.
3. Resolve current Python/TypeScript SDK major versions and migration guides.
4. Verify Inspector, Registry, and MCPB documentation.
5. Re-query GitHub metadata for every newly proposed repository and reject sources below 5 stars and 5 forks unless the project rule is explicitly changed.
6. Review security best practices and at least one maintained MCP/agent security scanner for newly recognized attack classes.
7. Update `SKILL.md` first; move detailed rules into references to preserve progressive disclosure.
8. Validate all relative links, frontmatter, examples, and commands.
9. Run a dry-run task with the skill for local stdio, remote authenticated HTTP, and a large-API search/execute design.
10. Record changed claims, limitations, and any compatibility assumptions.

## Known limitations

- Repository popularity does not establish correctness or security.
- Host capabilities differ and may lag the specification.
- SDK prereleases may document future protocol behavior; prefer stable packages unless explicitly evaluating a prerelease.
- This skill provides design and validation guidance, not an automatic certification of an MCP server.
