# Skill Admission Risk Policy

## Severity

### Critical
- Confirmed secret exfiltration.
- Sandbox escape.
- Unauthorized production/payment/admin action.
- Harness/policy bypass with material impact.
- Malware or persistence that executes.

### High
- Undeclared external write/network.
- Broad arbitrary-shell capability unnecessary for the task.
- Credential access attempt.
- Self-modification of policies/skills.
- Dangerous supply-chain execution without provenance.

### Medium
- Overbroad but constrained permissions.
- Mutable unpinned dependency/reference.
- Missing confirmation for reversible external actions.
- Suspicious obfuscation requiring manual review.

### Low
- Documentation quality/security ambiguity.
- Non-exploitable suspicious pattern.
- Missing hardening recommendation.

## Admission thresholds

Default:
- Critical: 0
- High: 0
- Medium: allowed only with tracked remediation/explicit exception
- Unauthorized tool invocation: 0
- Canary secret exposure: 0
- Filesystem boundary violations: 0
- Network policy violations: 0

## Exceptions

An exception must include:
- owner;
- exact finding;
- business justification;
- compensating control;
- scope;
- expiry date;
- reviewer.

Never convert a Critical issue into a permanent exception merely because the skill is useful.

## Capability manifest example

~~~yaml
security:
  risk_tier: S2

capabilities:
  filesystem:
    read:
      - workspace/**
    write:
      - workspace/reports/**
  network:
    allowed_hosts:
      - api.github.com
  shell:
    allowed_commands:
      - git
      - rg
      - pytest

prohibited:
  - secret.read
  - system.modify
  - skill.modify
  - arbitrary_network
  - arbitrary_shell

human_approval:
  - git.push
  - external.publish
  - package.install
~~~

Admission should compare declared, required, and observed capabilities.
