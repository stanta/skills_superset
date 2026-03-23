---
name: langgraph-agent-runtime
description: This skill should be used when designing, debugging, or extending LangGraph-based agent workflows, especially state schemas, node contracts, routing branches, tool loops, checkpoint persistence, and runtime diagnosis in `bot/graph/`, `langgraph.json`, or related orchestration files.
---

# LangGraph Agent Runtime

## Overview

Manage LangGraph workflows safely in repositories that use graph-driven conversational execution. Focus on state discipline, deterministic branching, checkpoint continuity, tool-loop correctness, and traceable runtime behavior.

## When to use

- Add or change nodes, edges, or routing logic in `bot/graph/`.
- Debug wrong intent branches, repeated tool loops, empty AI replies, or state-loss bugs.
- Change checkpointing behavior, `thread_id` handling, or persistence fallbacks.
- Add new deterministic branches such as reports, health flows, or payment-related graph actions.
- Review LangGraph/LangChain integration before changing prompts, tool bindings, or memory packaging.

## Core workflow

### 1. Map the graph contract first

- Identify entrypoint, compiled app builder, state schema, node files, tool bindings, and persistence layer.
- Confirm whether the change affects general routing, deterministic branches, or the `agent ↔ tools` loop.
- Record which state keys are read, written, or assumed by each node.

### 2. Preserve state discipline

- Treat each node output as a partial state patch, not a full state rebuild.
- Keep `messages` reducer semantics intact.
- Return serializable, stable values in state keys that may be checkpointed.
- Keep `thread_id` aligned with `config.configurable.thread_id` whenever persistence matters.

### 3. Separate deterministic branches from general-agent turns

- Use explicit nodes for report generation, health triage, payment links, or similar high-control flows.
- Limit tool binding scope by intent whenever possible.
- Avoid routing sensitive or structured tasks through an unrestricted general tool loop.

### 4. Treat tool loops as high-risk

- Confirm stop conditions when models stop emitting tool calls.
- Ensure tool outputs are appended in the correct message order.
- Minimize tool set size for each branch.
- Guard against repeated identical tool invocations and empty tool-output cycles.

### 5. Verify checkpoint and fallback behavior

- Test both persistent and in-memory fallback checkpointers.
- Confirm process restart behavior when Mongo-backed persistence is unavailable.
- Validate state restoration across turns for the same user/thread.

### 6. Add traceability before deep refactors

- Attach metadata such as intent, chat mode, language, thread id, tool names, and branch source.
- Prefer small graph changes followed by tests over multi-branch rewrites.

## Repository guidance

Prioritize these files:

- `bot/graph/entrypoint.py`
- `bot/graph/workflow.py`
- `bot/graph/state.py`
- `bot/graph/nodes.py`
- `bot/graph/tools.py`
- `bot/memory_system.py`
- `langgraph.json`

## Non-negotiables

- Keep state keys stable unless all dependent nodes are updated together.
- Keep deterministic health/report/payment flows outside free-form agent behavior when possible.
- Avoid broad tool registration when only one or two tools are needed for an intent.
- Preserve per-user continuity for `thread_id`, `session_id`, and retrieved memory context.
- Add or update tests for branch selection, tool loops, and checkpoint behavior after graph changes.

## Deliverables

When using this skill, produce:

1. Graph change summary.
2. State-impact summary.
3. Routing or tool-loop risk notes.
4. Required test updates.
5. Rollback plan for orchestration regressions.
