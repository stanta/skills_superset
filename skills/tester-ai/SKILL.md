---
name: tester-ai
description: This skill should be used when the task is to design, audit, or operationalize testing for AI applications such as chatbots, RAG systems, tool-using agents, autonomous loops, or multi-agent workflows, including evals, red-teaming, regression strategy, and production quality governance.
---

# Tester AI

## Overview

Design risk-based test strategies for AI applications by combining classical QA layers with LLM-specific evals, adversarial testing, and production observability. Use this skill to convert vague quality concerns into concrete suites, metrics, CI gates, and regression assets that are suitable for probabilistic systems.

## When to use

Use this skill when the request involves any of the following:

- Designing a test strategy for an LLM application, AI assistant, RAG workflow, or agent platform.
- Creating eval datasets, canary suites, golden regression sets, chaos sets, or red-team suites.
- Auditing an AI system for prompt injection, tool misuse, data leakage, memory safety, or model drift.
- Defining quality metrics such as task success, tool correctness, attack success rate, judge score, latency, or cost.
- Translating incidents from production traces into reproducible regression tests.
- Building CI/CD quality gates for prompt changes, model upgrades, guardrail updates, or tool integrations.
- Reviewing whether brittle end-to-end AI tests should be replaced with cheaper unit, contract, subcutaneous, or integration checks.

Do not use this skill for generic model experimentation without a quality objective, or for pure application feature development unrelated to verification.

## Core workflow

Follow this sequence unless the user explicitly requests only one subsection.

### 1. Classify the AI system under test

Identify the operating model before recommending tests:

- Chat assistant with no tools.
- RAG application with retrieval, reranking, and grounded answering.
- Tool-using agent with function calling, MCP tools, APIs, or browser actions.
- Autonomous or long-horizon agent with planning loops.
- Multi-agent system with role coordination and message passing.

State explicitly which qualities matter most: correctness, safety, reliability, privacy, explainability, latency, cost, or compliance.

### 2. Build a risk map before proposing tests

Anchor the strategy to failure modes, not to tools alone.

Minimum risk categories:

- Wrong answer or task failure.
- Hallucination or unsupported claims.
- Prompt injection, including indirect injection via retrieved or tool-returned content.
- Secret leakage or memory leakage.
- Unsafe or unauthorized tool execution.
- Failure to stop, excessive agency, or runaway loops.
- Model drift after provider or prompt changes.
- Excessive latency or cost.

For each risk, define:

- Severity.
- Trigger surface.
- Detection method.
- Preventive test layer.
- Release gate threshold.

### 3. Design the portfolio using an AI-adapted pyramid

Default to the lowest test level that can provide confidence.

Recommended effort distribution for AI applications:

- 60-70% fast unit, schema, policy, and contract checks.
- 20-30% integration tests across model, tools, memory, and orchestration.
- 5-10% end-to-end scenarios in realistic environments.
- Separate adversarial and red-team track on release cadence, nightly cadence, or both.

Apply the same logic as the classical test pyramid and testing trophy, but insert an eval layer:

- Prefer deterministic checks for parsers, schemas, routing, prompt contracts, and guardrail behavior.
- Prefer integration tests for tool calling, retrieval, memory updates, retries, and error recovery.
- Keep end-to-end suites thin and focused on critical user journeys.
- Replace brittle end-to-end coverage with subcutaneous or contract-style checks wherever UI or multi-service wiring is not the primary risk.

### 4. Define datasets and regression assets

Create at least three reusable datasets:

- Golden set: representative product scenarios and previously failed real cases.
- Canary set: small P0/P1 release gate scenarios.
- Chaos set: malformed inputs, tool failures, partial data, and hostile content.

For agentic systems, each test case should capture both final outcome and allowed trajectory:

- User goal.
- Initial system constraints.
- Available tools.
- Memory or context preconditions.
- Allowed and forbidden actions.
- Expected final behavior.
- Metrics and pass rule.
- Number of reruns for stochastic aggregation.

### 5. Choose scoring methods deliberately

Combine three scoring classes:

- Strict assertions for schema validity, invariants, safety flags, and exact tool behavior.
- Model-based judging for semantic quality, groundedness, helpfulness, or refusal quality.
- Human review for high-risk, ambiguous, or business-critical cases.

Never rely on LLM-as-a-judge as the only signal for a release gate.

### 6. Define operational policy

Specify:

- Flakiness policy for stochastic failures.
- Retry policy with explicit cap.
- Quarantine process for unstable cases.
- Ownership and SLA for broken tests.
- Drift-monitoring cadence after model or prompt changes.
- Incident-to-regression workflow from production traces.

## Task playbooks

### Design a test strategy

When asked for a strategy, produce these sections in order:

1. System classification and risk profile.
2. Test portfolio split by level.
3. Required datasets and fixtures.
4. Metrics and thresholds.
5. CI/CD cadence.
6. Governance, ownership, and evidence.

Include concrete examples such as:

- Unit test for structured JSON output.
- Contract test for a tool schema.
- Integration test for tool timeout fallback.
- End-to-end test for a critical user journey.
- Red-team case for indirect prompt injection.

### Create evals or regression suites

When asked to create evals, do the following:

1. Convert acceptance criteria into measurable behaviors.
2. Separate deterministic assertions from probabilistic quality checks.
3. Define dataset fields and scoring rules.
4. Set pass thresholds and rerun counts.
5. Mark each case by priority: P0, P1, or P2.

Prefer data structures that can be executed repeatedly and versioned alongside prompts, model versions, and tool definitions.

### Audit safety and red-team posture

Always include at least these attack classes for tool-enabled AI systems:

- Direct prompt injection.
- Indirect prompt injection through retrieved or tool-returned content.
- Secret or system prompt extraction.
- Unauthorized action requests.
- Model denial-of-service or excessive token spend.
- Tool selection manipulation.
- Memory poisoning or long-session drift.

For each class, define expected safe behavior, not only the malicious input.

### Review a flaky AI test suite

Treat flakiness as an engineering defect, not as a property to accept.

Inspect for:

- Uncontrolled model randomness.
- Non-versioned prompts or tools.
- Shared state between tests.
- Unstable external APIs.
- Missing tool mocks or unhermetic datasets.
- Semantic scoring that is too vague.
- Assertions on wording instead of invariant behavior.

Recommend quarantine plus root-cause elimination, not indefinite reruns.

## Non-negotiables

- Prefer risk-based testing over checklist theater.
- Push tests downward whenever confidence can be preserved.
- Keep a thin set of realistic end-to-end tests for critical journeys.
- Require explicit thresholds for P0 safety behaviors.
- Track model version, prompt version, tool version, and dataset version for every significant evaluation.
- Convert every confirmed production incident into a regression candidate.

## Output expectations

When using this skill, structure the result with clear headers and concrete deliverables.

Preferred output sections:

1. System under test.
2. Risks and assumptions.
3. Test portfolio.
4. Detailed suite design.
5. Metrics and thresholds.
6. CI/CD and cadence.
7. Governance and flakiness policy.
8. Example test cases.

## Reference files

Load [`references/api_reference.md`](references/api_reference.md) when a detailed playbook, metric catalog, or adversarial checklist is needed.

## Resources

### references/
Use the bundled reference document as the detailed source for:

- Test portfolio ratios.
- AI-specific risk taxonomy.
- Metric catalog.
- Golden/canary/chaos dataset design.
- Flakiness policy.
- Sample agent test cases.

---
