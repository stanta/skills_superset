# Source notes for LangGraph and LangChain skills

## Verification rule

Use only repositories with at least five stars or five forks as external source material.

## Repositories checked

| Repository | Stars checked | Forks checked | Usage |
|---|---:|---:|---|
| https://github.com/langchain-ai/langchain | 144444 | 24045 | LangChain framework patterns, agents, structured output, tools, middleware, retrieval, production guidance |
| https://github.com/langchain-ai/langgraph | 39901 | 6708 | LangGraph state graphs, checkpointing, interrupts, routing, streaming, agent loops |
| https://github.com/langchain-ai/langgraphjs | 3212 | 550 | TypeScript/JavaScript LangGraph parity and production orchestration references |
| https://github.com/langchain-ai/langgraph-101 | 575 | 142 | Learning examples for local graph development and fundamentals |
| https://github.com/langchain-ai/langgraph-example | 519 | 357 | Deployable LangGraph example patterns |
| https://github.com/langchain-ai/langsmith-cookbook | 1036 | 185 | Observability, tracing, eval, and production debugging examples |
| https://github.com/vonzosten/awesome-LangGraph | 1965 | 256 | Ecosystem survey and cross-project pattern discovery |

Counts were checked through the GitHub API during skill creation on 2026-08-18.

## Official documentation concepts incorporated

- LangGraph state schemas and append reducers for message history.
- Conditional edges and explicit router maps.
- Checkpointer configuration and thread-based state isolation.
- Human interrupts before tools and human-in-the-loop approval flows.
- LangChain structured output strategies using provider-native and tool-based schema enforcement.
- LangChain middleware for context normalization, dynamic model selection, and production controls.
- Event streaming and final-state separation.
- Context engineering, retrieval boundaries, privacy-safe tracing, and regression evaluation.

## Workspace evidence incorporated

- Creative validator architecture uses LangGraph after deterministic status calculation for user-facing AI summaries.
- Advertising workflows require large CSV/XLSX data to stay out of prompt context and pass compact DuckDB metadata instead.
- n8n workflow typing includes AI dependency maps for language models, memory, parsers, tools, retrievers, rerankers, and vector stores.
