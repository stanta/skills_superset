---
name: llm-context-compressor
description: This skill should be used when compressing, summarizing, pruning, budgeting, or restructuring long LLM context for chat histories, agent traces, tool outputs, RAG evidence, codebase snippets, logs, or multi-agent handoffs while preserving task-critical facts, citations, constraints, and recoverability.
license: Complete terms in LICENSE.txt
metadata:
  category: ai-engineering
  source:
    type: synthesized-research
    references:
      - https://github.com/microsoft/LLMLingua
      - https://github.com/liyucheng09/Selective_Context
      - https://github.com/carriex/recomp
      - https://github.com/chopratejas/headroom
      - https://github.com/rohitg00/agentmemory
      - https://github.com/FMInference/H2O
      - https://github.com/mit-han-lab/streaming-llm
      - https://github.com/NVIDIA/kvpress
---

# LLM Context Compressor

Compress long or noisy context into an evidence-dense working context that stays within a token budget while preserving instructions, user intent, unresolved decisions, constraints, provenance, and retrieval hooks for omitted details.

## Use When

Use this skill when any of the following appear:

- Context exceeds or risks exceeding the model window.
- Long chat history must be compacted without losing commitments or decisions.
- Tool outputs, logs, JSON, API responses, RAG chunks, web pages, or code snippets are too large.
- A handoff summary is needed for another agent, mode, workflow, or session.
- A prompt must be compressed to reduce cost or latency.
- Retrieved documents need selective augmentation before answer generation.
- The task requires deciding what to keep, summarize, externalize, retrieve later, or drop.

Do not use this skill as a substitute for factual verification. If compression may change meaning, preserve the original artifact path, URL, execution ID, or quote handle.

## Core Principles

1. Preserve hierarchy of importance: system/developer instructions, user goals, hard constraints, active task state, evidence, then background.
2. Separate prompt components before compression: instructions and questions are high sensitivity; documents, examples, logs, and repeated history are lower sensitivity.
3. Compress by purpose, not by length alone. Keep information that answers the active question, constrains the solution, or prevents repeated work.
4. Prefer extractive preservation for facts, numbers, identifiers, commands, code, file paths, API contracts, error messages, and user commitments.
5. Use abstractive summaries only for narrative history, repetitive discussion, broad rationale, and low-risk background.
6. Keep provenance with every non-obvious claim: source file/path, URL, command, tool result, line reference, timestamp, or message turn.
7. Make compression reversible where possible: store or reference the original and include retrieval cues.
8. Evaluate compression with task-specific checks before relying on it.

## Compression Workflow

### 1. Define the Compression Brief

Before compressing, determine:

- objective: handoff, prompt shrink, RAG context, tool-output digest, code review, debugging, research synthesis, or memory update;
- downstream task and expected answer type;
- target token budget and maximum budget;
- loss tolerance: lossless, evidence-preserving, lossy-but-safe, or rough gist;
- required provenance format;
- recovery mechanism for omitted material.

If no token budget is provided, allocate roughly:

- 10-15% for active instructions and task goal;
- 20-30% for current state, constraints, and decisions;
- 40-60% for task-critical evidence;
- 5-10% for unresolved questions and next actions.

### 2. Segment Context by Sensitivity

Split the input into labeled blocks:

- `KEEP_EXACT`: system/developer/user constraints, acceptance criteria, credentials policy notes, security warnings, schemas, formulas, IDs, URLs, file paths, line references, failing assertions, stack traces, commands.
- `COMPRESS_EXTRACTIVE`: documents, retrieved passages, logs, diffs, source snippets, tables, issue threads.
- `COMPRESS_ABSTRACTIVE`: conversation history, rationale, repeated explanations, meeting notes, brainstorming.
- `DROP_OR_ARCHIVE`: duplicates, boilerplate, unrelated tool noise, successful install logs, repeated listings, stale branches of reasoning.
- `RETRIEVE_ON_DEMAND`: large artifacts that can be referenced by stable path, URL, execution ID, or query.

### 3. Score Importance

Rank each segment using these signals:

- direct relevance to current user request;
- recency and unresolved status;
- explicit user preference or requirement;
- factual specificity: numbers, IDs, names, signatures, dates, error text;
- causal role in the task: blockers, assumptions, decisions, tests, failures;
- uniqueness: information not repeated elsewhere;
- risk of omission: security, data loss, compliance, irreversible actions;
- retrieval value: whether it can be cheaply retrieved later.

For RAG, prefer diverse high-relevance evidence over redundant near-duplicates. For code, preserve function/class names, call chains, file paths, interfaces, failing tests, and exact error output.

### 4. Apply the Right Compression Pattern

Choose one or combine several:

#### Budgeted Extractive Compression

Use for logs, code, requirements, legal/compliance text, API docs, and factual evidence.

- Keep exact snippets and minimal surrounding context.
- Preserve stable references.
- Remove duplicates and boilerplate.
- Convert long lists into top-N items plus omitted-count metadata.

#### Abstractive Session Summary

Use for chat histories and agent sessions.

- Summarize decisions, state, rationale, completed work, pending work, user preferences, and blockers.
- Avoid inventing facts not present in history.
- Mark uncertainty explicitly.

#### Selective Augmentation for RAG

Use for retrieved documents.

