# Threat Model for Skills

A skill is both content and executable influence. Natural-language instructions can change agent behavior as effectively as code when the agent can call tools.

## Protected assets

- System/developer/harness policies.
- User and organization data.
- Credentials, tokens, keys, cookies, environment variables.
- Source repositories and CI/CD identities.
- Local filesystem and host environment.
- Connected tools/plugins/MCP servers.
- External communication and publication channels.
- Persistent memory and agent configuration.
- Production/cloud/payment/admin capabilities.
- Audit logs and provenance.

## Threat classes

### Instruction-layer threats
- Direct prompt injection.
- Indirect injection from files, web, RAG, tool output, logs, test output, issues, PRs, PDFs, email, or MCP responses.
- Jailbreak/policy override.
- Hidden Unicode, zero-width, homoglyph, encoded or compressed instructions.
- Authority spoofing such as fake SYSTEM/DEVELOPER markers.
- Multi-turn delayed payloads and memory poisoning.

### Tool and agency threats
- Excessive agency.
- Tool selection hijacking.
- Dangerous argument manipulation.
- Confirmation bypass.
- Recursive agent spawning.
- Resource exhaustion or unbounded retries.
- Unauthorized external publication or mutation.

### Data threats
- Secret enumeration.
- Credential harvesting.
- Cross-user or cross-tenant access.
- PII/private-data exfiltration.
- Covert exfiltration via DNS, URL parameters, logs, issue comments, telemetry, or generated artifacts.

### Host and persistence threats
- Writing shell/profile startup files.
- Git hooks, CI workflow modification, scheduled tasks.
- Package-manager startup/install hooks.
- Modifying agent settings, policies, skills, plugins, or memory to survive future sessions.
- Sandbox escape and host filesystem discovery.

### Supply-chain threats
- Typosquatting/dependency confusion.
- Mutable branch/tag references.
- Unreviewed binaries.
- curl|sh / wget|bash bootstrap.
- postinstall/preinstall execution.
- Compromised GitHub Actions or overly broad workflow tokens.
- Missing provenance/SBOM/signatures.
- Malicious transitive dependencies.

## Adversary personas

1. Malicious skill author.
2. Compromised upstream maintainer.
3. Attacker controlling retrieved content.
4. Repository contributor inserting hostile instructions.
5. Tool/MCP server returning adversarial output.
6. Insider seeking privilege escalation.
7. Opportunistic dependency attacker.
8. Accidental author who requests dangerously broad capabilities.

## Security objective

Even if the model follows hostile instructions, technical boundaries should constrain impact to the skill's explicitly approved capabilities.

The key property is:

`effective_capability(skill) <= declared_capability <= harness_capability <= system_policy`

Any violation is a security finding.
