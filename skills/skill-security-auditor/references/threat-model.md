# Threat Model for Agent Skills

## Asset under assessment

An agent skill is an instruction package that may contain natural-language policy, scripts, references, assets, tool descriptions, configuration, and dependencies. Because an agent may execute or obey these materials, treat the package as both software and control-plane input.

## Protected assets

- system/developer/harness policy integrity;
- user data and private files;
- credentials, tokens, wallets, signing material, and environment secrets;
- source code and repository integrity;
- connected SaaS, cloud, GitHub, email, payments, and admin systems;
- long-term memory and cross-session state;
- CI/CD runners and build provenance;
- external reputation and user-visible actions;
- compute/token budget and availability.

## Adversary profiles

### Malicious skill publisher

Goal: gain code execution, steal data, obtain durable access, or influence future agent behavior.

Typical vectors: hidden instructions, install hooks, malicious dependency, encoded payload, network exfiltration, persistent rule-file modification.

### Compromised upstream maintainer or dependency

Goal: abuse trusted provenance or package updates.

Typical vectors: dependency takeover, mutable tags, poisoned release asset, compromised CI token, altered MCP/tool definition.

### Prompt-injection author

Goal: use content read by the agent to override the intended task.

Typical vectors: README text, issue/PR body, source comments, web pages, PDFs, logs, test/compiler output, retrieved memory, tool return values.

### Curious or compromised agent

Goal: overreach beyond user intent because it has excessive tools or ambiguous instructions.

Typical vectors: arbitrary shell, broad filesystem reads, unrestricted network, automatic package installation, high-impact actions without approval.

### Insider or reviewer-bypass attacker

Goal: weaken the gate while introducing a malicious skill.

Typical vectors: modify scanner/rules/workflow in the same PR, remove tests, change fail threshold, replace pinned CI actions, broaden workflow token permissions.

## Attack classes

1. Policy hierarchy override — instructions that claim authority over system, developer, platform, or harness controls.
2. Direct/indirect prompt injection — hostile instructions in user or retrieved content.
3. Tool poisoning/shadowing — malicious tool names, descriptions, schemas, or return values.
4. Excessive agency — tools, scopes, autonomy, retries, or side effects broader than required.
5. Secret and data exfiltration — reading sensitive values and sending them through network, logs, tool arguments, prompts, or output.
6. Persistence — modifying shell profiles, agent rules, memory, git hooks, scheduled tasks, startup files, or other future execution paths.
7. Self-modification / guardrail tampering — changing the auditor, system prompt, policy files, safety tests, or permission configuration.
8. Software supply chain — malicious dependencies, install scripts, binaries, archives, unsigned artifacts, mutable references.
9. Sandbox escape / host abuse — Docker socket, host mounts, symlink escape, metadata endpoints, privileged namespaces, local service access.
10. Resource abuse — recursive agents, infinite retries, fork/process explosions, decompression bombs, oversized context, excessive paid API usage.
11. Memory poisoning — storing attacker-controlled steering in persistent memory or shared knowledge stores.
12. Approval manipulation — forging, reusing, broadening, or bypassing approval for high-impact actions.

## Security objectives

- A malicious skill cannot obtain capabilities it was not explicitly granted.
- Untrusted data cannot become authoritative merely because the model reads it.
- Sensitive actions are independently authorized outside the model.
- Candidate skill code executes only in a contained environment during evaluation.
- Changes to the admission mechanism itself require independent review.
- Release artifacts are traceable to reviewed source and immutable revisions.

## Assumptions and limitations

Static scanning is a triage mechanism, not proof of safety. Semantic prompt attacks, logic bombs, dependency compromise, and model-specific behavior require manual review and adversarial testing. Conversely, security documentation may intentionally contain dangerous strings; documented suppressions may be needed, but suppressions themselves require review.
