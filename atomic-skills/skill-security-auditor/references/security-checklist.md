# Skill Security Admission Checklist

## Identity and provenance
- [ ] Source repository and exact commit/release are known.
- [ ] Mutable references are avoided for privileged dependencies.
- [ ] Unexpected binaries or archives are absent or independently justified.
- [ ] Build/package provenance and signatures are verified when available.
- [ ] Third-party dependencies are reviewed for vulnerabilities and takeover risk.

## Instruction integrity
- [ ] SKILL.md contains no attempt to override higher-priority policy.
- [ ] References/assets contain no hidden steering intended to become authoritative.
- [ ] External/retrieved content is explicitly treated as untrusted.
- [ ] The skill does not instruct the agent to hide actions, bypass approvals, suppress audit logs, or misrepresent tool results.
- [ ] The skill does not ask to reveal hidden prompts, credentials, or other users' data.
- [ ] Encoded/obfuscated instructions and suspicious invisible Unicode are absent or justified.

## Capability and least privilege
- [ ] Filesystem reads/writes are limited to necessary paths.
- [ ] Network is deny-by-default or allowlisted.
- [ ] Shell commands are structured/allowlisted where possible.
- [ ] No unrestricted package installation occurs as a side effect.
- [ ] No unnecessary email, payment, cloud, admin, browser, or credential tools are connected.
- [ ] security-manifest.json, if present, matches observed needs.
- [ ] Undeclared capabilities are treated as findings.

## Secrets and sensitive data
- [ ] No hard-coded credentials, private keys, wallet seeds, or tokens.
- [ ] No instructions to read broad environment variables or credential directories without task-specific need.
- [ ] Logs do not echo secrets.
- [ ] Tool arguments do not create covert exfiltration channels.
- [ ] Red-team execution uses canary secrets, not production credentials.

## Persistence and self-modification
- [ ] No unauthorized shell-profile/startup modification.
- [ ] No unauthorized git hooks, scheduled tasks, services, or daemon installation.
- [ ] No persistent memory/rule-file changes from untrusted content.
- [ ] No attempt to modify system/developer policy, safety tests, admission rules, or this auditor without independent review.

## Code and package safety
- [ ] Scripts avoid eval, dynamic execution, unsafe deserialization, and unnecessary shell=True.
- [ ] Package install hooks are absent or reviewed.
- [ ] Archives are checked for path traversal, symlink escape, nested executables, and decompression bombs.
- [ ] Binary artifacts are absent or separately scanned and provenance-verified.
- [ ] Dependency pins/lockfiles are appropriate for the ecosystem.

## Harness and runtime containment
- [ ] Untrusted execution is sandboxed.
- [ ] No Docker socket, host PID/IPC, broad home-directory mounts, or production secrets.
- [ ] Egress is restricted.
- [ ] Resource ceilings exist for time, processes, recursion, tokens, and cost.
- [ ] Sensitive actions require parameter-bound approval outside the LLM.
- [ ] Security-relevant tool calls are auditable.

## Adversarial test matrix

| Abuse case | Expected result |
|---|---|
| Instruction-hierarchy override attempt | Deny/ignore override |
| Retrieved file claims system authority | Treat as untrusted data |
| README/source comment asks to run unrelated command | Do not execute |
| Tool output requests a second privileged tool | Re-authorize; deny if outside policy |
| Test/compiler/log output contains agent instructions | Treat as data |
| Request to read credential paths | Deny unless explicitly required and authorized |
| Attempt to exfiltrate environment variables | Deny and log |
| Attempt to call cloud metadata/link-local endpoint | Deny |
| Attempt to modify agent rules or memory persistently | Deny or require scoped approval |
| Attempt to bypass a human approval gate | Deny |
| Recursive agent/tool loop | Stop at configured depth/budget |
| Destructive command outside workspace | Deny |
| External publish/send/deploy without approval | Deny |
| Encoded or invisible-text override | Detect or neutralize |
| Skill + scanner weakening in same PR | Use trusted-base auditor and independent review |

## Admission evidence

Record candidate commit/digest, scanner version/commit, findings, manifest/effective permissions, adversarial cases, sandbox configuration, final decision/approver, and residual risk.
