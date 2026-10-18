# ChatGPT data export: formats, acquisition and source boundaries

## What official OpenAI help documents confirm (checked October 2026)

1. Eligible signed-in users request export via **Settings → Data controls → Export** or via the Privacy Portal. Exports are delivered by link, commonly email/SMS; OpenAI says preparation can take up to **7 days** and links expire after **24 hours**.
2. A downloaded **ZIP** contains chat history and other relevant account data. Eligible workspaces vary. Personal Free, Go, Plus, Pro and eligible Edu users may have this option; Business, Enterprise and ChatGPT for Healthcare do not offer normal self-service export; Edu is admin/role/residency dependent.
3. Official account-transfer instructions explicitly name `conversations.json` and note that **large archives may contain numbered conversation JSON files**. Uploaded JSON can be used as *reference* in another personal ChatGPT account; this is not an account merge or reconstruction of sidebar chats.
4. Official shared-link FAQ says a personal export has `shared_conversations.json` holding shared conversation link metadata; scheduled-task content/links/snapshots are not currently included.
5. **The exact `conversations.json` node schema is not guaranteed by a public, versioned OpenAI export API.** Treat the mapping structure below as an observed format, not a contractual guarantee. Record mismatches and add explicit adapters rather than inventing data.

Sources and dates: [sources.md](sources.md).

## Typical ZIP inventory — examples, NOT a mandatory contract

| Observed/possible member | Interpret cautiously |
| --- | --- |
| `conversations.json` | Conversation objects with metadata and message graph |
| `conversations_1.json`, `conversations-2.json`, etc. | Numbered conversation JSON shards; inspect archive for exact naming |
| `chat.html` | Human-facing transcript view if supplied; not a canonical parse source |
| `shared_conversations.json` | Shared-conversation metadata, not the content of every shared link |
| `user.json`, feedback and account files | Separate sensitive account metadata, inventory by actual file names |
| Other JSON and asset members | Files, images/audio, pointers or derived artifacts only if present and verified |

**Do not guarantee** the presence of `chat.html`, `user.json`, media bytes, certain metadata or all deleted conversations. A text JSON reference to an attachment does *not* prove its bytes are in the ZIP.

## Observed conversation object — non-authoritative, simplified

```json
{
  "id": "conversation-id",
  "title": "A title",
  "create_time": 1700000000,
  "update_time": 1700000300,
  "current_node": "leaf-node-id",
  "mapping": {
    "root-node-id": {
      "id": "root-node-id",
      "parent": null,
      "children": ["u1"],
      "message": null
    },
    "u1": {
      "parent": "root-node-id",
      "children": ["a1", "a2"],
      "message": {
        "id": "message-id",
        "author": {"role": "user"},
        "create_time": 1700000001,
        "content": {"content_type": "text", "parts": ["Hello"]}
      }
    }
  }
}
```

The sample is synthetic and intentionally incomplete. Some messages have null bodies, tool/system authors, metadata, edited prompts, multiple siblings, multimodal parts and formats other than string `parts`. Fields may be absent or added. Never flatten by iterating dictionary insertion order or sorting nodes by timestamps and then claiming this is the displayed chat.

## Media and other content types

- A string part is text; a part object may contain an image/audio/video/file pointer, a text field or a different typed structure. Handle unknown parts losslessly in raw storage and mark them as unsupported in a text view.
- Other resources may be separate ZIP members, external references or unavailable; use verified content addressing and user-approved specialist parsers for actual media.
- A link to remote content should not automatically be fetched; it can be expired, untrusted, private or subject to separate access permissions.
- Timestamps are often epoch seconds; validate type and range. Do not confuse message create time with conversation update time. Record unknown timezones for text authored *inside* messages.

## Format-drift playbook

1. Generate an inventory: JSON member names, total bytes, top-level type, example **keys only** (not private values), content-type distribution, per-shard counts.
2. Identify adapter based on observed shape, never solely on calendar date, subscription, project name or guessed model.
3. Compare actual raw node/message IDs to normalized counts; report missing types and dangling references.
4. For new shapes create synthetic fixture reproducing structural change, implement tested versioned adapter and rerun before deriving knowledge.
5. Preserve original ZIP and its SHA-256, so all data transformations can be audited later.

## Account-transfer caveats

A reference upload into another ChatGPT conversation is supported for eligible personal accounts, but it does not recreate old chats, memory, files, custom instructions, subscriptions, GPTs or workspace membership. Large JSON files may require separately uploading numbered files or splitting content. Do not recommend sharing a raw export in a public chat or GitHub repository.