# Risk Scoring and Admission Policy

## Severity definitions

### Critical

A credible path exists to cross a trust boundary with severe impact or no meaningful user control.

Examples:

- confirmed secret exfiltration;
- sandbox/permission bypass;
- malicious executable or dependency with active payload;
- persistence in agent/system startup or shared memory;
- unauthorized signing/payment/admin/deploy capability;
- deliberate self-modification of security controls to conceal behavior.

Default action: REJECT or QUARANTINE.

### High

A strong prerequisite for compromise exists or a privileged behavior is insufficiently constrained.

Examples:

- arbitrary shell or unrestricted network requirement;
- install-time script from an untrusted dependency;
- policy-override or approval-bypass instructions;
- executable binaries without trustworthy provenance;
- archive path traversal/symlink escape;
- undeclared privileged capability.

Default action: block admission until remediated.

### Medium

A weakness increases attack surface but normally needs additional conditions or compensating failures.

Examples:

- unpinned dependency or mutable reference;
- broad but read-only repository access;
- suspicious encoding requiring manual review;
- undocumented network destination;
- dependency manifest without a lockfile.

Default action: remediate or accept with documented owner and deadline.

### Low / Info

Hardening or maintainability issue with limited direct exploitability.

Default action: backlog or document.

## Absolute blockers

Admission must not pass with an unresolved finding involving:

- secret/data exfiltration;
- sandbox or harness escape;
- higher-priority policy override;
- unauthorized persistent modification;
- malware or unexplained executable payload;
- unauthorized external write or high-impact action;
- privilege escalation;
- disabling/removing the security gate in the same change without independent approval.

## Suggested CI threshold

Fail automatically on high and critical. Report medium and below for review.

Do not convert the policy to a simple average score. One Critical finding must not be hidden by many clean checks.

## Suppressions

Allow suppression only when all of the following are recorded:

- exact rule ID;
- exact path or narrow scope;
- business/technical justification;
- reviewer identity;
- expiry or reevaluation condition for non-trivial risk.

A suppression changes triage, not the underlying capability boundary. Harness restrictions still apply.
