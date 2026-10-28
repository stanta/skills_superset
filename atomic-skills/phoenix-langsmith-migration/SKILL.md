---
name: phoenix-langsmith-migration
description: Use to assess or implement a safe LangSmith-to-Arize-Phoenix observability migration or parallel pilot for LangChain/LangGraph without rewriting application graph, checkpoints, or production business logic.
---

# LangSmith to Phoenix: Capability Migration

Move *workflows* (tracing, evals, datasets, prompt comparisons) before attempting data migration. Feature names do not imply 1:1 export/import compatibility.

## Checklist
1. Inventory LangSmith use: trace callbacks, projects, sessions, feedback, datasets, experiments, prompts, API keys, access controls, alerting and retention. Mark required, optional and unavailable Phoenix equivalents.
2. Keep application orchestration, LangGraph checkpoint persistence, retries and business state unchanged. Do not introduce a second graph, second LLM caller, or a new result database.
3. Pilot Phoenix as an OTLP receiver using OpenTelemetry/OpenInference. Use one tracer-provider configuration, explicit opt-in and a bounded synthetic workload. If parallel tracing is required, assess span duplication and load instead of enabling competing auto-instrumentations.
4. Define field mapping before migration: project, trace/span hierarchy, operation, time, model, token usage, latency, errors, feedback, dataset version and prompt version. Record fields with no verified target mapping rather than silently discarding them.
5. For historical data, verify official export APIs and destination ingestion contracts against installed versions. Export a small sample, validate schema, timestamps, references and redaction, then decide whether to migrate historical traces at all. OTLP live export alone does NOT migrate historical LangSmith records.
6. Recreate eval rubrics and dataset/experiment comparisons independently; confirm parity on fixed examples. Never assume LangSmith feedback and Phoenix annotations are semantically identical.
7. Compare privacy, authentication, network isolation, storage, backups, retention, operational cost and incident workflows; self-hosting does not automatically guarantee secure configuration.
8. Define rollback: disable Phoenix exporter, retain existing LangSmith instrumentation and preserve app behavior. Cut over only after explicit acceptance and monitoring gates.

## Decision
Prefer: (A) Phoenix only for new traces and reproducible experiments; (B) parallel pilot where operations require LangSmith continuity; (C) historical migration only when a justified requirement and proven mapping exist.

## Acceptance
- Coverage comparison and unsupported features documented.
- No lost trace correlation or duplicated LLM invocations.
- Reversible switch without changing agent behavior.
- Historical import claims backed by actual tested data, not assumptions.

## Sources
- https://arize.com/docs/phoenix/
- https://arize.com/docs/phoenix/tracing/integrations-tracing
- https://arize.com/docs/phoenix/learn/tracing/how-tracing-works
