# Operations, tests, completeness and troubleshooting

## Runbook: export → verified local derivatives

**Prerequisites:** user-authorized exported ZIP or extracted directory; Python 3.11+; sufficient local disk and RAM; controlled private destination. The included parser is dependency-free and **text-view only**.

### 1. Store and fingerprint raw input

```bash
mkdir -p /private/chatgpt-export
chmod 700 /private/chatgpt-export
cp /downloads/chatgpt-export.zip /private/chatgpt-export/
chmod 600 /private/chatgpt-export/*.zip
sha256sum /private/chatgpt-export/chatgpt-export.zip
unzip -l /private/chatgpt-export/chatgpt-export.zip
```

`unzip -l` enumerates without extracting (file names could be sensitive; don't paste them into public logs). If an archive is unexpectedly encrypted, truncated or very large, stop and diagnose first. Windows users may enumerate ZIP via a trusted local library without extraction.

### 2. Produce current-path and all-node views

```bash
python3 scripts/chatgpt_export.py /private/chatgpt-export/chatgpt-export.zip \
  --out /private/chatgpt-current --mode current

python3 scripts/chatgpt_export.py /private/chatgpt-export/chatgpt-export.zip \
  --out /private/chatgpt-graph --mode all
```

Paths above assume the working directory is `atomic-skills/chatgpt-export-knowledge-engineering/`. The tool creates outputs with restrictive local permissions via a restrictive umask. It does not modify the ZIP or decode the assets.

### 3. Validate manifests and message rows

```bash
python3 - <<'PY'
import json
from pathlib import Path
folder = Path("/private/chatgpt-current")
manifest = json.loads((folder / "manifest.json").read_text())
rows = [json.loads(line) for line in (folder / "messages.jsonl").open()]
assert manifest["messages"] == len(rows)
assert len({(r["conversation_id"], r["node_id"]) for r in rows}) == len(rows)
assert all(r.get("source_member") and r.get("source_json_sha256") for r in rows)
print({k: manifest[k] for k in ("conversations", "messages", "nontext_parts")})
PY
```

Note: this quick validation loads messages into memory. For very large outputs use streaming row counters/SQLite. It checks structural consistency but cannot verify that all graphical/UI elements were preserved.

### 4. Generate a retrieval-ready DB only after checking quality

- Load `conversations.jsonl` and `messages.jsonl` with transaction/rollback semantics; enforce uniqueness and foreign keys.
- Branch selection is part of import metadata.
- Store raw JSON SHA-256 and full provenance keys for citations.
- Use FTS5 initially; add embeddings and permissions under an explicit architecture and privacy decision (see `knowledge-base-rag.md`).
- Do not load `user.json` or raw account metadata into a search engine unless specifically necessary and authorized.

## Unit and acceptance test cases

Run from the skill directory:

```bash
python3 -m unittest discover -s scripts -p 'test_*.py' -v
```

Expected synthetic-only tests:
- [x] Active path excludes an alternate assistant answer; full-graph mode includes both.
- [x] Multiple numbered conversation JSONs deduplicate identical repeated nodes.
- [x] Missing `current_node` preserves all graph nodes with warning, not guess.
- [x] Tool role is not silently dropped; nontext count and asset pointer remain visible.
- [x] ZIP path traversal is rejected before reading conversation JSON.
- [x] Conflicting duplicate node payloads fail rather than silently overwrite.
- [x] Every exported message has raw source-member and SHA-256 provenance.

Additional production/format-regression tests to add when real examples are available **with explicit permission**:
- malformed JSON, BOM, unknown schema, empty archive, nested member paths, invalid UTF-8;
- symlink ZIP entries, too many files, decompression ratio and resource-limit rejection;
- missing/dangling parents, cycles and invalid message shapes;
- nested image, audio, video, file pointers, inaccessible media and unknown content types;
- timestamps including null, zero, negative, float, unreasonable values and timezone ambiguity;
- very large sharded exports with bounded-memory streaming adapter and resumability;
- Linux/macOS/Windows path and permission policy; Unicode/Cyrillic, HTML/Markdown injection;
- incremental reimport, changed revisions, ACL reindex, deletion and rollback.

## Explicit acceptance contract

| Gate | Pass condition |
| --- | --- |
| Acquisition | Eligible authorized source; original retained; SHA-256 documented |
| Safety | No automatic ZIP extraction, code execution or external network access; resource/path checks passed |
| Parse | All recognized JSON members consumed or failing member named; unsupported top-level shapes stop with diagnostic |
| Graph | Per-conversation active path or full graph chosen explicitly; graph warnings surfaced |
| Coverage | Unique conversations/nodes/messages and skipped nontext reported; no false claim of full media coverage |
| Provenance | Each derived message refers to immutable raw JSON SHA-256 + member + conversation/node IDs |
| Consistency | No conflicting duplicate IDs silently accepted; same input+mode yields stable logical rows |
| Confidentiality | All raw/derived data remains within authorized private store |
| Retrieval (when requested) | Queries cite actual source locators; no-answer and changed-decision cases evaluated |

## Troubleshooting matrix

| Symptom | Next diagnostic |
| --- | --- |
| `No conversations JSON files recognized` | Inventory all ZIP members; numbered naming may have changed; inspect keys locally and implement a versioned adapter. |
| `Unrecognized top-level format` | Inspect data type/keys privately; don't assume the document is a conversation list. |
| `Conflicting duplicate nodes` | Compare source_member SHA-256 and node payloads, identify newer revision; resolve under explicit policy and retain both snapshots if appropriate. |
| Current-mode output unexpectedly small | Check `current_node`/parent chain; compare `--mode all` and null-message/root counts. |
| “Missing” chat | Check export eligibility, deleted status, shard discovery and whether the chat was saved; do not assert recoverability. |
| Missing images or audio | Inspect verified ZIP media members, content types and opaque pointers; text view cannot decode media automatically. |
| Out-of-memory reading JSON | Use a streaming parser with limits or partition the source JSON; the included standard-library adapter loads one JSON member into RAM. |
| External DB/API refuses upload | Do not bypass DLP or permissions; use local SQLite or obtain explicit authorization. |
| Search finds outdated/contradictory answers | Preserve time, author, branch and supersession links; review extraction/claim states. |

## Change control

Every change to the format adapter or CLI must add a synthetic regression test, update this guide and increment the normalized schema version if meaning changes. Do not build fixtures from an actual user's private export. Run repository meta-skill catalog validation and the skill's isolated Python tests before merging.