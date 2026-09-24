---
name: prd-developer
description: This skill should be used when drafting, reviewing, restructuring, or quality-checking Product Requirements Documents (PRDs) for software development initiatives, especially when the work requires clear product-level problem framing, explicit scope and out-of-scope boundaries, user/persona context, measurable success metrics, release criteria, design/engineering handoff clarity, and—when applicable—AI/LLM feature requirements such as evaluation, guardrails, observability, and human-in-the-loop flows.
license: MIT
metadata:
  author: Builder AI
  version: "1.0.0"
  domain: product-management
  triggers: PRD, product requirements document, product requirements, feature brief, product spec, scope definition, user stories, release criteria, product handoff, AI product requirements
  role: specialist
  scope: design
  output-format: document
  related-skills: product-owner, feature-forge, techwriter, brd-developer
---

# PRD Developer

Produce high-quality Product Requirements Documents for software development work.

## Purpose

Transform validated business and user needs into a structured, reviewable, and handoff-ready PRD that defines product behavior, scope, priorities, UX expectations, assumptions, risks, success metrics, and release intent without collapsing into low-level implementation detail.

Base the work on the principles synthesized in [`docs/research/prd-best-practices-for-software-development.md`](../../docs/research/prd-best-practices-for-software-development.md).

## Use this skill when

Use this skill when the task requires any of the following:

- Draft a PRD from scratch for a product, feature, workflow, or release.
- Convert discovery notes, stakeholder input, research findings, or a BRD into a PRD.
- Review an existing PRD for ambiguity, scope drift, weak metrics, or poor handoff quality.
- Clarify product behavior before design and engineering execution.
- Separate product requirements from business-only artifacts, technical specifications, or backlog items.
- Prepare a product-facing requirements artifact for downstream design specs, epics, user stories, acceptance criteria, or implementation plans.
- Define AI/LLM feature requirements including evaluation, guardrails, observability, and fallback logic.

## Do not use this skill when

Do not use this skill for the following primary tasks:

- Write a BRD focused mainly on organizational rationale and business governance; use [`brd-developer`](../brd-developer/SKILL.md) instead.
- Write a low-level SRS or implementation specification as the main deliverable.
- Produce only backlog tickets, story maps, or sprint-ready items with no product-level framing.
- Invent user research, KPI baselines, design approvals, release decisions, or AI safety guarantees.

## Related Skills

- Use [`brd-developer`](../brd-developer/SKILL.md) when the work is still centered on business-level rationale, governance, and organizational outcomes.
- Use [`trd-developer`](../trd-developer/SKILL.md) when the product requirements need to be translated into technically actionable requirements such as interfaces, data contracts, NFRs, and verification logic.
- Use [`architecture-designer`](../architecture-designer/SKILL.md) when architectural decision-making and structural trade-offs become the main deliverable.
- Use [`product-owner`](../product-owner/SKILL.md) when product strategy, prioritization, roadmap planning, or discovery leadership is broader than PRD authoring alone.

## Core operating principles

Apply these principles in every PRD workflow:

1. Start with the user problem and product objective.
2. Keep the document at product level, not business-only or implementation-only level.
3. Make scope and out-of-scope explicit.
4. Tie each major requirement to user value and measurable success.
5. Treat assumptions as first-class elements.
6. Support design and engineering handoff directly.
7. Define release or launch criteria.
8. Maintain the PRD as a living alignment artifact.
9. For AI features, include evaluation, guardrails, observability, and human oversight where relevant.

## Required inputs

Collect or infer the following inputs before producing a final PRD:

- product context and problem statement;
- target users, personas, or segments;
- business and product goals;
- current pain points, workflow context, or user journey;
- in-scope and out-of-scope boundaries;
- assumptions and constraints;
- dependencies and risks;
- success metrics and, if available, baselines/targets;
- design/UX references or expected experience outcomes;
- release intent or launch constraints;
- expected downstream artifacts such as design specs, epics, stories, or SRS sections;
- for AI features, evaluation strategy and guardrail expectations.

If critical inputs are missing, stop and produce an explicit open-questions list before finalizing the PRD.

## Workflow

Follow this workflow in order.

### 1. Calibrate the artifact boundary

Determine whether the request truly needs a PRD.

Check for these signals:

- Need to explain why the organization should change -> BRD
- Need to define what product behavior should be built -> PRD
- Need detailed system behavior and technical qualities -> SRS
- Need implementable delivery increments -> backlog items or stories

If the request mixes artifact types, separate them clearly and keep the PRD at product granularity.

### 2. Frame the user problem and product objective

Document:

- user or market problem;
- why it matters now;
- expected product outcome;
- user or business impact;
- consequences of not solving it.

Prefer evidence-backed statements where available.

### 3. Identify users, use cases, and journeys

Capture at minimum:

- primary user segments or personas;
- their goals and pain points;
- primary use cases or jobs to be done;
- critical journey steps or workflows affected by the feature.

If personas are unknown, describe user groups functionally and mark missing research as an assumption or validation gap.

### 4. Define scope boundaries

Write scope visibly and explicitly.

Always include:

- in scope;
- out of scope;
- assumptions;
- constraints;
- dependencies.

If scope is unstable, mark it as provisional and identify the decisions needed to stabilize it.

### 5. Draft product requirements at the correct level

Describe what the product should do in terms of user-facing behavior, experience, and product constraints.

