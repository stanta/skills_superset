# KiloCode AI Workflow Repository

This repository contains a structured, documentation-first workflow for AI-assisted software delivery. It combines:

- custom agent modes;
- reusable skill packs;
- workflow commands and templates;
- research and review documents that support better architecture, code quality, testing, and documentation.

The repository is best understood as an internal toolkit for running a multi-agent development process from business idea to implementation, testing, and technical documentation.

---

## Table of Contents

1. [Repository Purpose](#repository-purpose)
2. [Who This Repository Is For](#who-this-repository-is-for)
3. [How the Workflow Is Organized](#how-the-workflow-is-organized)
4. [Repository Structure](#repository-structure)
5. [Main Entry Points](#main-entry-points)
6. [Workflow Stages](#workflow-stages)
7. [Key Directories in Detail](#key-directories-in-detail)
8. [Skill Navigation](#skill-navigation)
9. [Research and Review Documents](#research-and-review-documents)
10. [Configuration Files](#configuration-files)
11. [Getting Started](#getting-started)
12. [Typical Usage Paths](#typical-usage-paths)
13. [Notes and Conventions](#notes-and-conventions)

---

## Repository Purpose

The repository defines a repeatable AI-supported delivery process with clear role separation.

At a high level, it supports work such as:

- turning business needs into epics and feature specifications;
- converting specifications into technical plans;
- implementing code and tests through specialized agents;
- producing technical and architectural documentation;
- maintaining reusable skills and examples for future tasks.

The process is described in detail in [workflows/.ai/full-project.md](workflows/.ai/full-project.md) and mirrored by mode definitions in [.kilocodemodes](.kilocodemodes).

---

## Who This Repository Is For

This repository is most useful for:

- AI workflow designers;
- technical leads defining structured delivery processes;
- teams using KiloCode custom modes and skills;
- engineers who want a documented path from requirements to implementation;
- technical writers and architects documenting delivery standards.

---

## How the Workflow Is Organized

The repository follows a staged model of work.

A simplified flow looks like this:

1. Business need is described.
2. An epic may be created for large initiatives.
3. A feature specification is written.
4. A summary technical plan is produced.
5. Development and test plans are created per task.
6. Code is implemented.
7. Tests are implemented.
8. Technical documentation is written.
9. Architecture documentation is updated.

The conceptual overview is documented in [workflows/.ai/full-project.md](workflows/.ai/full-project.md), while practical examples are collected in [workflows/.ai/examples/README.md](workflows/.ai/examples/README.md).

---

## Repository Structure

```text
.
├── README.md
├── .gitignore
├── .kilocodemodes
├── package.json
├── bun.lock
├── docs/
│   ├── research/
│   └── reviews/
├── skills/
└── workflows/
    ├── fullproject.md
    └── .ai/
        ├── CustomModes.yaml
        ├── full-project.md
        ├── plan.md
        ├── agents/
        ├── commands/
        ├── examples/
        └── rules/
```

### Directory summary

| Path             | Purpose                                                                       |
| ---------------- | ----------------------------------------------------------------------------- |
| `docs/`          | Research reports and review documents that inform standards and improvements. |
| `skills/`        | Reusable skill definitions for specialized agent behavior.                    |
| `workflows/`     | Core workflow documentation, command guides, templates, and examples.         |
| `.kilocodemodes` | Custom mode definitions used by the agent system.                             |
| `package.json`   | Minimal Node package manifest used for KiloCode plugin dependency management. |

---

## Main Entry Points

If you are new to the repository, start with these files in order:

1. [README.md](README.md) — repository overview and navigation.
2. [workflows/.ai/full-project.md](workflows/.ai/full-project.md) — full workflow concept.
3. [workflows/.ai/examples/README.md](workflows/.ai/examples/README.md) — practical navigation for examples.
4. [workflows/.ai/examples/QuickStartGuide.md](workflows/.ai/examples/QuickStartGuide.md) — step-by-step walkthrough.
5. [.kilocodemodes](.kilocodemodes) — mode catalog mapped to workflow stages.

---

## Workflow Stages

The repository defines the following main stages.

| Stage                         | Goal                                                        | Primary references                                                                         |
| ----------------------------- | ----------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| 0. Epic planning              | Break a large initiative into stages and business outcomes. | [workflows/.ai/agents/epic-writer.md](workflows/.ai/agents/epic-writer.md)                 |
| 1. Feature specification      | Turn business intent into functional requirements.          | [workflows/.ai/agents/feature-writer.md](workflows/.ai/agents/feature-writer.md)           |
| 2. Summary technical planning | Create a high-level implementation plan for a feature.      | [workflows/.ai/agents/summary-plan-writer.md](workflows/.ai/agents/summary-plan-writer.md) |
| 3. Development planning       | Produce a task-level coding plan.                           | [workflows/.ai/agents/dev-plan-writer.md](workflows/.ai/agents/dev-plan-writer.md)         |
| 4. Test planning              | Produce a task-level testing plan.                          | [workflows/.ai/agents/test-plan-writer.md](workflows/.ai/agents/test-plan-writer.md)       |
| 5. Code implementation        | Implement planned functionality.                            | [workflows/.ai/agents/php-developer.md](workflows/.ai/agents/php-developer.md)             |
| 6. Test implementation        | Implement tests for delivered functionality.                | [workflows/.ai/agents/php-test-developer.md](workflows/.ai/agents/php-test-developer.md)   |
| 7. Technical documentation    | Write implementation-facing documentation.                  | [workflows/.ai/agents/tech-doc-writer.md](workflows/.ai/agents/tech-doc-writer.md)         |
| 8. Architecture documentation | Update system-level architecture documentation.             | [workflows/.ai/agents/arch-doc-writer.md](workflows/.ai/agents/arch-doc-writer.md)         |

The same lifecycle is reflected in the custom modes listed in [.kilocodemodes](.kilocodemodes).

---

## Key Directories in Detail

### `workflows/`

This is the core process directory.

Important files and subdirectories:

- [workflows/.ai/full-project.md](workflows/.ai/full-project.md) — conceptual description of the end-to-end process.
- [workflows/.ai/CustomModes.yaml](workflows/.ai/CustomModes.yaml) — YAML version of workflow-oriented mode definitions.
- [workflows/.ai/agents/](workflows/.ai/agents/) — role-specific instructions for each stage.
- [workflows/.ai/commands/](workflows/.ai/commands/) — command-level usage guides.
- [workflows/.ai/examples/](workflows/.ai/examples/) — onboarding material, examples, and FAQ.
- [workflows/.ai/rules/](workflows/.ai/rules/) — supporting standards and guidance.
- [workflows/.ai/agents/Template/](workflows/.ai/agents/Template/) — reusable templates for generated artifacts.

### `skills/`

This directory contains reusable specialist skills. Each skill typically includes a [SKILL.md](skills/techwriter/SKILL.md) file and, in many cases, supporting reference documents.

Examples of skill categories present in the repository include:

- architecture and technical design;
- API design;
- code review and security review;
- debugging and testing;
- frontend, backend, database, and infrastructure specialties;
- documentation and technical writing.

This directory is intended to make agent behavior more consistent, reusable, and easier to maintain.

### `docs/`

This directory contains reference documentation about quality, architecture, and process improvement.

Current visible sections:

- [docs/research/](docs/research/) — longer research reports.
- [docs/reviews/](docs/reviews/) — focused review and gap-analysis documents.

---

## Skill Navigation

The [skills/](skills/) directory contains reusable specialist capabilities. Use this section as a directory map when selecting a skill for a task or when updating skill documentation.

### Architecture, platform, and operations

| Skill                                                      | Use when you need                                                                          |
| ---------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| [architecture-designer](skills/architecture-designer/)     | System architecture, architecture decisions, scalability planning, or architecture review. |
| [cloud-architect](skills/cloud-architect/)                 | Cloud architecture, migration planning, disaster recovery, and cost optimization.          |
| [devops](skills/devops/)                                   | CI/CD, infrastructure automation, secure delivery, and developer workflow optimization.    |
| [devops-engineer](skills/devops-engineer/)                 | Docker, Kubernetes, Terraform, GitOps, deployment automation, and platform operations.     |
| [kubernetes-specialist](skills/kubernetes-specialist/)     | Kubernetes workloads, Helm, RBAC, NetworkPolicies, storage, and pod troubleshooting.       |
| [legacy-modernizer](skills/legacy-modernizer/)             | Incremental modernization, strangler patterns, dependency mapping, and migration planning. |
| [microservices-architect](skills/microservices-architect/) | Service decomposition, distributed systems, DDD, sagas, CQRS, and service boundaries.      |
| [monitoring-expert](skills/monitoring-expert/)             | Metrics, logs, tracing, dashboards, alerts, profiling, and capacity planning.              |
| [sre-engineer](skills/sre-engineer/)                       | SLOs, error budgets, incident response, toil reduction, and reliability engineering.       |
| [terraform-engineer](skills/terraform-engineer/)           | Terraform modules, state management, provider configuration, and infrastructure testing.   |
| [use-railway](skills/use-railway/)                         | Railway deployments, services, environments, variables, domains, and troubleshooting.      |

### Backend, full-stack, and API development

| Skill                                                | Use when you need                                                                                 |
| ---------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| [api-designer](skills/api-designer/)                 | REST or GraphQL API design, OpenAPI specs, versioning, pagination, and error patterns.            |
| [csharp-developer](skills/csharp-developer/)         | C#, .NET, ASP.NET Core APIs, Entity Framework, Blazor, and async application patterns.            |
| [django-expert](skills/django-expert/)               | Django, Django REST Framework, models, serializers, viewsets, and ORM optimization.               |
| [dotnet-core-expert](skills/dotnet-core-expert/)     | .NET 8, Minimal APIs, clean architecture, CQRS, JWT, and cloud-native services.                   |
| [fastapi-expert](skills/fastapi-expert/)             | FastAPI, Pydantic, async Python APIs, SQLAlchemy async, JWT, and OpenAPI.                         |
| [fullstack-guardian](skills/fullstack-guardian/)     | Secure full-stack features spanning frontend, backend, database, and API layers.                  |
| [golang-pro](skills/golang-pro/)                     | Go services, goroutines, channels, gRPC, REST, benchmarks, and table-driven tests.                |
| [graphql-architect](skills/graphql-architect/)       | GraphQL schemas, resolvers, Apollo Federation, DataLoader, subscriptions, and query optimization. |
| [java-architect](skills/java-architect/)             | Enterprise Java, Spring Boot, JPA, WebFlux, Spring Security, OAuth2, and JWT.                     |
| [laravel-specialist](skills/laravel-specialist/)     | Laravel applications, Eloquent, Sanctum, Horizon, Livewire, APIs, and Pest/PHPUnit tests.         |
| [nestjs-expert](skills/nestjs-expert/)               | NestJS modules, controllers, services, DTOs, guards, interceptors, Swagger, and tests.            |
| [php-pro](skills/php-pro/)                           | Modern PHP, Laravel, Symfony, strict typing, PSR standards, PHPUnit, Pest, and APIs.              |
| [rails-expert](skills/rails-expert/)                 | Rails, Active Record, Hotwire, Turbo, Action Cable, Sidekiq, and RSpec.                           |
| [spring-boot-engineer](skills/spring-boot-engineer/) | Spring Boot, Spring Security, Spring Data JPA, WebFlux, and Java microservices.                   |
| [websocket-engineer](skills/websocket-engineer/)     | WebSocket or Socket.IO systems, real-time messaging, rooms, presence, and Redis scaling.          |

### Frontend, mobile, UI, and web platforms

| Skill                                                                  | Use when you need                                                                                      |
| ---------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| [angular-architect](skills/angular-architect/)                         | Angular standalone components, routing, guards, NgRx, RxJS, signals, and tests.                        |
| [flutter-expert](skills/flutter-expert/)                               | Flutter and Dart apps, widgets, Riverpod, Bloc, GoRouter, and performance tuning.                      |
| [frontend-react-dev](skills/frontend-react-dev/)                       | Senior React or Next.js frontend guidance across architecture, TypeScript, accessibility, and testing. |
| [frontend-vue-developer](skills/frontend-vue-developer/)               | Vue 3 or Nuxt frontend architecture, reactivity, TypeScript, accessibility, and testing.               |
| [nextjs-developer](skills/nextjs-developer/)                           | Next.js App Router, server components, server actions, route handlers, middleware, and Vercel.         |
| [nextjs15-vercel-ai-sdk](skills/nextjs15-vercel-ai-sdk/)               | Next.js 15, Vercel AI SDK, streaming chat, shadcn/ui, Zustand, TanStack Query, and Tailwind.           |
| [react-expert](skills/react-expert/)                                   | React components, hooks, Suspense, server components, rendering issues, and state management.          |
| [react-native-expert](skills/react-native-expert/)                     | React Native or Expo apps, navigation, native modules, FlatList performance, and platform behavior.    |
| [shopify-expert](skills/shopify-expert/)                               | Shopify themes, Liquid, Storefront API, Hydrogen, apps, checkout extensions, and Functions.            |
| [swift-expert](skills/swift-expert/)                                   | Swift, SwiftUI, UIKit, Combine, async/await, actors, and Apple-platform apps.                          |
| [telegram-mini-apps-specialist](skills/telegram-mini-apps-specialist/) | Telegram Mini Apps, React/Vite, Telegram runtime APIs, TON Connect, and wallet flows.                  |
| [ux](skills/ux/)                                                       | UX/UI design, user flows, wireframes, design systems, prototypes, and accessibility.                   |
| [vue-expert](skills/vue-expert/)                                       | Vue 3, Composition API, Nuxt 3, Pinia, Quasar, PWA, Vite, and TypeScript.                              |
| [vue-expert-js](skills/vue-expert-js/)                                 | Vue 3 with JavaScript-only projects, JSDoc typing, Vite, routing, and state management.                |
| [web-design-guidelines](skills/web-design-guidelines/)                 | UI, UX, and accessibility reviews against web interface best practices.                                |
| [webdesigner-in-medical-area](skills/webdesigner-in-medical-area/)     | Healthcare UX/UI, patient portals, telemedicine, clinic websites, and compliance-aware design.         |
| [wordpress-pro](skills/wordpress-pro/)                                 | WordPress themes, plugins, Gutenberg blocks, WooCommerce, REST API, and performance/security.          |

### Languages, data, and domain-specific engineering

| Skill                                                                    | Use when you need                                                                               |
| ------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------- |
| [cli-developer](skills/cli-developer/)                                   | CLI tools, argument parsing, interactive prompts, progress indicators, and shell completion.    |
| [cpp-pro](skills/cpp-pro/)                                               | Modern C++, templates, CMake, concurrency, SIMD, memory management, and performance.            |
| [database-optimizer](skills/database-optimizer/)                         | PostgreSQL or MySQL query optimization, indexes, execution plans, and lock contention.          |
| [embedded-systems](skills/embedded-systems/)                             | STM32, ESP32, FreeRTOS, bare-metal firmware, interrupts, DMA, and power optimization.           |
| [game-developer](skills/game-developer/)                                 | Unity, Unreal Engine, ECS, physics, multiplayer networking, shaders, and game optimization.     |
| [javascript-pro](skills/javascript-pro/)                                 | JavaScript, ES modules, async flows, Node.js APIs, browser performance, and Web Workers.        |
| [kotlin-specialist](skills/kotlin-specialist/)                           | Kotlin coroutines, Flow, multiplatform development, Compose, Ktor, and DSLs.                    |
| [mongodb-atlas-local](skills/mongodb-atlas-local/)                       | MongoDB Atlas Local, Docker setup, auth-enabled local development, and vector search bootstrap. |
| [mongodb-operator](skills/mongodb-operator/)                             | MongoDB schemas, indexes, query paths, persistence, growth, and operational safeguards.         |
| [nats-jetstream](skills/nats-jetstream/)                                 | NATS JetStream, async Python services, durable subscriptions, retries, and acknowledgments.     |
| [pandas-pro](skills/pandas-pro/)                                         | pandas DataFrame operations, cleaning, joins, aggregation, time series, and performance.        |
| [postgres-pro](skills/postgres-pro/)                                     | PostgreSQL tuning, EXPLAIN analysis, JSONB, extensions, VACUUM, and replication.                |
| [python-dev](skills/python-dev/)                                         | Senior Python backend design, refactoring, typing, validation, async safety, and testing.       |
| [python-pro](skills/python-pro/)                                         | Python 3.14, type hints, async/await, dataclasses, pytest, black, ruff, and mypy.               |
| [rust-engineer](skills/rust-engineer/)                                   | Rust ownership, borrowing, lifetimes, traits, async Rust, Tokio, and performance.               |
| [salesforce-developer](skills/salesforce-developer/)                     | Apex, Lightning Web Components, SOQL, triggers, batch jobs, platform events, and Salesforce DX. |
| [spark-engineer](skills/spark-engineer/)                                 | Apache Spark jobs, DataFrames, Spark SQL, RDDs, shuffle tuning, and structured streaming.       |
| [sql-pro](skills/sql-pro/)                                               | SQL queries, joins, window functions, CTEs, indexing, EXPLAIN plans, and schema design.         |
| [sqlalchemy-alembic-expert](skills/sqlalchemy-alembic-expert/)           | SQLAlchemy and Alembic database models, migrations, sessions, and schema evolution.             |
| [ton-smart-contracts-specialist](skills/ton-smart-contracts-specialist/) | TON smart contracts, Tact, FunC, opcodes, wrappers, and app integration boundaries.             |
| [typescript-pro](skills/typescript-pro/)                                 | Advanced TypeScript types, generics, utility types, type guards, branded types, and tRPC.       |

### AI, LLM, RAG, automation, and agent tooling

| Skill                                                                      | Use when you need                                                                                     |
| -------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| [agent-evals-lab](skills/agent-evals-lab/)                                 | Evaluation suites for LLM agents, RAG flows, tool-using assistants, and regression gates.             |
| [fine-tuning-expert](skills/fine-tuning-expert/)                           | LoRA, QLoRA, PEFT, model fine-tuning, datasets, hyperparameters, and deployment.                      |
| [langfuse](skills/langfuse/)                                               | Langfuse traces, prompts, datasets, scores, sessions, API access, and documentation lookup.           |
| [langfuse-add-model-price](skills/langfuse-add-model-price/)               | Langfuse model pricing updates and related operational maintenance.                                   |
| [langfuse-backend-dev-guidelines](skills/langfuse-backend-dev-guidelines/) | Langfuse backend development conventions and implementation guidance.                                 |
| [langfuse-skill-developer](skills/langfuse-skill-developer/)               | Langfuse-related skill development and maintenance.                                                   |
| [langgraph-agent-runtime](skills/langgraph-agent-runtime/)                 | LangGraph state schemas, node contracts, routing, tool loops, checkpointing, and runtime diagnosis.   |
| [llm-observability-ops](skills/llm-observability-ops/)                     | LLM tracing, prompt observability, tool-call diagnostics, retrieval spans, and release analysis.      |
| [mcp-builder](skills/mcp-builder/)                                         | Building high-quality MCP servers for external APIs and tool integrations.                            |
| [mcp-developer](skills/mcp-developer/)                                     | MCP servers, clients, transports, schemas, tool handlers, resources, and protocol debugging.          |
| [milvus-vector-ops](skills/milvus-vector-ops/)                             | Milvus vector database operations, hybrid search, indexing, schemas, and pymilvus services.           |
| [ml-pipeline](skills/ml-pipeline/)                                         | ML pipelines, MLflow, W&B, Kubeflow, Airflow, feature stores, model registries, and retraining.       |
| [n8n-code-javascript](skills/n8n-code-javascript/)                         | JavaScript code in n8n Code nodes, `$input`, `$json`, `$node`, helpers, and dates.                    |
| [n8n-code-python](skills/n8n-code-python/)                                 | Python code in n8n Code nodes, `_input`, `_json`, `_node`, and standard-library workflows.            |
| [n8n-expression-syntax](skills/n8n-expression-syntax/)                     | n8n expressions, `{{ }}` syntax, `$json`, `$node`, and expression troubleshooting.                    |
| [n8n-mcp-tools-expert](skills/n8n-mcp-tools-expert/)                       | n8n MCP tools, node search, configuration validation, templates, and workflow management.             |
| [n8n-node-configuration](skills/n8n-node-configuration/)                   | n8n node configuration, required fields, dependencies, and common node patterns.                      |
| [n8n-validation-expert](skills/n8n-validation-expert/)                     | n8n validation errors, warnings, operator structure, profiles, and validation loops.                  |
| [n8n-workflow-best-practices](skills/n8n-workflow-best-practices/)         | Reliable n8n workflow architecture, retries, error handling, lineage, scaling, and operations.        |
| [n8n-workflow-patterns](skills/n8n-workflow-patterns/)                     | n8n workflow patterns for webhooks, HTTP APIs, databases, AI agents, and scheduled tasks.             |
| [opencode-expert](skills/opencode-expert/)                                 | OpenCode configuration, agents, permissions, providers, MCP, plugins, and TUI workflows.              |
| [prompt-engineer](skills/prompt-engineer/)                                 | Prompt design, structured output schemas, evaluation rubrics, few-shot examples, and test suites.     |
| [prompt-security-redteam](skills/prompt-security-redteam/)                 | Prompt injection, data exfiltration, unsafe tool execution, RAG attacks, and memory red teaming.      |
| [rag-architect](skills/rag-architect/)                                     | RAG systems, chunking, embeddings, vector stores, hybrid search, reranking, and retrieval evaluation. |
| [telegram-ai-bot-runtime](skills/telegram-ai-bot-runtime/)                 | Telegram bots, async handlers, AI inference, media inputs, payments, queues, and user concurrency.    |
| [tester-ai](skills/tester-ai/)                                             | Testing AI apps, chatbots, RAG systems, tool-using agents, red teaming, and eval governance.          |

### Quality, security, review, and testing

| Skill                                                                                | Use when you need                                                                                   |
| ------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------- |
| [chaos-engineer](skills/chaos-engineer/)                                             | Chaos experiments, failure injection, blast-radius control, game days, and resilience testing.      |
| [code-review](skills/code-review/)                                                   | Comprehensive code reviews against requirements, quality, security, and maintainability standards.  |
| [code-reviewer](skills/code-reviewer/)                                               | Structured PR or code quality review with prioritized findings and actionable recommendations.      |
| [debugging-wizard](skills/debugging-wizard/)                                         | Systematic debugging, stack traces, logs, root-cause analysis, and hypothesis-driven fixes.         |
| [detect-architecture-antipatterns](skills/detect-architecture-antipatterns/)         | Architecture anti-pattern audits and remediation guidance.                                          |
| [detect-code-development-antipatterns](skills/detect-code-development-antipatterns/) | Code-level anti-pattern audits across frontend, backend, databases, testing, and DevOps.            |
| [playwright-expert](skills/playwright-expert/)                                       | Playwright E2E tests, fixtures, page objects, reporters, CI, mocking, and visual testing.           |
| [playwright-skill](skills/playwright-skill/)                                         | Browser automation, web app testing, screenshots, forms, responsive checks, and UX validation.      |
| [secure-code-guardian](skills/secure-code-guardian/)                                 | Authentication, authorization, input validation, encryption, OWASP prevention, and secure sessions. |
| [security](skills/security/)                                                         | Security architecture, threat modeling, compliance, infrastructure security, and incident planning. |
| [security-reviewer](skills/security-reviewer/)                                       | Security audits, vulnerability reports, dependency checks, secrets scanning, SAST, and remediation. |
| [test-master](skills/test-master/)                                                   | Unit, integration, E2E, regression, performance, security testing, coverage, and test strategy.     |
| [webapp-testing](skills/webapp-testing/)                                             | Local web application testing with Playwright, screenshots, browser logs, and UI validation.        |

### Documentation, research, education, product, and marketing

| Skill                                                                      | Use when you need                                                                                |
| -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| [ai-seo](skills/ai-seo/)                                                   | AI search visibility, AI Overviews, Perplexity citations, generative search, and LLM visibility. |
| [code-documenter](skills/code-documenter/)                                 | Docstrings, OpenAPI/Swagger, JSDoc, documentation sites, tutorials, and user guides.             |
| [competitive-ads-extractor](skills/competitive-ads-extractor/)             | Competitor ad extraction and analysis from ad libraries.                                         |
| [content-research-writer](skills/content-research-writer/)                 | Research-backed content, outlines, citations, hooks, and section-level writing support.          |
| [digital-advertizer](skills/digital-advertizer/)                           | Google Ads, Yandex Direct, AdSense, campaign structure, keywords, creatives, and tracking plans. |
| [feature-forge](skills/feature-forge/)                                     | Feature specs, requirements workshops, user stories, EARS requirements, and acceptance criteria. |
| [geo-marketologist](skills/geo-marketologist/)                             | Generative engine optimization strategy for AI search visibility and citations.                  |
| [humanizer](skills/humanizer/)                                             | Editing AI-generated writing to sound more natural and human-written.                            |
| [lead-research-assistant](skills/lead-research-assistant/)                 | Lead research, target company discovery, and contact strategy.                                   |
| [lecture-materials-improver](skills/lecture-materials-improver/)           | Improving existing teaching materials for clarity, pacing, engagement, and teachability.         |
| [lecture-pack-generator](skills/lecture-pack-generator/)                   | Complete teachable session packages, slide outlines, activities, checks, and handouts.           |
| [medical-marketologist](skills/medical-marketologist/)                     | Compliant medical marketing strategy, patient journeys, trust UX, CRO, and ads-safe messaging.   |
| [practice-materials-generator](skills/practice-materials-generator/)       | Quizzes, problems, concept checks, mini-cases, practice materials, and answer keys.              |
| [product-owner](skills/product-owner/)                                     | Product strategy, backlog management, prioritization, user stories, roadmaps, and OKRs.          |
| [sci-editor](skills/sci-editor/)                                           | Academic manuscript editing for clarity, logic, hedging, structure, and publication readiness.   |
| [sci-literature-reviewer](skills/sci-literature-reviewer/)                 | Doctoral-style literature reviews from provided sources with non-hallucinated citations.         |
| [sci-writer](skills/sci-writer/)                                           | Research manuscript drafting, IMRaD structure, gap framing, contribution framing, and hedging.   |
| [semester-module-planner](skills/semester-module-planner/)                 | Multi-week modules, syllabi, learning arcs, activities, homework, and assessment checkpoints.    |
| [skill-creator](skills/skill-creator/)                                     | Creating or updating skills with specialized knowledge, workflows, or tool integrations.         |
| [slide-writer-teaching](skills/slide-writer-teaching/)                     | Production-ready slide text, presenter notes, timing guidance, and visual suggestions.           |
| [spec-miner](skills/spec-miner/)                                           | Reverse engineering legacy or undocumented codebases into specs and architecture documentation.  |
| [technical](skills/technical/)                                             | Technical architecture guidance for full-stack applications and implementation decisions.        |
| [techwriter](skills/techwriter/)                                           | Technical documentation, guides, API references, tutorials, release notes, and changelogs.       |
| [the-fool](skills/the-fool/)                                               | Devil's advocate reviews, pre-mortems, red-team critiques, and assumption audits.                |
| [vercel-deploy](skills/vercel-deploy/)                                     | Deploying applications and websites to Vercel.                                                   |
| [vercel-react-best-practices](skills/vercel-react-best-practices/)         | React and Next.js performance best practices from Vercel Engineering.                            |
| [working-lecture-notes-generator](skills/working-lecture-notes-generator/) | Teacher-facing lecture scripts, speaking flow, board plans, timing, and fallback options.        |

---

## Research and Review Documents

The repository already includes several substantial knowledge documents.

### Research

- [docs/research/software-architecture-antipatterns-report.md](docs/research/software-architecture-antipatterns-report.md) — a detailed report on architecture anti-patterns, their causes, and refactoring strategies.
- [docs/research/code-level-antipatterns-report.md](docs/research/code-level-antipatterns-report.md) — a broad survey of code-level anti-patterns across frontend, backend, databases, testing, and DevOps.

### Reviews

- [docs/reviews/test-master-sdd-gap-analysis.md](docs/reviews/test-master-sdd-gap-analysis.md) — a review of the `test-master` skill against a spec-driven development testing approach.

These documents are useful as supporting material when evolving skills, rules, and workflow standards.

---

## Configuration Files

### [.kilocodemodes](.kilocodemodes)

Defines custom modes such as:

- epic planning;
- feature specification;
- development planning;
- test planning;
- implementation;
- testing;
- technical documentation;
- architecture documentation;
- markdown linting and fix workflows.

This file is the main registry for how the agent environment exposes workflow-specific operating modes.

### [package.json](package.json)

The repository currently has a minimal package manifest and depends on [`@kilocode/plugin`](package.json).

This indicates that the repository is centered on KiloCode-based workflow tooling rather than a traditional application runtime.

### [bun.lock](bun.lock)

Lockfile for the package manager state.

---

## Getting Started

### 1. Read the conceptual overview

Start with [workflows/.ai/full-project.md](workflows/.ai/full-project.md) to understand the intended lifecycle.

### 2. Review the quick-start materials

Use the following onboarding files:

- [workflows/.ai/examples/QuickStartGuide.md](workflows/.ai/examples/QuickStartGuide.md)
- [workflows/.ai/examples/QuickStartChecklist.md](workflows/.ai/examples/QuickStartChecklist.md)
- [workflows/.ai/examples/FAQ.md](workflows/.ai/examples/FAQ.md)

### 3. Choose the right workflow path

Use:

- epic-first flow for large, multi-stage initiatives;
- direct feature flow for smaller, self-contained work.

### 4. Use the matching mode or command per stage

Mode definitions are listed in [.kilocodemodes](.kilocodemodes), and command guides live in [workflows/.ai/commands/](workflows/.ai/commands/).

---

## Typical Usage Paths

### Path A: Large initiative

Use this path when work must be split into stages.

1. Create the epic.
2. Create a feature spec for a stage.
3. Create the summary technical plan.
4. Create development and test plans for each task.
5. Implement code and tests.
6. Write technical and architecture documentation.

Primary references:

- [workflows/.ai/commands/ra-create-epic.md](workflows/.ai/commands/ra-create-epic.md)
- [workflows/.ai/commands/ra-create-feature.md](workflows/.ai/commands/ra-create-feature.md)
- [workflows/.ai/commands/ra-create-summary-plan.md](workflows/.ai/commands/ra-create-summary-plan.md)
- [workflows/.ai/commands/ra-create-dev-plan.md](workflows/.ai/commands/ra-create-dev-plan.md)
- [workflows/.ai/commands/ra-create-test-plan.md](workflows/.ai/commands/ra-create-test-plan.md)
- [workflows/.ai/commands/ra-php-implementation.md](workflows/.ai/commands/ra-php-implementation.md)
- [workflows/.ai/commands/ra-php-test-implementation.md](workflows/.ai/commands/ra-php-test-implementation.md)
- [workflows/.ai/commands/ra-create-tech-doc.md](workflows/.ai/commands/ra-create-tech-doc.md)
- [workflows/.ai/commands/ra-create-arch-doc.md](workflows/.ai/commands/ra-create-arch-doc.md)

### Path B: Small feature

Use this path when the work does not need epic decomposition.

1. Create the feature spec directly.
2. Create the summary technical plan.
3. Continue with task plans, implementation, testing, and documentation.

A practical example of both paths is documented in [workflows/.ai/examples/QuickStartGuide.md](workflows/.ai/examples/QuickStartGuide.md).

---

## Notes and Conventions

- Most repository guidance is written in Russian, even though many skill names and technical terms remain in English.
- The repository is documentation-heavy by design; many important behaviors are encoded in Markdown instructions rather than executable application code.
- The visible dependency footprint is intentionally small because the main value of the repository is process definition, agent instruction, and reusable documentation assets.
- Large local data directories such as `lancedb/` may appear in the workspace, but they are not part of the primary onboarding path for understanding the repository structure.

---

## Recommended Reading Order

For a complete orientation, read these files in sequence:

1. [README.md](README.md)
2. [workflows/.ai/full-project.md](workflows/.ai/full-project.md)
3. [workflows/.ai/examples/README.md](workflows/.ai/examples/README.md)
4. [workflows/.ai/examples/QuickStartGuide.md](workflows/.ai/examples/QuickStartGuide.md)
5. [.kilocodemodes](.kilocodemodes)
6. [docs/research/software-architecture-antipatterns-report.md](docs/research/software-architecture-antipatterns-report.md)
7. [docs/research/code-level-antipatterns-report.md](docs/research/code-level-antipatterns-report.md)

This sequence provides context first, usage second, and deeper quality guidance last.
