---
name: long-horizon-context-management
description: Use when designing, implementing, reviewing, debugging, or evaluating context management for long-running LLM agents and tool-using coding assistants. Applies a two-plane architecture: preserve lossless history for audit/recovery while building a bounded working context from structured task state, recent dialogue, typed tool observations, and recoverable references. Use for context-window optimization, task state, tool-result compaction, structured condense, rewind/resume safety, retention policies, overflow recovery, and token-efficiency rollout.
license: MIT
metadata:
  category: ai-engineering
  role: specialist
  scope: architecture-implementation-evaluation
  triggers: context management, context window, long horizon, task state, context compaction, context compression, tool output, condense, summarize history, token optimization, agent memory, rewind, resume, retention, prompt budget
  related-skills: agent-evals-lab, llm-observability-ops, langgraph-agent-runtime, prompt-engineer, debugging-wizard, test-master
  source:
    type: synthesized-research
    papers:
      - SKILL.state: Scalable Long-Horizon Agent Skills, arXiv:2608.26263
      - Scroll: Context as an Environment, arXiv:2608.21690
      - Context Window Lifecycle, arXiv:2606.11213
---

# Long-Horizon Context Management

## Purpose

Design agent context so long-running tasks remain correct, resumable, auditable, and token-efficient without making destructive summarization the source of truth.

The core rule is:

> Preserve lossless execution history separately from the bounded context shown to the model.

Treat context construction as a projection problem, not as deletion of history.

## When to use

Use this skill when:

- an agent approaches or exceeds provider context limits;
- raw tool outputs dominate cumulative input tokens;
- long tasks repeat reads, searches, commands, or reasoning because earlier facts are hard to recover;
- condensing or sliding-window truncation loses task intent or breaks resume/rewind;
- native `tool_use` / `tool_result` pairs must remain protocol-valid;
- you need a versioned task state for multi-turn or long-running workflows;
- you want to introduce context compaction behind feature flags or shadow mode;
- you need measurable token savings without degrading task success.

Do not use this skill as a substitute for retrieval design, durable application storage, or ordinary chat summarization when the task is short-lived.

## Core architecture: two planes

Maintain two independent planes.

### 1. Lossless plane

The lossless plane is the authoritative execution record.

It should contain, as applicable:

- full API/task conversation history;
- original user turns and explicit constraints;
- tool calls and raw tool results;
- native tool-call pairing identifiers;
- checkpoints, rewind markers, and resume metadata;
- persisted artifacts or stable references to them;
- enough provenance to reconstruct why the working state exists.

Properties:

- append-only or non-destructively persisted by default;
- optimized for audit, recovery, rewind, debugging, and re-projection;
- allowed to grow on disk;
- never assumed to fit into the model context.

### 2. Working-context plane

The working-context plane is the bounded projection sent to the model.

It should contain:

- versioned structured task state;
- current user intent and explicit constraints;
- latest relevant tool/user observation;
- recent dialogue needed for local coherence;
- compact references to evicted or replaced historical evidence;
- only the system/environment data needed for the next action.

Properties:

- bounded by explicit budgets;
- deterministic where possible;
- validated before use;
- reconstructable from the lossless plane plus durable environment state;
- safe to discard and rebuild.

Target shape:

```text
LOSSLESS PLANE
full API/task history
tool_use <-> tool_result
rewind / audit / recovery
        |
        | projections + stable addresses
        v
WORKING CONTEXT PLANE
bounded task state
+ current observation
+ recent dialogue
+ compact references
```

The steady-state goal is approximately bounded working context even while the lossless plane continues to grow.

## Non-negotiable invariants

### MUST preserve

- Original user intent and explicit constraints.
- Protocol-critical `tool_use` / `tool_result` pairs.
- Stable provenance from compact observations back to raw evidence.
- A full-history fallback path.
- Resume and rewind semantics.
- Provider-specific thinking/signature constraints.
- A versioned state schema and migration/fallback behavior.

### MUST NOT

