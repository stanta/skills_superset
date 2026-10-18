# Source provenance and evidence limits (checked 2026-10-18)

**Official OpenAI help references** (public documentation; verify again before giving account-specific or time-sensitive instructions):

1. [Exporting your ChatGPT history and data](https://help.openai.com/en/articles/7260999-exporting-your-chatgpt-history-and-data) — export eligibility, Settings/Data controls flow, Privacy Portal, ZIP delivery, 7-day wait and 24-hour link expiry.
2. [Transfer exported conversations between ChatGPT accounts](https://help.openai.com/en/articles/9106926-transfer-exported-conversations-between-chatgpt-accounts) — explicitly names `conversations.json` and numbered conversation JSON files; allows reference upload but not restoration of sidebar, account/memory/settings or subscriptions.
3. [Exporting data from a ChatGPT Edu workspace](https://help.openai.com/en/articles/20001279-exporting-data-from-a-chatgpt-edu-workspace) — eligibility, workspace restrictions and exports including conversation JSONs, possible files/assets and metadata.
4. [ChatGPT shared links FAQ](https://help.openai.com/en/articles/7925741-chatgpt-shared-links-faq) — `shared_conversations.json` and limitations regarding scheduled tasks and their shared links.

**Schema confidence boundary:** None of the linked Help Center pages specifies a complete, stable, publicly versioned contract for `mapping`, `current_node`, part types or attachment pointers. Those fields are observed export patterns. This skill's parser is a conservative, tested adapter for common observed shapes, **not** an OpenAI-maintained reference parser. Treat new or missing fields as explicit format drift. Do not invent completeness guarantees about images, tools, metadata, old deleted chats or current account state.

**Dependency boundary:** Python standard-library `zipfile`/`json`/`hashlib`/`sqlite3` are implementation choices; the optional search/RAG stacks in the guide are architecture recommendations, not required components of OpenAI export.

**Last source review:** 2026-10-18. Refresh official documentation before using this skill for new workspaces, new export variants or policy-sensitive transfers.