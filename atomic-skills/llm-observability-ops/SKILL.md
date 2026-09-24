---
name: llm-observability-ops
description: This skill should be used when instrumenting, reviewing, or operating observability for LLM applications, especially traces, prompts, tool calls, retrieval spans, model comparisons, and release diagnostics across LangGraph, LangChain, Langfuse, or LangSmith integrations.
---

# LLM Observability Ops

## Overview

Instrument and operate LLM workflows so failures become diagnosable instead of anecdotal. Focus on trace completeness, metadata standards, prompt/model version visibility, privacy-safe logging, and release comparison workflows.

## When to use

- Add tracing to agent turns, retrieval, prompt packaging, or tool calls.
- Investigate why users received bad answers, empty responses, wrong tool behavior, or slow turns.
- Compare model versions, prompt revisions, or retrieval changes.
- Introduce Langfuse, LangSmith, or similar observability into `bot/graph/`, `bot/openrouter_utils.py`, or `bot/memory_system.py`.
- Build operator playbooks for AI runtime incidents.

## Core workflow

### 1. Define the trace model

- Capture at least: request id or thread id, user id surrogate, chat mode, language, intent, model id, latency, token usage, tool names, retrieval count, and outcome status.
- Decide which parts belong at span level versus run-level metadata.

### 2. Instrument the critical path

- Instrument entrypoint, prompt construction, retrieval, tool execution, model call, and persistence.
- Tag deterministic branches separately from general-agent turns.
- Record prompt version or config revision whenever prompts can change.

### 3. Preserve privacy

- Redact or hash PII/PHI before attaching attributes.
- Avoid sending raw health details, payment payloads, or secrets into third-party telemetry.
- Store enough context to debug behavior without leaking sensitive content.

### 4. Build an operator workflow

- Start from a failing run.
- Inspect branch selection, retrieval inputs, prompt payload, tool calls, and final answer.
- Compare against a known-good run.
- Decide whether the fault belongs to prompt design, retrieval quality, tool behavior, model choice, or orchestration.

### 5. Turn incidents into datasets

- Save representative bad runs as canary or regression examples.
- Group failures by class: hallucination, empty answer, unsafe answer, slow turn, wrong tool, wrong language, wrong intent.

## Standard metadata fields

- `thread_id`
- `session_id`
- `chat_mode`
- `language_code`
- `intent`
- `model`
- `tool_names`
- `retrieved_docs_count`
- `response_latency_ms`
- `token_usage`
- `release_version`

## Repository guidance

Prioritize these files:

- `bot/graph/entrypoint.py`
- `bot/graph/nodes.py`
- `bot/memory_system.py`
- `bot/openrouter_utils.py`
- `bot/openai_utils.py`
- `docs/Configuration.md`
- `docs/Troubleshooting.md`

## Non-negotiables

- Keep telemetry privacy-safe.
- Version prompts and models in trace metadata.
- Distinguish user-visible failure from internal error cause.
- Prefer structured metadata over free-form logging for AI runs.
- Convert recurring incidents into eval inputs.

## Deliverables

When using this skill, produce:

1. Instrumentation plan.
2. Metadata schema.
3. Privacy/redaction notes.
4. Operator triage workflow.
5. Regression capture plan.
