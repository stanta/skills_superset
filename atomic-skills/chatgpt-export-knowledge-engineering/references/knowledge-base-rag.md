# Turning ChatGPT history into a trustworthy knowledge base

## Primary principle

A conversation is **evidence of what was said**, not automatic evidence that the statement was true, is still true or represents the user's current preference. Do not collapse assistant speculation, obsolete proposals and later corrections into one “fact.” For project memory, keep *claims* with author, time, source and status.

## 1. Logical data model

Recommended relational entities:

- `imports` (`import_id`, source hash, acquired_at, adapter_version, privacy_policy, parser_options).
- `conversations` (`conversation_id`, title, source import, creation/update UTC, topic/project labels as separate derived data).
- `messages` (`conversation_id`, `node_id` primary compound key within an import/revision; parent, author role, message_id, channel, timestamp, source_member, text, text_sha256, content_type, unsupported_parts).
- `assets` (`asset_id`, source filename/pointer, byte hash *if actually present*, media type, availability_state, ACL).
- `message_asset_links` (message locator, asset ID/pointer, relation, verification status).
- `chunks` (`chunk_id`, source locators, character offsets, normalized text, splitter/version, branch/path context, security labels).
- `claims` (`claim_id`, subject, predicate, value, validity period, asserted_at, speaker, source_message, status, confidence, extraction model/version).
- `claim_relations` (supports, refutes, supersedes, duplicates, depends_on).
- `projects` and `conversation_projects` (many-to-many; topic tags are hypotheses until validated).
- `embedding_index` (chunk_id, embedding model/version, vector store key, privacy/retention context, last_refresh).

Keep raw archival identifiers independent of title; titles and project tags change. Use stable foreign keys to avoid duplicating the same source message in multiple project collections.

### Minimal SQLite / FTS5 example

```sql
PRAGMA foreign_keys = ON;

CREATE TABLE messages (
  conversation_id TEXT NOT NULL,
  node_id TEXT NOT NULL,
  parent_node_id TEXT,
  role TEXT,
  created_at TEXT,
  source_member TEXT NOT NULL,
  source_json_sha256 TEXT NOT NULL,
  body TEXT,
  PRIMARY KEY (conversation_id, node_id)
);

CREATE VIRTUAL TABLE messages_fts USING fts5(
  body, conversation_id UNINDEXED, node_id UNINDEXED,
  tokenize='unicode61'
);

INSERT INTO messages_fts (body, conversation_id, node_id)
SELECT body, conversation_id, node_id FROM messages;

SELECT m.conversation_id, m.node_id, snippet(messages_fts, 0, '[', ']', '…', 20) AS excerpt
FROM messages_fts
JOIN messages AS m
 ON m.conversation_id = messages_fts.conversation_id
 AND m.node_id = messages_fts.node_id
WHERE messages_fts MATCH 'графон*'
LIMIT 20;
```

SQLite full-text search uses language-agnostic Unicode tokenization; for Russian morphology or fuzzy concepts consider stemming, multilingual embeddings or language-aware preprocessing. Apply branch selection, security and time filters in the surrounding query, not only the FTS expression. Ingest only authorized indexed data.

## 2. Chunking and lineage

- Start at a **message boundary**. Preserve entire short messages. For long messages, split at structural paragraphs/headings with overlap where useful.
- Chunk IDs should be deterministic: hash of source locator + offsets + splitter version. Store original character offsets and source UTF-8 byte ranges if reproducibly computed.
- Avoid combining sibling answers that are different branches. For multi-turn context, store a contextual window that follows *parent pointers on one selected path*; do not indiscriminately concatenate by timestamp.
- For every chunk, store ACL/project/time/role/branch and input hash; maintain a direct link to raw JSON source and node ID.
- Link human-visible Markdown file for convenience only; use source locator as authoritative citation.
- A derived summary can be indexed, but store `derived_from` locators and distinguish it from original authored content. Never use summaries as sole evidence for critical claims.

## 3. Retrieval architecture

Preferred baseline for a moderate archive: **SQLite FTS5** for exact search + SQLite/PostgreSQL for metadata + **local embeddings/Qdrant/FAISS** only if semantic retrieval is needed and approved. Start with exact retrieval; add vector infrastructure after testing its benefit.

