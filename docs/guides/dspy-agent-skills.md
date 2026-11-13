# DSPy-derived Agent Skills

These 12 reusable skills are original, agent-portable workflows informed by [DSPy](https://dspy.ai/), not official DSPy exports.

The repository preserves two-level discovery: start in `skills/meta-*/SKILL.md`, search `references/members.md`, and then read the chosen full `atomic-skills/<id>/SKILL.md`. Never treat a brief catalog entry as the instructions.

## Skill map

| Skill | DSPy mechanism | Meta-skills |
| --- | --- | --- |
| [task-contract-designer](../../atomic-skills/task-contract-designer/SKILL.md) | Signature, InputField, OutputField | meta-agent-systems, meta-software-architecture |
| [llm-eval-engineer](../../atomic-skills/llm-eval-engineer/SKILL.md) | Example, Evaluate | meta-machine-learning, meta-testing-quality |
| [prompt-optimizer](../../atomic-skills/prompt-optimizer/SKILL.md) | GEPA, MIPROv2 | meta-agent-systems, meta-machine-learning |
| [few-shot-learning](../../atomic-skills/few-shot-learning/SKILL.md) | LabeledFewShot, BootstrapFewShot | meta-agent-systems, meta-machine-learning |
| [self-refinement](../../atomic-skills/self-refinement/SKILL.md) | BestOfN, Refine | meta-agent-systems, meta-testing-quality |
| [long-context-research](../../atomic-skills/long-context-research/SKILL.md) | RLM | meta-agent-systems, meta-research-knowledge |
| [rag-optimizer](../../atomic-skills/rag-optimizer/SKILL.md) | Module composition, Evaluate, GEPA | meta-agent-systems, meta-machine-learning |
| [tool-use-optimizer](../../atomic-skills/tool-use-optimizer/SKILL.md) | ReAct, Tool, MCP | meta-agent-systems, meta-testing-quality |
| [multi-step-reasoning](../../atomic-skills/multi-step-reasoning/SKILL.md) | Module, Predict, ChainOfThought | meta-agent-systems, meta-software-architecture |
| [model-cost-optimizer](../../atomic-skills/model-cost-optimizer/SKILL.md) | LM, Evaluate, Optimizers | meta-agent-systems, meta-machine-learning |
| [agent-architecture-evolver](../../atomic-skills/agent-architecture-evolver/SKILL.md) | Flex, GEPA | meta-agent-systems, meta-software-architecture |
| [ai-regression-gate](../../atomic-skills/ai-regression-gate/SKILL.md) | Evaluate, versioned artifacts | meta-devops-cloud, meta-testing-quality |

## Recommended workflow

1. **Define a contract** with `task-contract-designer` and measurable validators.
2. **Establish the baseline** with `llm-eval-engineer`, preserve train/validation/test isolation.
3. **Pick a targeted intervention**: `few-shot-learning`, `prompt-optimizer`, `rag-optimizer`, `tool-use-optimizer`, `self-refinement` or `long-context-research`.
4. **Measure against the baseline** including failed calls, token costs and latency.
5. **Gate independently** using `ai-regression-gate`. For uncertain architecture changes use `agent-architecture-evolver` only in isolation.

## Trust and deployment boundary

DSPy optimization is not an authorization system. Keep secrets, tool scopes, destructive actions, medical and security policy, CI release approvals and human decisions outside optimization. Retrieved documents and model output are untrusted. The repository's meta-skills only route to atomic skills; they do not require runtime scripts, plugins or MCP.

## Evidence

Each atomic package includes an evaluation specification with four behavioral scenarios. These are **unrun test cases**, not claims of improved model accuracy. API compatibility and measured performance must be verified per pinned DSPy version.
