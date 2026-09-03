---
name: langgraph-agent-runtime
description: This skill should be used when designing, implementing, debugging, reviewing, or operating LangGraph-based agent workflows, especially state schemas, reducers, node contracts, conditional routing, tool loops, checkpoint persistence, streaming, human-in-the-loop interrupts, recursion limits, and production diagnostics for Python or TypeScript agent runtimes.
license: Complete terms in LICENSE.txt
metadata:
  category: ai-engineering
  source:
    type: synthesized-research
    repositories:
      - url: https://github.com/langchain-ai/langgraph
        stars_verified: 39901
        forks_verified: 6708
      - url: https://github.com/langchain-ai/langgraphjs
        stars_verified: 3212
        forks_verified: 550
      - url: https://github.com/langchain-ai/langgraph-101
        stars_verified: 575
        forks_verified: 142
      - url: https://github.com/langchain-ai/langgraph-example
        stars_verified: 519
        forks_verified: 357
      - url: https://github.com/vonzosten/awesome-LangGraph
        stars_verified: 1965
        forks_verified: 256
---

# LangGraph Agent Runtime

## Purpose

Design and operate LangGraph workflows as reliable state machines rather than loose prompt chains. Apply this skill to make graph execution explicit, restartable, testable, observable, and safe for tool-using agents.

Use LangGraph for controllable agent orchestration: durable execution, explicit state transitions, multi-step workflows, tool loops, human approvals, streaming, and long-running tasks. Use LangChain components inside nodes for models, prompts, tools, structured output, retrieval, and provider integrations.

## When to use

- Add, refactor, or review graph nodes, edges, conditional branches, or compiled app builders.
- Design graph state, reducers, checkpoint persistence, thread/session identity, or memory scope.
- Debug wrong routes, state loss, repeated tool loops, empty responses, recursion-limit errors, or resumed-run failures.
- Add human approval before high-risk tools, edits, external calls, payments, SQL writes, or file writes.
- Build multi-agent graphs, evaluator loops, fan-out/fan-in review flows, or deterministic branches for reports and validations.
- Prepare LangGraph workflows for production observability, regression tests, or release gates.

## Core operating model

### 1. Map the graph contract before editing

- Identify entrypoint, compiled graph builder, state schema, all nodes, all edges, conditional routers, tool bindings, checkpointer, store, and streaming mode.
- Draw the intended graph as a compact state-transition map before changing implementation.
- Classify each node as deterministic transformation, model call, tool call, router, evaluator, human-interrupt, persistence operation, or finalizer.
- Record every state key read and written by every node.
- Preserve downstream state contracts unless all consumers are updated together.

### 2. Treat state as the product API

- Define stable state keys with typed schemas and explicit ownership.
- Return partial state patches from nodes; do not rebuild unrelated state.
- Use append-style reducers for message history where conversation continuity matters.
- Keep checkpointed values serializable, deterministic, and migration-friendly.
- Separate durable state from ephemeral execution scratch fields.
- Store large artifacts outside the graph state and pass references, IDs, summaries, and bounded samples.

### 3. Design reducers deliberately

- Use append reducers for message lists and event ledgers.
- Use overwrite semantics only for fields with a single owner.
- Use merge reducers for dictionaries only when field-level conflict rules are explicit.
- Avoid letting multiple branches write the same scalar key without a merge policy.
- Add regression tests for reducer behavior when parallel branches or retries are introduced.

### 4. Keep routing deterministic where possible

- Prefer explicit router nodes for intent, validation status, completeness gates, and safety gates.
- Make route return values enumerable and map every value to a target node.
- Add fallback routes for unknown, low-confidence, malformed, or unsupported states.
- Keep sensitive workflows outside unrestricted general-agent paths.
- Log route inputs, route outputs, confidence signals, and fallback reasons.

### 5. Treat tool loops as high risk

- Bind the smallest viable tool set for each branch.
- Define stop conditions: no tool call, final structured answer, maximum loop count, repeated tool-call detector, timeout, or human escalation.
- Validate tool arguments before execution and validate tool outputs before reinserting into state.
- Avoid passing raw tool output directly to downstream nodes when a compact normalized result is sufficient.
- Interrupt before high-risk tools when side effects are irreversible or costly.

### 6. Use checkpointing intentionally

- Require a stable thread or session identifier whenever graph state must resume across turns.
- Use in-memory checkpointers only for local development, tests, and ephemeral MVP flows.
- Use persistent checkpointers for production conversations, interrupts, long-running tasks, retries, and resumable tool approvals.
- Version checkpointed state schemas and define migration behavior before changing durable keys.
- Test restart, resume, interrupt, and duplicate-request scenarios.

### 7. Add human-in-the-loop at decision boundaries

- Interrupt before tools that write, delete, purchase, publish, notify, mutate databases, or expose private data.
- Show the human a concise action request, arguments, evidence summary, and risk classification.
- Support approve/reject/edit/respond paths only where each path has tested behavior.
- Resume from checkpoint after approval instead of re-running prior model calls blindly.

### 8. Control context growth

