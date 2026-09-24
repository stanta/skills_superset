# Discovery Plane MVP

Local CLI + optional MCP stdio wrapper. No daemon, model, paid API, external DB or
runtime dependency is needed for CLI. It indexes SKILL.md frontmatter only.

Run from the repository root:

    python discovery/skills_discovery.py index
    python discovery/skills_discovery.py search "react typescript error" --top-k 3
    python discovery/skills_discovery.py eval
    python -m unittest discover -s discovery -p 'test_*.py' -v

Indexing reuses unchanged entries by SHA-256 and prunes deleted skills. CI runs
index --check, tests and a routing smoke eval. Curated aliases and explicit
negative intents/dependencies live in overrides.json. Do not infer dependencies.

Optional MCP: install the package mcp[cli], then configure your agent to run
python /absolute/path/to/discovery/mcp_server.py over stdio. Exposed tools:
search_skills(query, top_k) and read_skill(path). The latter only reads indexed
SKILL.md files, not arbitrary paths.

Agent instruction: "Before picking a skill, call search_skills. Read only the
selected 1-3 SKILL.md files. If routing is uncertain, refine the query or use
ordinary repository search. Never execute skill scripts without normal approval."

Hybrid ranker = weighted BM25 plus trigram TF-IDF cosine and exact aliases.
Trigrams are fuzzy matching, NOT neural embeddings. Synonyms and multilingual
coverage require aliases until optional embeddings are implemented.
Evaluation reports recall@1, recall@5, MRR@5 and no-skill accuracy; the bundled
cases are a smoke test, not a production benchmark. Neither actual token savings
nor downstream task quality is measured by this MVP.