- Destructively delete raw history during early rollout.
- Treat an LLM-generated summary as the only source of task truth.
- Infer old decisions or hypotheses silently when persisted state is missing.
- Hide a tool result unless its replacement is validated and recoverable.
- Let state-persistence failure block the primary task.
- Change context treatment for an existing session merely because a global flag changed.
- Emit raw user/tool content into telemetry when counts, hashes, ids, and classes are sufficient.
- Break native tool-pair integrity to save tokens.

## Workflow

### Phase 0 — measure before optimizing

Instrument the outgoing context before changing behavior.

Measure at least:

- system prompt;
- conversation history;
- environment/runtime details;
- raw tool results;
- structured task state;
- retrieved files/documents;
- estimated or exact input tokens.

Capture content-free metrics:

- total prompt tokens;
- p50/p95 prompt tokens per turn;
- cumulative input tokens per task;
- tool-result share of prompt;
- condense/truncation count;
- context-overflow failures;
- repeat tool-call rate;
- repeat unchanged-read rate.

Create a baseline eval set before compaction.

### Phase 1 — add bounded structured task state

Introduce a versioned runtime-validated state object.

Recommended logical fields:

```typescript
type TaskExecutionStateV1 = {
  version: 1
  revision: number

  originalGoal: string
  currentGoal: string

  todos: Array<{
    id: string
    content: string
    status: "pending" | "in_progress" | "completed"
  }>

  files: Array<{
    path: string
    status: "read" | "modified" | "created" | "deleted" | "referenced"
    note?: string
  }>

  decisions: string[]
  hypotheses: Array<{
    text: string
    status: "active" | "tested" | "rejected" | "confirmed"
    evidenceRefs?: string[]
  }>
  constraints: string[]
  pendingQuestions: string[]
  observations: string[]

  provenance: {
    createdAt: number
    updatedAt: number
    source: "runtime" | "model" | "migration"
  }
}
```

Rules:

- Define hard bounds for every string and collection.
- Keep `version`, `revision`, original goal, and provenance runtime-owned.
- Persist state separately from raw conversation history.
- Use deterministic runtime events to update fields whenever possible.
- Treat model-written state as a validated patch, not an unrestricted replacement.
- Render state into dynamic context, not the static system prompt, when prompt caching matters.
- If state is missing or corrupt, fall back safely rather than inventing state from old history.

### Phase 2 — controlled model state updates

If the model must update semantic state, expose a narrow state-update contract.

Preferred pattern:

- discriminated patch operations;
- optimistic `revision` check;
- schema validation;
- path/size/evidence validation;
- atomic apply;
- short success result;
- rollback on failure.

Do not require a state-update tool after every turn. Update only when information materially affects future actions.

### Phase 3 — normalize tool results into observations

Intercept tool results at the narrowest shared boundary before provider request assembly.

Create a normalized observation envelope such as:

```typescript
type ToolObservation = {
  observationId: string
  toolName: string
  toolUseId?: string
  occurredAt: number

  semanticClass:
    | "read"
    | "search"
    | "command"
    | "edit"
    | "browser"
    | "mcp"
    | "diagnostic"
    | "other"

  status: "success" | "error" | "denied" | "partial"
  paths: string[]
  command?: string

  rawContentHash: string
  rawTokenEstimate: number
  projectedTokenEstimate: number

  projection: unknown

  sourceRef: {
    messageId?: string
    blockIndex?: number
    artifactId?: string
  }

  retentionClass: "pinned" | "recent" | "replaceable" | "protected-pair"
}
```

Projection must be deterministic for MVP.

Examples:

- file read: path, ranges, content hash, read status;
- edit/write/delete: path, operation, success/failure, resulting hash when available;
- search: query, result count, bounded top paths;
- command: command, cwd, exit/active status, bounded diagnostic tail;
- diagnostics: counts, severity, paths;
- browser/MCP: metadata first; keep raw output until projector coverage is proven.

Projectors should extract reliable facts, not interpret code semantics.

### Phase 4 — classify retention

Classify context by semantic recoverability rather than age alone.

Use classes such as:

| Class | Meaning | Default action |
|---|---|---|
| `pinned` | User intent, explicit constraints, critical decisions | Keep |
| `protected-pair` | Provider/native tool protocol dependency | Keep atomically |
| `recent` | Needed for local dialogue/action coherence | Keep temporarily |
| `replaceable` | Durable/recoverable evidence already projected | Candidate for compaction |