- Pass structured summaries between nodes instead of full prior transcripts.
- Keep full documents, CSVs, screenshots, and long traces in storage; pass handles and sampled previews.
- Include invariant context fields: task, constraints, current state, accepted facts, rejected assumptions, and next required action.
- Compress multi-agent outputs into role-specific summaries before fan-in synthesis.
- Add context budget checks around large memory, retrieval, and tool-result spans.

### 9. Stream for UX and diagnostics

- Choose stream mode based on consumer needs: values for state snapshots, updates for node-level patches, messages for token-level UI, events for diagnostics.
- Never assume streamed partial text equals final state.
- Persist final state separately from UI stream fragments.
- Attach node names and run identifiers to streamed events for debugging.

### 10. Instrument every production graph

- Trace graph run ID, thread ID, node name, route decision, model ID, tool name, latency, token usage, retry count, recursion count, checkpoint ID, and final outcome.
- Redact secrets, credentials, raw personal data, and sensitive uploaded content from traces.
- Convert recurring incidents into eval cases.
- Keep prompt versions, tool versions, graph version, and state schema version visible in traces.

## Recommended graph patterns

### Deterministic pipeline

Use for validation, reporting, extract-transform-summarize, and approval workflows where the steps are known.

Rules:
- Give each step a narrow node contract.
- Validate state after each transformation.
- Use final guardrail and schema validation nodes before returning a user-visible answer.

### Router plus specialized branches

Use when inputs require different handling paths.

Rules:
- Keep routing criteria explicit.
- Avoid routing sensitive work through the broadest agent.
- Add low-confidence fallback to clarification or human review.

### Agent-tool loop

Use when an agent must decide which read-only tools to call.

Rules:
- Bind only branch-specific tools.
- Add maximum loops and repeated-call detection.
- Normalize tool results into compact state before final answer generation.

### Evaluator-optimizer loop

Use when output quality can be scored.

Rules:
- Cap iterations, normally at three.
- Make evaluator output structured: score, failed criteria, evidence, and required fix.
- Exit when score plateaus or required evidence is missing.

### Parallel fan-out/fan-in

Use for independent expert reviews or multi-source retrieval.

Rules:
- Avoid shared mutable state in fan-out branches.
- Define merge strategy before implementation: union, vote, ranking, weighted confidence, or human arbitration.
- Handle partial branch failures explicitly.

### Hierarchical multi-agent orchestration

Use for dynamic decomposition.

Rules:
- Keep the orchestrator responsible for planning, delegation, ledger maintenance, contradiction detection, and synthesis.
- Keep subagents responsible for narrow scoped outputs only.
- Pass structured outputs and summaries, not raw transcripts.

## Project-specific guidance for this workspace

- For creative validation backend work, keep deterministic status calculation before the LangGraph summarization graph; the graph may explain and recommend but must not silently change validation status.
- For advertising analytics and n8n-adjacent workflows, keep large CSV/XLSX data out of LLM context; pass DuckDB table names, row counts, column metadata, bounded samples, and storage paths.
- When using MCP or database tools, enforce read/write boundaries and bounded output limits before tool results enter graph state.
- Prefer graph nodes that produce auditable intermediate artifacts: normalized findings, risk context, per-file summaries, overall summary, recommendations, and guardrail output.

## Implementation checklist

- Define the state schema and reducers before adding nodes.
- Document node inputs, outputs, side effects, retry policy, and failure behavior.
- Add route maps for every conditional edge.
- Add loop caps and recursion limits for every cyclic path.
- Add checkpoint configuration and thread/session identity rules.
- Add interrupts for high-risk side effects.
- Add schema validation on all user-visible structured outputs.
- Add observability metadata and privacy redaction.
- Add unit tests for nodes, router tests for branches, integration tests for full graph runs, and restart/resume tests when checkpointing is used.

## Common failure modes and fixes

| Failure mode | Likely cause | Fix |
|---|---|---|
| State key disappears | Node returned a full replacement or wrong patch | Return only intended patch and test state merge behavior |
| Message history overwritten | Missing append reducer | Add append reducer and regression test |
| Wrong branch selected | Router prompt or deterministic criteria ambiguous | Make route values enumerable and log evidence |
| Infinite tool loop | No stop condition or repeated call detector | Add max iterations, repeated-call guard, and fallback |
| Resume fails | Missing stable thread ID or incompatible checkpoint schema | Persist thread identity and version durable state |
| Duplicate side effect | Retry re-executed non-idempotent tool | Add idempotency keys and interrupt before execution |
| Context overflow | Raw documents/tool outputs carried in state | Store artifacts externally and pass handles/summaries |
| Untraceable bad answer | Missing per-node metadata | Add node spans, prompt versions, and output validation |

## Deliverables when using this skill

1. Graph map and node inventory.
2. State schema and reducer impact summary.
3. Routing, loop, checkpoint, and interrupt design.
4. Tool-safety and context-budget controls.
5. Observability and privacy metadata plan.
6. Test plan covering node, route, loop, restart, and failure cases.
7. Rollback plan for orchestration regressions.
