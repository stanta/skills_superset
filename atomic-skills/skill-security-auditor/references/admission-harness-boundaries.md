# Harness Boundaries

Prompt text is not a sufficient security boundary. Enforce sensitive permissions outside the model.

## Permission broker pattern

Agent -> Permission Broker -> Policy Engine -> Tool

The broker should evaluate at least:
- skill identity/version;
- requested action;
- resource;
- arguments;
- user intent/approval state;
- environment;
- risk tier.

## Default-deny capabilities

Unless explicitly required:
- secret.read
- arbitrary_shell
- arbitrary_network
- system.modify
- skill.modify
- policy.modify
- credential.use
- production.write
- payment.execute
- external.publish
- package.install
- persistence.create

## Filesystem

Prefer explicit workspace roots. Deny sensitive paths such as:
- ~/.ssh/**
- ~/.aws/**
- ~/.config/gcloud/**
- ~/.kube/**
- ~/.gnupg/**
- browser profiles/cookies
- credential stores
- /etc/**
- Docker/Podman sockets
- host process/procfs surfaces not required for the task

## Network

Default deny. Allowlist exact hosts/services where practical. Block:
- metadata endpoints such as 169.254.169.254;
- localhost/internal networks unless required;
- raw arbitrary outbound sockets;
- DNS exfiltration paths where enforceable.

## Human approval

Require explicit approval before:
- publishing/sending content externally;
- git push/merge/release;
- package installation with executable hooks;
- infrastructure or production mutations;
- financial/admin actions;
- deleting or overwriting high-value data.

Approval must bind to the concrete action and arguments, not be a blanket session-wide grant.

## Audit

Record:
- skill and version;
- requested tool/action;
- normalized arguments;
- decision;
- approval context;
- side-effect result;
- network/filesystem/process events for high-risk runs.

A skill must not be able to disable or rewrite these logs.