Recommended eviction order:

1. repeated telemetry/progress noise;
2. superseded search/read results;
3. old successful command output whose durable result is known;
4. old deterministic tool evidence with validated projection;
5. narrative history already represented by structured state.

Evict user intent and unresolved reasoning last.

### Phase 5 — shadow planner before compaction

Before changing the outgoing payload, simulate compaction while still sending full legacy history.

For every candidate removal, record:

- observation id;
- source reference;
- retention class;
- raw tokens;
- projected tokens;
- expected savings;
- state revision that supersedes the raw evidence;
- whether protocol pairs remain valid;
- whether raw evidence remains recoverable.

Shadow mode must not alter model-visible history.

Do not enable destructive or hidden compaction until shadow data proves coverage and protocol safety.

### Phase 6 — assemble compact effective history

Build an effective history separately from persisted history.

A safe assembly algorithm:

```text
1. Load full persisted history.
2. Load and validate current task state.
3. Identify protected user turns and protocol-critical pairs.
4. Keep the newest coherence window.
5. Evaluate older observations by retention class.
6. Replace only validated + recoverable replaceable spans.
7. Insert compact observation/reference markers where useful.
8. Validate provider/tool protocol invariants.
9. Measure candidate prompt size.
10. If any invariant fails, send full history.
```

The operation is a view/projection. It must not mutate the lossless plane.

### Phase 7 — structured condense

Use structured condense only after deterministic projection is working.

A structured condense result should separate:

- task-state patch;
- short narrative context that cannot be represented structurally;
- evidence references;
- unresolved items.

Apply it transactionally:

1. request structured result;
2. parse;
3. validate schema;
4. validate evidence references;
5. apply patch to a copy of state;
6. build candidate effective history;
7. verify provider/tool-pair invariants;
8. verify token reduction;
9. atomically persist state/history metadata;
10. otherwise fall back to legacy condense.

Preferred provider strategy:

1. native structured output / JSON schema;
2. strict JSON parser;
3. at most one bounded repair attempt;
4. legacy summary fallback;
5. existing truncation/overflow fallback.

### Phase 8 — bounded overflow recovery

Context-overflow handling must be finite and observable.

Rules:

- cap recovery attempts;
- make each attempt strictly reduce estimated context size;
- preserve user intent and protocol pairs;
- fall back from compact view to a known-safe policy;
- never enter cascading condense/truncate loops;
- emit metrics for attempt count, before/after size, and chosen fallback.

## Session treatment lock

Context-management behavior should be stable for a session.

For experimental rollout:

- decide treatment at session creation;
- persist the treatment or infer it from a persisted versioned state marker;
- do not silently migrate an old session because a global feature flag changed;
- allow explicit migration as a separate operation;
- make disabling the experiment fall back to full lossless history without losing task continuity.

## Recoverability contract

A historical span is replaceable only if all are true:

1. A validated compact representation exists.
2. The compact representation has a stable id.
3. The source raw evidence has a stable persisted address.
4. The source can be reloaded without relying on model memory.
5. The current state revision records or implies that projection.
6. Removing the span does not split a protected protocol structure.
7. User intent or unresolved constraints are not lost.

If any condition is false, keep the span.

## Testing strategy

Use three layers.

### Canary

Small deterministic release blockers:

- flag-off payload equivalence;
- state schema validation;
- state size bounds;
- corrupt/missing state fallback;
- state revision conflict handling;
- native tool-pair integrity;
- resume/rewind treatment stability;
- content-free telemetry;
- stable source references for replaceable observations.

### Golden

Representative long-horizon tasks:

- multi-file refactor;
- debugging loop with large terminal output;
- repeated codebase search followed by edits;
- long task with repeated file reads;
- child/subtask delegation and parent resume;
- provider/model switch with thinking/tool-call constraints.

Track:

- task success;
- project tests;
- cumulative input tokens;
- p50/p95 prompt tokens;
- repeated tool/action rate;
- repeated unchanged reads;
- condense count;
- condense latency/cost;
- fallback rate;
- state-validation failure rate;
- resume/rewind correctness.