Include where relevant:

- feature behavior;
- core workflows;
- edge cases visible to users;
- business rules that shape product behavior;
- non-functional expectations at product level.

Do not over-specify technical implementation unless the detail is necessary to avoid product ambiguity.

### 6. Tie requirements to value and metrics

For each major requirement or feature area, attempt to capture:

- intended user value;
- success metric or KPI;
- baseline if known;
- target if known;
- owner or measurement context;
- release condition if applicable.

If metrics are unavailable, record the absence explicitly and propose a validation method instead of inventing numbers.

### 7. Support design and engineering handoff

Include the minimum scaffolding needed for multidisciplinary execution:

- user stories or core scenarios;
- UX notes, flows, or interaction expectations;
- dependency notes;
- unresolved questions;
- links or placeholders for design specs, prototypes, or engineering follow-ons.

### 8. Define release criteria

State what must be true before shipping.

Release criteria may include:

- required functionality complete;
- dependency readiness;
- metric or quality thresholds;
- operational readiness;
- stakeholder sign-off expectations;
- documentation or enablement tasks.

### 9. Extend the PRD for AI/LLM features when applicable

If the product includes AI/LLM behavior, add these sections as needed:

- expected model behavior;
- evaluation strategy;
- safety and guardrails;
- observability and runtime monitoring;
- human-in-the-loop or fallback logic.

Treat these as product requirements, not optional technical afterthoughts.

### 10. Run the PRD quality gate

Review the document section by section.

Check whether the PRD is:

- clear about the problem being solved;
- grounded in user value;
- explicit about scope and out-of-scope;
- measurable where appropriate;
- ready for design/engineering handoff;
- not overloaded with low-level implementation detail;
- explicit about assumptions and unknowns;
- release-aware;
- for AI features, explicit about evaluation and guardrails.

### 11. Produce the final package

Generate all relevant output sections:

- PRD draft;
- assumptions register;
- open questions log;
- handoff notes for design and engineering;
- release readiness checklist;
- for AI features, evaluation and guardrails appendix.

## Output structure

Unless the user requests another format, produce PRDs using this structure:

1. Title and change history
2. Overview / product context
3. Problem statement
4. Goals and success metrics
5. Personas or user segments
6. User stories / primary use cases
7. Scope
   - In scope
   - Out of scope
8. Assumptions and dependencies
9. Product requirements / feature behavior
10. UX / design considerations
11. Non-functional expectations at product level
12. Risks and trade-offs
13. Release criteria / launch considerations
14. Open questions
15. Links to downstream artifacts

For AI/LLM products, append as needed: 16. Expected model behavior 17. Evaluation strategy 18. Safety and guardrails 19. Observability and runtime feedback loops 20. Human-in-the-loop / fallback logic

## Review heuristics

Flag the PRD if any of the following appear:

- features listed with no user problem or product objective;
- no explicit out-of-scope section;
- no assumptions listed;
- success metrics missing or purely aspirational;
- product behavior described too vaguely for design or engineering handoff;
- detailed technical design replacing product intent;
- no release criteria;
- no open questions despite clear uncertainty;
- for AI features, no evaluation plan, no guardrails, or no observability expectations.

## Anti-hallucination rules

Apply these rules strictly:

- Do not invent user evidence.
- Do not invent KPI baselines or targets.
- Do not invent design sign-off.
- Do not invent engineering feasibility claims.
- Do not invent launch readiness or approval decisions.
- Do not invent AI quality thresholds, model guarantees, or safety claims.
- Mark unknowns as `Assumption`, `Open Question`, or `Needs Validation`.

## Suggested deliverable variants

Select the most appropriate variant based on user need:

- **Full PRD**: For cross-functional features, releases, or new product areas.
- **Lean PRD**: For smaller features that still need product/design/engineering alignment.
- **PRD Review Report**: For auditing an existing PRD.
- **PRD-to-Execution Handoff Pack**: For moving from product definition into design specs, stories, and engineering planning.
- **AI Feature PRD**: For LLM, copilot, RAG, or agentic workflows requiring evaluation and safety sections.

## Collaboration notes

When paired with other skills:

- Use [`product-owner`](../product-owner/SKILL.md) when prioritization, roadmap strategy, or product discovery is the main concern.
- Use [`feature-forge`](../feature-forge/SKILL.md) when the PRD must be decomposed into structured feature specs, acceptance criteria, or implementation checklists.
- Use [`brd-developer`](../brd-developer/SKILL.md) when the work is still at business-justification and governance level.
- Use [`techwriter`](../techwriter/SKILL.md) when the main task is documentation polish instead of requirements design.

## Minimal response pattern

When producing a PRD, structure the work in this order:

1. State artifact type and scope.
2. List critical missing inputs if any.
3. Draft the PRD with explicit sections.
4. Append assumptions and open questions.
5. Append handoff and release-readiness notes.
6. For AI features, append evaluation and guardrails notes.

## Success criteria for using this skill

A successful use of this skill results in a PRD that:

- explains the user problem and product objective clearly;
- stays at product granularity;
- defines scope and out-of-scope explicitly;
- links major requirements to user value and measurable outcomes;
- supports design and engineering handoff;
- defines release-readiness logic;
- handles uncertainty explicitly;
- for AI features, includes evaluation, safety, observability, and fallback considerations where needed.
