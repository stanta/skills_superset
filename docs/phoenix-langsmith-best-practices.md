# Phoenix observability, evals and LangSmith transition

Research date: 2026-10-28. Scope: reusable skills; no application deployment or data migration.

## Findings
Phoenix is an open-source observability/evaluation platform with OpenTelemetry and OpenInference integrations, tracing, datasets, experiments, prompts and evaluation. It supports self-hosting. Its official quickstart recommends the loop tracing → evals → datasets/prompts → experiments.

LangSmith migration is **not** assumed to be a native one-click import. Evaluate semantic parity per data type and validate APIs against the exact installed versions. New-trace OTLP instrumentation is distinct from a historical-data importer.

## Minimal recommended architecture
Application (existing LangGraph, LLM clients, MCP, PostgreSQL checkpoints) → one OpenTelemetry/OpenInference instrumentation layer → configured OTLP destination → Phoenix. Business-result persistence stays in the application. Evaluate representative sanitized traces using deterministic assertions first and calibrated model judges second.

## Implementation order
1. Audit current observability, access and privacy boundaries.
2. Pilot a synthetic trace across graph, LLM, tools and persistence.
3. Add reusable versioned eval datasets and baseline-versus-candidate experiments.
4. Pilot alongside LangSmith only if required, measure overhead and duplicates.
5. Decide whether historical trace migration is required; run schema-and-redaction validation on a small sample.
6. Adopt gated rollout with documented rollback.

## Skills
- [phoenix-tracing](../atomic-skills/phoenix-tracing/SKILL.md)
- [phoenix-evals-experiments](../atomic-skills/phoenix-evals-experiments/SKILL.md)
- [phoenix-langsmith-migration](../atomic-skills/phoenix-langsmith-migration/SKILL.md)

Complement rather than duplicate existing [llm-observability-ops](../atomic-skills/llm-observability-ops/SKILL.md), [agent-evals-lab](../atomic-skills/agent-evals-lab/SKILL.md), and [agent-skill-development](../atomic-skills/agent-skill-development/SKILL.md).

## Sources
- https://arize.com/docs/phoenix/
- https://arize.com/docs/phoenix/quickstart
- https://arize.com/docs/phoenix/tracing
- https://arize.com/docs/phoenix/evaluation/llm-evals/evaluator-traces
- https://arize.com/docs/phoenix/learn/datasets-and-experiments/datasets-concepts

## Verification status
Skill content prepared from official docs and repository conventions. No application-side integration, SDK smoke test, live traces, exported LangSmith data or behavioral A/B skill trials were performed.
