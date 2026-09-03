---
name: langchain-agent-engineering
description: This skill should be used when designing, implementing, debugging, reviewing, or operating LangChain-based LLM applications and agents, especially model/provider setup, prompt templates, tools, structured outputs, middleware, context engineering, retrieval chains, callbacks, tracing, evaluations, and production reliability patterns that may run standalone or inside LangGraph nodes.
license: Complete terms in LICENSE.txt
metadata:
  category: ai-engineering
  source:
    type: synthesized-research
    repositories:
      - url: https://github.com/langchain-ai/langchain
        stars_verified: 144444
        forks_verified: 24045
      - url: https://github.com/langchain-ai/langgraph
        stars_verified: 39901
        forks_verified: 6708
      - url: https://github.com/langchain-ai/langsmith-cookbook
        stars_verified: 1036
        forks_verified: 185
      - url: https://github.com/vonzosten/awesome-LangGraph
        stars_verified: 1965
        forks_verified: 256
---

# LangChain Agent Engineering

## Purpose

Build LangChain applications as typed, observable, testable LLM subsystems. Use LangChain for provider integrations, chat models, prompt templates, tools, structured output, retrieval, middleware, context engineering, and tracing. Use LangGraph when orchestration needs durable state, explicit branches, resumability, interrupts, or multi-step control.

## When to use

- Add or review LangChain model calls, prompts, tools, chains, agents, retrievers, callbacks, or middleware.
- Design structured outputs for extraction, classification, reporting, validation summaries, or tool-facing contracts.
- Convert raw prompt logic into reusable prompt templates, model wrappers, output parsers, and testable components.
- Add retrieval, document loading, text splitting, embeddings, vector stores, reranking, or answer-grounding logic.
- Debug inconsistent outputs, schema failures, hallucinations, high token cost, high latency, poor tool use, or provider migration issues.
- Embed LangChain components inside LangGraph nodes or n8n-style agent workflows.

## Core workflow

### 1. Choose the right abstraction boundary

- Use a direct chat model call for single-turn deterministic transformations.
- Use structured output for extraction, classification, routing, and machine-consumed results.
- Use tools only when the model must choose among external capabilities.
- Use retrieval chains when answers require external knowledge.
- Use LangGraph for stateful orchestration, loops, branches, resumes, and human approval.
- Keep domain logic outside prompts when it can be deterministic code.

### 2. Define contracts before prompts

- Write input schema, output schema, failure schema, and retry policy before composing the prompt.
- Prefer Pydantic or JSON Schema for outputs consumed by code or downstream agents.
- Include confidence, evidence, missing-data flags, and assumptions when outputs drive decisions.
- Validate outputs after the model call and map validation errors to controlled retries or fallbacks.
- Do not parse critical behavior from free-form prose when a structured response can be enforced.

### 3. Engineer prompts as versioned assets

- Keep prompts concise, role-specific, and testable.
- Separate system policy, task, context, examples, output format, and refusal/fallback instructions.
- Avoid contradictory instructions and hidden dependencies on previous conversational text.
- Include only relevant context; pass summaries and references instead of full artifacts.
- Version prompt templates and record prompt version in traces.
- Test prompts on representative happy paths, edge cases, adversarial inputs, missing data, and multilingual inputs when applicable.

### 4. Use structured output by default for machine contracts

- Prefer provider-native structured output when the selected model supports it.
- Use tool-based structured output fallback when provider-native response format is unavailable.
- Keep schemas strict enough to catch errors but flexible enough to represent missing/unknown information.
- Never ask the model to invent required fields; include nullable fields and missing-data explanations.
- Validate schema instances before writing to databases, calling tools, or returning API responses.

### 5. Design tools as safe APIs

- Give each tool a narrow name, clear description, typed arguments, bounded outputs, and explicit side effects.
- Validate tool arguments before execution.
- Make write tools idempotent where possible.
- Split read and write tools; attach human approval to high-risk writes.
- Limit tool results before reinserting them into the model context.
- Return structured tool results with status, data, warnings, and error details.

### 6. Apply middleware for production controls

- Use middleware for dynamic model selection, context normalization, structured output injection, guardrails, rate limiting, retries, and redaction.
- Keep middleware deterministic and small.
- Record when middleware changes model, prompt, response format, context, or tool execution behavior.
- Do not hide business rules in middleware without tests and documentation.

### 7. Build retrieval as an evaluated subsystem

- Choose chunking based on document structure, not arbitrary defaults.
- Preserve metadata: source, section, date, tenant/project, file path, and version.
- Use hybrid retrieval and reranking for production-quality knowledge workflows when feasible.
- Bound retrieved context by relevance, diversity, and token budget.
- Require citations or evidence IDs in final outputs when retrieval drives the answer.
- Evaluate retrieval separately from generation using labeled questions and expected evidence.

### 8. Manage memory and context explicitly

