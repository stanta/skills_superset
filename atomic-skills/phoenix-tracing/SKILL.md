---
name: phoenix-tracing
description: Use when adding or debugging Arize Phoenix tracing for Python LLM, LangChain or LangGraph applications; instrument OpenInference/OTLP spans, correlate runs and protect trace payloads.
---

# Phoenix Tracing

Use alongside [LLM Observability Ops](../llm-observability-ops/SKILL.md); do not build another tracing stack.

## Workflow
1. Inventory existing tracers, LangSmith callbacks, OpenTelemetry providers, LLM transports, LangGraph checkpointers and loggers. Choose one owner for tracer-provider initialization; avoid double-instrumentation.
2. Define a trace rooted at each user operation, with child spans for graph nodes, LLM calls, tool/MCP calls, validation and persistence. Preserve parent context across workers; propagate standard W3C trace context where supported. Do not mistake a graph checkpoint for a trace.
3. Register a Phoenix OTLP exporter and OpenInference instrumentors supported by the installed SDK versions. Follow current official docs; never guess endpoint protocol or authentication. Local HTTP examples may use `http://localhost:6006/v1/traces` after validating the running Phoenix version.
4. Standardize safe span attributes: environment, application release, graph version, prompt version, model/provider, operation type, status, duration, tokens, retry attempt, tool name, and opaque request/run/group IDs. Link retries to the same operation without conflating attempts.
5. Disable raw prompts, completions, spreadsheets, credentials and tool arguments by default. Explicitly approve data classification, filtering, retention, RBAC and deployment destination before capture. Never attach API keys, cookies, Authorization headers or customer identifiers.
6. Use representative synthetic runs: success, tool failure, LLM retry, cancellation, replay and multi-turn session. Verify parent/child grouping, duplicate spans, service naming, exporter outage isolation and error outcomes.
7. Convert diagnosed defects into regression datasets and tests.

## Acceptance
- A trace can explain a user-visible result through graph, model and tool spans.
- Exporter failure does not fail the business request.
- Exactly one span per actual model attempt, not per UI refresh.
- Tracing does not change checkpoint execution or SQL transactions.
- All telemetry is privacy-reviewed and can be switched off.

## Sources
- https://arize.com/docs/phoenix/tracing
- https://arize.com/docs/phoenix/learn/tracing/how-tracing-works
- https://arize.com/docs/phoenix/tracing/integrations-tracing
