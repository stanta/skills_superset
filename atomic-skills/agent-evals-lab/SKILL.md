---
name: agent-evals-lab
description: This skill should be used when designing, implementing, or operationalizing evaluation suites for LLM agents, RAG flows, tool-using assistants, multilingual prompts, and release regression gates, especially for health, nutrition, retrieval, or structured-output workflows.
---

# Agent Evals Lab

## Overview

Design evaluation suites that make AI behavior measurable before and after prompt, model, retrieval, or orchestration changes. Combine deterministic assertions, model-based scoring, and adversarial cases with explicit release thresholds.

## When to use

- Change prompts, models, retrieval logic, or graph routing.
- Add new health, meal, report, memory, or search behaviors.
- Build regression gates for multilingual output quality.
- Convert production incidents into repeatable eval cases.
- Compare candidate prompts or models before deployment.

## Core workflow

### 1. Classify the behavior under test

- Prompt-only response quality
- Tool correctness
- Retrieval grounding
- Health-safety behavior
- Multilingual consistency
- Structured JSON extraction

### 2. Build a layered dataset portfolio

- Create `canary` cases for release gating.
- Create `golden` cases for representative product quality.
- Create `chaos` or adversarial cases for malformed inputs, missing context, and hostile content.
- Tag each case by severity and business criticality.

### 3. Match metrics to the risk

- Use exact assertions for schemas, language selection, routing, tool names, and refusal behavior.
- Use semantic scoring for advice quality, groundedness, helpfulness, and report usefulness.
- Use human review for borderline safety or medical-language cases.

### 4. Define release thresholds

- Set stricter thresholds for P0 safety behavior than for style quality.
- Require zero tolerance for unauthorized tool use, unsafe medical overclaiming, or broken JSON in extractor flows.
- Allow calibrated tolerance only for stylistic variation.

### 5. Feed failures back into development

- Promote every confirmed production failure into a regression candidate.
- Version datasets alongside prompt and model changes.

## Recommended eval categories for this repository

- Meal logging correctness
- Health triage safety and non-diagnostic language
- Daily and weekly report usefulness
- Retrieval grounding and memory relevance
- Multilingual prompt consistency
- Payment-link/tool gating behavior
- Prompt injection resistance

## Repository guidance

Prioritize these files:

- `tests/test_graph_nodes_workflow.py`
- `tests/test_health_tools.py`
- `tests/test_memory_extractors.py`
- `tests/test_retrieval_pipeline.py`
- `tests/test_messaging_handlers.py`
- `config/chat_modes.yml`
- `bot/graph/nodes.py`
- `bot/memory_system.py`

## Non-negotiables

- Keep deterministic assertions for routing, schemas, and tool behavior.
- Separate canary, golden, and adversarial suites.
- Track prompt version, model version, and dataset version together.
- Avoid release decisions based on one anecdotal example.
- Treat health-safety regressions as release blockers.

## Deliverables

When using this skill, produce:

1. Eval plan.
2. Dataset schema.
3. Metrics and thresholds.
4. CI/release gate proposal.
5. Regression additions from current defects.