- Remove irrelevant retrieved chunks even if they match keywords.
- Summarize only evidence that helps answer the question.
- Emit an empty or minimal context when retrieval is irrelevant.
- Keep citations or document handles.

#### Reversible Context Compression

Use for tool outputs, files, logs, and RAG chunks in agent systems.

- Store full originals externally or preserve stable handles.
- Send compressed summaries plus retrieval instructions.
- Include exact search keys for recovery.

#### Rolling Memory Compression

Use for long-running agents.

- Maintain pinned slots: user preferences, project context, active tasks, decisions, tool guidelines, known pitfalls.
- Deduplicate new observations before summarizing.
- Refresh summaries at session end and retrieve only budgeted relevant memories at session start.

#### Prompt Compressor Model Pattern

Use when an implementation can call compressor libraries such as LLMLingua or Selective Context.

- Separate instruction, question, and context fields.
- Compress context more aggressively than instruction/question.
- Start with conservative ratios such as 0.5, then benchmark lower ratios.
- Force preservation of separators, newlines, question marks, code delimiters, JSON braces, and domain-critical symbols when supported.

#### Inference-Time KV Cache Compression

Use only when controlling model serving/runtime, not ordinary prompt writing.

- Consider attention-based KV retention methods for long-generation workloads.
- Preserve attention sinks or initial tokens for streaming settings.
- Benchmark quality, latency, and memory against the target model and workload.

### 5. Emit a Structured Compressed Context

Use this format unless the user requested another one:

```markdown
# Compressed Context

## Objective
- ...

## Non-Negotiable Instructions and Constraints
- ...

## Current State
- Completed: ...
- In progress: ...
- Pending: ...

## Key Evidence
- [source: path/url/tool-result] exact or near-exact fact/snippet

## Decisions and Assumptions
- Decision: ... Evidence: ...
- Assumption: ... Confidence: high|medium|low

## Omitted or Archived Material
- ... omitted because ... Recovery: ...

## Retrieval Hooks
- Query/path/URL/execution ID: ...

## Next Actions
- ...
```

### 6. Validate the Compression

Run these checks before using the compressed result:

- Constraint check: every hard instruction and acceptance criterion is preserved.
- Entity check: names, IDs, dates, file paths, URLs, command flags, and numbers are unchanged.
- Evidence check: each claim has provenance or is labeled as inference.
- Coverage check: all active subtasks and blockers remain visible.
- Retrieval check: omitted important material has a handle or query to recover it.
- Faithfulness check: the summary does not add facts, conclusions, or commitments not present in the original.
- Budget check: compressed context fits the target token budget with room for response generation.

## Compression Ratios

Use conservative defaults and tighten only after validation:

- Safety-critical, legal, security, API schemas, failing tests: 0-20% reduction; mostly exact extraction.
- Code/debugging context: 30-60% reduction; preserve exact error messages and interfaces.
- RAG evidence: 50-80% reduction; keep diverse cited facts.
- Logs/tool outputs: 70-95% reduction; keep anomalies, warnings, final errors, counts, commands.
- Chat history/session handoff: 60-90% reduction; preserve state, decisions, commitments.
- Brainstorming/background: 80-95% reduction or archive.

## Anti-Patterns

Avoid:

- compressing instructions and questions at the same rate as background context;
- dropping provenance because the compressed text sounds self-contained;
- summarizing code or errors so aggressively that exact tokens disappear;
- retaining all retrieved chunks just because they are similar to the query;
- hiding uncertainty or conflicts;
- deleting originals when the compression is lossy;
- benchmarking only token savings without answer quality checks;
- using KV-cache compression advice when only prompt-level control is available.

## Research Basis

This skill synthesizes practices from public GitHub repositories that satisfy the project requirement of 5+ stars and/or 5+ forks:

| Repository | Stars/Forks checked 2026-06-01 | Applied practice |
|---|---:|---|
| `microsoft/LLMLingua` | 6232 / 385 | Separate instruction/question/context, budget control, prompt sensitivity, LongLLMLingua for long context, forced token preservation, experiment with ratios. |
| `liyucheng09/Selective_Context` | 420 / 24 | Self-information based content filtering for sentences/phrases/tokens; long-document and long-conversation context reduction. |
| `carriex/recomp` | 148 / 8 | RAG compression with selective augmentation; extractive and abstractive compressors; omit irrelevant retrieved context. |
| `chopratejas/headroom` | 3519 / 291 | Compress tool outputs/logs/files/RAG chunks before the LLM; route by content type; preserve originals for retrieval. |
| `rohitg00/agentmemory` | 20388 / 1681 | Deduplicate, privacy-filter, compress observations, maintain memory slots, and retrieve within a token budget. |
| `FMInference/H2O` | 518 / 81 | Attention-based KV cache retention for efficient generation where runtime control exists. |
| `mit-han-lab/streaming-llm` | 7232 / 399 | Preserve attention sinks/initial tokens for stable streaming long-context inference. |
| `NVIDIA/kvpress` | 1098 / 147 | Operational KV cache compression patterns for supported model-serving stacks. |

## Output Quality Bar

A good compressed context is smaller, faithful, source-grounded, task-shaped, and recoverable. Prefer a slightly longer context that preserves constraints and evidence over an aggressively short summary that forces the next model to guess.