- Distinguish session memory, long-term memory, retrieved knowledge, uploaded artifacts, and transient tool results.
- Compress long histories into durable summaries while preserving constraints, IDs, decisions, and unresolved questions.
- Avoid sending raw private data or large files into prompts.
- Define who can write memory, what is stored, when it expires, and how it is redacted.
- Keep memory retrieval auditable with source IDs and scores.

### 9. Add observability from the first production path

- Trace request ID, session/thread ID, user surrogate, model ID, prompt version, tool names, retrieval metadata, output schema version, latency, token usage, retry count, and outcome.
- Capture validation errors and fallback reasons as structured metadata.
- Redact secrets, credentials, raw personal data, and uploaded private content.
- Convert bad production runs into regression/evaluation cases.
- Compare model/provider changes against golden datasets before release.

### 10. Evaluate before release

- Define success metrics: exact match, schema validity, factuality, groundedness, tool correctness, latency, cost, safety, and user-visible quality.
- Create small deterministic unit tests for prompt formatting and schema validation.
- Create integration tests with fake tools and mocked providers for branch behavior.
- Create golden-case evals for important user tasks and known failure modes.
- Set release gates for schema-valid rate, groundedness, hallucination rate, tool-call precision, and cost/latency budgets.

## LangChain patterns to prefer

### Single model transformation

Use for summarization, normalization, classification, and explanation where no tools or retrieval are required.

Rules:
- Use typed input/output schemas.
- Keep temperature low for deterministic tasks.
- Add fallback for empty, unsafe, or invalid output.

### Structured extraction

Use for converting text, reports, chats, or uploaded document previews into machine-readable data.

Rules:
- Include nullable fields for unknown values.
- Require evidence snippets or source IDs.
- Reject invented values explicitly.

### Tool-using agent

Use when tool choice is dynamic and cannot be predetermined.

Rules:
- Keep the tool list small.
- Add argument validation and output limits.
- Add approval to write tools.
- Add tool-call evals.

### Retrieval-augmented generation

Use when responses must be grounded in external documents, analytics tables, prior cases, or knowledge bases.

Rules:
- Retrieve evidence before generation.
- Pass concise evidence with source IDs.
- Require answer citations or explicit missing-evidence response.
- Evaluate retrieval and answer separately.

### LangChain inside LangGraph

Use LangChain components inside LangGraph nodes when orchestration is stateful.

Rules:
- Keep each node contract narrow.
- Return normalized outputs to graph state.
- Do not let LangChain memory and LangGraph checkpointing conflict; define one source of truth for conversation state.

## Project-specific guidance for this workspace

- For creative validation, use LangChain to produce explanations, summaries, and recommendations from deterministic findings; do not let prompts override rule-engine status.
- For advertising analytics, keep full CSV/XLSX and large SQL outputs outside prompt context; pass DuckDB table names, schemas, row counts, bounded samples, and saved result paths.
- For n8n AI nodes, mirror LangChain contracts in node prompts: explicit input contract, bounded tool use, structured output shape, completeness checks, and safe user-facing errors.
- For Telegram or browser-extension flows, validate user inputs and file references before model calls and keep generated text separate from side-effect execution.

## Reliability checklist

- Model/provider configured explicitly with timeout, retry, token, and cost assumptions.
- Prompt template versioned and covered by formatting tests.
- Output schema validated and failure path defined.
- Tool list minimized and write tools protected.
- Retrieved context bounded and cited.
- Memory scope and retention documented.
- Observability metadata attached.
- Golden evals and regression cases updated.
- Privacy redaction applied before traces and prompts.

## Common failure modes and fixes

| Failure mode | Likely cause | Fix |
|---|---|---|
| Invalid JSON or schema failure | Free-form output or overly rigid schema | Use structured output strategy and controlled retry |
| Hallucinated field values | Required fields force invention | Allow nulls and require missing-data explanations |
| Wrong tool selected | Too many tools or vague tool descriptions | Narrow tool set and improve tool schemas |
| Tool output overwhelms context | Unbounded result payloads | Add limits, summaries, and storage references |
| Prompt regression after model switch | Model-specific behavior changed | Run golden evals before provider/model migration |
| Retrieval misses key evidence | Poor chunking or metadata filters | Tune chunking, hybrid retrieval, reranking, and eval set |
| High cost/latency | Oversized context or expensive model everywhere | Add context budget, caching, batching, and dynamic model selection |
| Un-debuggable failures | Missing trace metadata | Add structured spans, prompt versions, and validation events |

## Deliverables when using this skill

1. LangChain component map: models, prompts, tools, retrievers, parsers, middleware, and callbacks.
2. Input/output schema and validation plan.
3. Prompt and context-budget design.
4. Tool-safety and side-effect control plan.
5. Retrieval and memory strategy when relevant.
6. Observability metadata and privacy-redaction plan.
7. Evaluation suite and release-gate recommendations.
