---
name: agent-architecture-evolver
description: "Experimentally search bounded LLM module architectures with frozen evaluators, isolated execution and optional DSPy Flex plus GEPA; never mutate production authority or self-deploy."
license: MIT
---

# Agent Architecture Evolver

Evaluate code-level changes to an AI module's structure as controlled offline experiments. This is not permission for an agent to rewrite its own operating rules or production controls.

## When to use

Use only after a measurable baseline exists and prompt/demo optimization cannot address the observed structural limitation. For ordinary simplification use [design-minimal-architecture](../design-minimal-architecture/SKILL.md). Treat Flex-backed search as experimental and version-sensitive.

## Inputs

Require the module contract, baseline source, allowed edit surface, immutable evaluator/tests, dependency/tool allowlist, train/validation splits, hard resource limits and separate release authority.

## Procedure

1. Freeze the task interface, evaluator, test data, safety rules and permission boundaries. Define which internal calls, branches or aggregation logic may change.
2. Establish a minimal baseline and explicit hypotheses. Penalize unnecessary stages and cost only after correctness and safety gates pass.
3. Prepare an isolated execution environment with restricted filesystem/network, no production credentials, time/memory limits and allowlisted tool wrappers. Without this boundary, stop code execution and return reviewed design proposals only.
4. Generate a small bounded candidate set. Validate syntax, imports, interface compatibility and prohibited changes before running task cases.
5. Evaluate candidates on train/validation with the same immutable checks. Count syntax errors, runtime failures, timeouts and unsafe attempts as failures rather than removing them.
6. Review code diffs and ablate added stages. Use a held-out comparison only after selection; reject reward hacking, evaluator changes and unjustified complexity.
7. Export the candidate source, tests and dependency manifest as a reviewable artifact. Require independent review and normal regression/release authorization; retain the original implementation.

## Deliverable and acceptance

Return bounded experiment settings, candidate diffs, quality/cost comparison, rejected mutations, sandbox evidence and an accept/reject/inconclusive recommendation. A generated architecture is untrusted code even when its score is high.

## Safety

Never grant production credentials, edit approval/authorization controls or auto-deploy from the search loop. A local subprocess is not automatically a sandbox. Do not import new dependencies or extend tool access just because a candidate requests them.

Read [Flex integration and protected surfaces](references/playbook.md) and [evaluation cases](evals/cases.json). Handoff to [ai-regression-gate](../ai-regression-gate/SKILL.md).