```text
Question and project/time permissions
    -> metadata/ACL filter
    -> keyword search (FTS) + optional multilingual vector ANN
    -> reciprocal rank fusion or evaluated weighted merging
    -> deduplicate by source locator and branch
    -> rerank under the same authorization constraints
    -> evidence packets (quoted spans, IDs, dates, branch)
    -> grounded answer with traceable citations and uncertainty
```

- Enforce ACL **before** retrieval and again before presenting evidence.
- Use question intent filters (`project`, `from/to`, `role`, `branch current/all`, `source revision`).
- For “what did we decide?” prefer final authoritative user messages and versioned decisions, while retaining earlier contradicted alternatives.
- For “what was discussed?” preserve chronological evidence and uncertainty; don't claim a canonical decision where none is recorded.
- For “what do I believe?” do not infer personal identity or lasting preferences from one assistant message.
- If verified source spans are missing, return “not found in indexed export,” not “this never happened.”
- If a record contains image/audio references with no verified decoded contents, don't hallucinate descriptions.

## 4. Knowledge extraction contract

An LLM-generated `claim` is always derived, and has:
```json
{
  "claim_id": "cl-001",
  "project": "synthetic-project",
  "statement": "The team chose an API-first architecture",
  "source": {"conversation_id": "c-1", "node_id": "n-7", "span_start": 0, "span_end": 42},
  "asserted_at": "2026-10-01T13:00:00Z",
  "speaker_role": "user",
  "status": "proposed",
  "confidence": 0.82,
  "valid_from": null,
  "supersedes": [],
  "extractor": {"name": "local-model", "version": "demo"}
}
```

Status vocabulary: `proposed` / `approved` / `rejected` / `superseded` / `disputed` / `unknown`. Promote to `approved` only when supported by explicit authorized approval; assistant assumptions do not count. Treat confidence as model output, not verification.

For citations in an answer, show a plain-language reference such as “Chat title — YYYY-MM-DD UTC — message node ID”; include direct source offsets when indexed. Do not invent clickable links if the raw export does not contain a valid share URL.

## 5. Incremental ingestion and consistency

1. Compute SHA-256 per original conversation JSON source. Same hash + adapter config → skip expensive repeat parsing.
2. Deduplicate nodes by (`conversation_id`, `node_id`, source revision) and chunks by (node locator, offsets, splitter version).
3. If a node changes, keep old revision under configured retention, update text index, invalidate embeddings and derived claims that depend on that node.
4. Handle node disappearance according to archive policy; **absence does not prove deletion or revoke archival permission**. Explicit deletion requirements propagate through indexes, caches, derived claims and backups.
5. Include parser, index, embedding-model and prompt versions in manifests. Rebuild when any affects derived output.
6. Separate `current path` vs `all graph`: cache and report branch mode as an input parameter to avoid silently changing denominators.
7. Keep summaries refreshed when upstream claims are superseded. Provide a “contradictions and revisions” report.

## 6. Evaluation before production

Prepare a **synthetic** gold set plus opt-in hand-labeled real user queries across categories: exact quotation, project decision, corrected decision, time-bounded recall, edited branch, near-duplicate, contradictory claims, confidential project, attachment-only question and answer-not-present.

Track retrieval Recall@k, MRR/nDCG, grounded citation precision, branch/path validity, factuality, outdated answer rate, no-answer calibration, PII leakage and latency. Define minimum acceptance thresholds for the user's use case; avoid asserting universal numeric quality gates. For high-stakes medical, financial or legal material, apply an independent domain verification gate and user-controlled access policy.

## 7. Cost/performance staging

- Start: disk archive + JSONL + SQLite FTS5; zero external calls.
- Next: local multilingual embedding model and SQLite or FAISS/Qdrant if semantic questions beat keyword search in held-out tests.
- Scale: incremental message/chunk partitioning, streaming JSON adapter for large exports, transactional upserts and verified snapshot backups.
- Add cross-project entity graph or graph-RAG only if tests demonstrate improvements over simpler hybrid retrieval. Avoid a semantic graph that encodes speculative associations as facts.

See `rag-architect` for advanced index design and `ai-agent-response-data-quality` for evidence verification.