### Chaos

Adversarial and failure scenarios:

- huge terminal result;
- malformed persisted state;
- process killed during state write;
- tool output containing XML/JSON delimiter injection;
- provider context-overflow error;
- rewind across a condense boundary;
- duplicate native tool ids;
- missing raw observation source;
- stale file hash after external modification;
- experiment flag changes mid-session.

Every confirmed production context incident should become a regression case.

## Release gates

### Gate A — structured state

Require:

- schema and persistence tests;
- flag-off legacy payload equivalence;
- bounded state at p95;
- resume/rewind correctness;
- no raw content leakage into telemetry.

### Gate B — shadow projection

Require:

- at least 95% of successful supported tool results produce valid observations;
- zero tool-pair integrity violations;
- measurable projected token savings on long-horizon evals;
- all state/projection mismatches investigated before compact mode;
- every candidate replaceable span has a stable recovery address.

### Gate C — compact effective history

Require:

- task success stays within the agreed non-regression tolerance versus legacy;
- cumulative input tokens decrease materially, target at least 20%;
- full-history fallback works without task loss;
- zero critical resume/rewind regressions;
- no provider protocol regressions.

### Gate D — structured condense

Require:

- structured parse success at least 98% on supported models;
- fallback rate below 5%;
- quality no worse than legacy summarization;
- additional token reduction or a demonstrated reduction in repeated actions.

## Debugging workflow

When context behavior fails:

1. Reproduce with the smallest long-horizon scenario.
2. Compare lossless history with the effective history sent to the provider.
3. Locate the first missing or stale semantic fact.
4. Trace it to state, observation, retention class, and source reference.
5. Check whether the projector, planner, or assembler violated an invariant.
6. Verify tool-pair and provider-specific constraints.
7. Fix one layer at a time.
8. Add a regression test representing the failure.
9. Re-run both quality and token-efficiency evals.

Do not diagnose context regressions only from the final answer. Inspect the exact effective payload.

## Common failure modes

| Failure | Likely cause | Corrective action |
|---|---|---|
| Agent forgets original goal | Goal not pinned or state not loaded | Pin original intent; validate state load |
| Agent repeats file reads | Read observations not projected or invalidated incorrectly | Track hashes and supersession |
| Resume behaves differently | Session treatment not persisted | Add session-level treatment lock |
| Native provider rejects request | Tool pair split by compaction | Treat pair as atomic protected unit |
| State grows without bound | Schema has no collection/string limits | Add deterministic budgets and eviction |
| Summary invents decisions | Condense allowed free-form state reconstruction | Require evidence-backed structured patches |
| Token usage stays high | Raw tool results retained despite proven projection | Inspect retention planner and candidate coverage |
| Rewind loses context | Working state not tied to checkpoint/revision | Persist revision/checkpoint mapping |
| Overflow loops repeatedly | Recovery attempts do not monotonically reduce size | Add bounded monotonic recovery |
| Tests break after adding state API | Callers use partial/legacy task mocks | Feature-check optional integration surfaces or update shared test factory |

## Implementation principles

- Prefer one shared tool-result interception point over modifying every tool handler.
- Prefer deterministic projectors before LLM-based summarization.
- Prefer hashes, ids, counts, and stable references over raw content in telemetry.
- Keep large artifacts outside working state; store references plus bounded previews.
- Keep state schemas migration-friendly and provider-independent.
- Make compact history a pure transformation whenever possible.
- Add kill switches before enabling compaction.
- Optimize cumulative input tokens, not only the size of one prompt.
- Treat task correctness as the primary metric and token reduction as a constrained optimization objective.

## Deliverables when using this skill

Produce:

1. Context-source inventory and baseline composition report.
2. Two-plane architecture map.
3. Versioned bounded task-state schema.
4. Tool observation schema and deterministic projector plan.
5. Retention policy and recoverability rules.
6. Shadow compaction planner and token-savings metrics.
7. Effective-history assembly algorithm.
8. Structured-condense transaction and fallback design.
9. Canary, golden, and chaos eval plan.
10. Release gates, feature-flag plan, rollback path, and measured results.
