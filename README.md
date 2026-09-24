# Skill Superset: Meta-Skill Discovery

**In the `metaskills` branch, ordinary skill discovery exposes only meta-skills.** Each is an ordinary Agent Skill with standard `SKILL.md`, `name` and `description`. No agent-time scripts, MCP server, embedding API, or special loader is needed.

## How a simple agent navigates

**Path base is the containing file.** This root README correctly uses `atomic-skills/`. From any `skills/meta-*/SKILL.md`, use `../../atomic-skills/`; from its `references/members.md` (or the specialist `references/legacy-names.md`), use `../../../atomic-skills/`. Search/open each file relative to its own directory, even if the agent's initial skill search is restricted to `skills/`.

1. Search only `skills/` and read a relevant `skills/meta-*/SKILL.md`.
2. Decompose the request and search/read that meta-skill's static `references/members.md`.
3. Read the selected `atomic-skills/<original-id>/SKILL.md` with normal file reading. Repeat for distinct subtasks; do not bulk-load atomic skills.

**Get full skill details with ordinary file-search tools.** A meta-skill's `references/members.md` is an index, not the instructions. **Use the existing file-search tool on the exact path** given for the chosen child (for example, `atomic-skills/react-expert/SKILL.md`), then open/read the entire matching file. If exact-file filtering is unavailable, search the parent directory of that path for `SKILL.md` and open the exact match; an existing direct file-read tool also works. If the chosen `SKILL.md` points to `references/` or other documentation, search/read only those files under the chosen child's directory. Do not substitute a search snippet or catalog summary for the full skill body, and do not run scripts or MCP for skill discovery. Repeat this file-search step for each additional subtask; broad first-level discovery remains restricted to `skills/`.


For a request naming a particular original skill, use [the exact-name registry](skills/meta-specialist-catalog/references/legacy-names.md), or read the known `atomic-skills/<original-id>/SKILL.md` directly. The registry contains all original skills and exact paths.

**Configure initial skill discovery to scan `skills/`, not the repository root.** A repository-global `**/SKILL.md` search also sees atomic files; visibility applies to the configured skill root, not unrestricted code search.

## First-level meta-skills

- [`meta-agent-systems`](skills/meta-agent-systems/SKILL.md) — LLM agents, routing, memory and context.
- [`meta-software-architecture`](skills/meta-software-architecture/SKILL.md) — software architecture, code and refactoring.
- [`meta-frontend-web`](skills/meta-frontend-web/SKILL.md) — React, Vue, Angular and web UI.
- [`meta-backend-services`](skills/meta-backend-services/SKILL.md) — backend APIs, data stores and services.
- [`meta-mobile-desktop`](skills/meta-mobile-desktop/SKILL.md) — iOS, Android, Flutter and desktop apps.
- [`meta-devops-cloud`](skills/meta-devops-cloud/SKILL.md) — CI/CD, cloud deployment and observability.
- [`meta-security-compliance`](skills/meta-security-compliance/SKILL.md) — security, authorization and compliance.
- [`meta-testing-quality`](skills/meta-testing-quality/SKILL.md) — testing, QA, agent evals and debugging.
- [`meta-data-analytics`](skills/meta-data-analytics/SKILL.md) — data analytics, SQL and dashboards.
- [`meta-machine-learning`](skills/meta-machine-learning/SKILL.md) — machine learning and embeddings.
- [`meta-genomics-omics`](skills/meta-genomics-omics/SKILL.md) — genomics, NGS and transcriptomics.
- [`meta-molecular-discovery`](skills/meta-molecular-discovery/SKILL.md) — protein structures and molecular design.
- [`meta-clinical-health`](skills/meta-clinical-health/SKILL.md) — clinical and medical research.
- [`meta-research-knowledge`](skills/meta-research-knowledge/SKILL.md) — literature, citations and evidence synthesis.
- [`meta-visual-design`](skills/meta-visual-design/SKILL.md) — Figma, UX, images and accessibility.
- [`meta-media-production`](skills/meta-media-production/SKILL.md) — video, audio, writing and media creation.
- [`meta-marketing-growth`](skills/meta-marketing-growth/SKILL.md) — SEO, marketing and growth.
- [`meta-product-business`](skills/meta-product-business/SKILL.md) — product management, specifications and operations.
- [`meta-finance-payments`](skills/meta-finance-payments/SKILL.md) — payments, budgeting and finance.
- [`meta-office-documents`](skills/meta-office-documents/SKILL.md) — PDF, Word, spreadsheets and slides.
- [`meta-workplace-integrations`](skills/meta-workplace-integrations/SKILL.md) — Google, Slack, Notion and workplace apps.
- [`meta-customer-communications`](skills/meta-customer-communications/SKILL.md) — Twilio, Zoom, voice, email and messaging.
- [`meta-commerce-platforms`](skills/meta-commerce-platforms/SKILL.md) — Shopify, ecommerce and checkout.
- [`meta-browser-automation`](skills/meta-browser-automation/SKILL.md) — browser navigation, testing and scraping.
- [`meta-web3-blockchain`](skills/meta-web3-blockchain/SKILL.md) — TON, smart contracts and Web3.
- [`meta-specialist-catalog`](skills/meta-specialist-catalog/SKILL.md) — rare domains and exact lookup of an original skill.

## Compatibility and maintenance

All original atomic skill bodies and bundled resources are preserved under `atomic-skills/`; their internal relative references remain valid. Old hardcoded `skills/<original-id>/...` file paths become `atomic-skills/<original-id>/...`. Preserving old paths while hiding them from directory scanners is not possible.

Read [the architecture and limitations](docs/metaskills.md) or [the archived workflow guide](README.legacy.md). Catalog generation and validation are maintainer/CI activities, never part of the agent's search workflow.
