---
name: plugin-eval
description: "Evaluate skills/plugins with portable file tools, optional CLI and controlled agent comparisons."
---

# Plugin Eval

A local `plugin-eval` executable, Codex path or lifecycle hook is **optional**. First inspect the actual host, repository, target `SKILL.md`, references, examples and available permissions.

## Workflow

1. Resolve the target by explicit path or repository search; do not assume `~/.codex/skills` exists.
2. Identify the intended behavior, likely risks, testable cases, baseline and evaluation budget.
3. If `plugin-eval` CLI exists and is authorized, inspect its `--help` and reuse its analyze/benchmark commands. Otherwise use ordinary file tools and any existing permitted evaluation runner. Do not install a new framework merely to analyze skill text.
4. Follow [the controlled comparison protocol](../agent-evals-lab/references/skill-comparison.md): baseline/current/candidate, same tools and model settings, isolated tasks, verified skill loading and held-out behavioral checks.
5. Report defects and smallest useful improvements. Keep failures and timeouts; separate structural validation from actual model behavior.

For evidence fields and states see [agent-test-contract](../agent-evals-lab/references/agent-test-contract.md). For trigger and portability design see [agent-skill-development](../agent-skill-development/SKILL.md). Unavailable CLI-only helper references are not required.

## Output

Return actionable findings, tested scenarios, actual run identifiers, missing evidence and the achieved level: specified / structurally validated / smoke-tested / behaviorally benchmarked. Never infer measured gains from a prose rewrite.
