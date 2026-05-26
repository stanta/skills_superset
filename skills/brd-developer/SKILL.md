---
name: brd-developer
description: This skill should be used when drafting, reviewing, restructuring, or quality-checking Business Requirements Documents (BRDs) for software development initiatives, especially when the work requires clear separation of business, stakeholder, solution, and transition requirements; explicit scope boundaries; measurable success metrics; stakeholder governance; and traceability into downstream artifacts such as PRDs, SRS documents, epics, user stories, and acceptance criteria.
license: MIT
metadata:
  author: Builder AI
  version: "1.0.0"
  domain: business-analysis
  triggers: BRD, business requirements document, business requirements, requirements discovery, scope definition, stakeholder mapping, traceability, business analysis
  role: specialist
  scope: design
  output-format: document
  related-skills: feature-forge, product-owner, techwriter, spec-miner
---

# BRD Developer

Produce high-quality Business Requirements Documents for software development work.

## Purpose

Transform incomplete business context into a structured, reviewable, and traceable BRD that captures the business need, expected outcomes, scope boundaries, stakeholder interests, constraints, and requirement layers without collapsing too early into implementation detail.

Base the work on the principles synthesized in [`docs/research/brd-best-practices-for-software-development.md`](../../docs/research/brd-best-practices-for-software-development.md).

## Use this skill when

Use this skill when the task requires any of the following:

- Draft a BRD from scratch for a software initiative.
- Convert scattered notes, meeting summaries, discovery output, or stakeholder input into a BRD.
- Review an existing BRD for completeness, ambiguity, traceability, and artifact-boundary problems.
- Distinguish BRD content from PRD, SRS, backlog, or architecture content.
- Prepare a business-facing requirements artifact before product or engineering decomposition.
- Build a requirements foundation for downstream artifacts such as PRDs, SRS documents, epics, user stories, acceptance criteria, or test plans.

## Do not use this skill when

Do not use this skill for the following primary tasks:

- Write detailed implementation specifications only; use a more solution-oriented requirements skill instead.
- Design architecture or APIs without a business-analysis objective.
- Replace user stories, PRDs, or SRS documents when the task explicitly requires those artifacts.
- Invent missing business facts, approvals, budgets, compliance obligations, or KPIs.

## Related Skills

- Use [`prd-developer`](../prd-developer/SKILL.md) when the work needs to move from business change rationale into product behavior, personas, scope, and release intent.
- Use [`trd-developer`](../trd-developer/SKILL.md) when the work needs to move from business requirements into technically actionable interfaces, constraints, data contracts, NFRs, and validation logic.
- Use [`architecture-designer`](../architecture-designer/SKILL.md) when structural solution decisions and architecture trade-offs become the primary deliverable.
- Use [`product-owner`](../product-owner/SKILL.md) when prioritization, roadmap, discovery strategy, or broader product decision-making is the main concern.

## Core operating principles

Apply these principles in every BRD workflow:

1. Anchor the document in business change, not features.
2. Separate requirement layers explicitly:
   - business requirements,
   - stakeholder requirements,
   - high-level solution capabilities,
   - transition requirements.
3. Make scope visible through in-scope, out-of-scope, dependencies, assumptions, and constraints.
4. Convert vague goals into measurable business outcomes where evidence exists.
5. Preserve solution neutrality while capturing mandatory constraints.
6. Add traceability anchors so the BRD can feed downstream artifacts.
7. Mark unknowns explicitly instead of hallucinating answers.

## Required inputs

Collect or infer the following inputs before producing a final BRD:

- business context or problem statement;
- sponsor, owner, or requesting stakeholder;
- target users or stakeholder groups;
- desired business outcomes and success measures;
- current-state pain points;
- scope boundaries;
- assumptions and constraints;
- dependencies and risks;
- downstream artifact expectations such as PRD, SRS, backlog, RFP, or implementation plan.

If critical inputs are missing, stop and produce an explicit open-questions list before finalizing the BRD.

## Workflow

Follow this workflow in order.

### 1. Calibrate the artifact boundary

Determine whether the user really needs a BRD or another artifact.

Check for these signals:

- Need to explain why the change is needed -> BRD
- Need to define product behavior and feature intent -> PRD
- Need formal system behavior and quality specification -> SRS
- Need implementable delivery increments -> backlog items or stories

If the request mixes artifact types, separate them clearly in the output and keep the BRD at business-analysis level.

### 2. Frame the business change

Document:

- problem or opportunity;
- affected business area;
- why change is needed now;
- expected business impact;
- consequences of not changing.

Prefer plain language over technical jargon.

### 3. Identify stakeholders and governance

Capture at minimum:

- sponsor;
- business owner;
- operational stakeholders;
- user groups;
- approvers;
- consulted technical stakeholders.

For each important stakeholder, capture:

- role,
- interest,
- influence,
- approval or decision rights,
- expected involvement cadence.

### 4. Define scope boundaries

Write scope as a boundary system, not as a vague paragraph.

Always include:

- in scope;
- out of scope;
- assumptions;
- constraints;
- dependencies.

If scope is unstable, mark it as provisional and identify decision points needed to stabilize it.

### 5. Separate requirement layers

Structure requirements into explicit sections.

#### Business requirements

Describe business objectives, policy drivers, operational outcomes, and value expectations.

#### Stakeholder requirements

Describe what stakeholder groups need from the change in order to achieve the business outcomes.

#### High-level solution capability requirements

Describe capabilities the future solution must provide, while avoiding detailed design or implementation specification.

#### Transition requirements

Describe migration, rollout, training, change management, reporting, or cutover needs necessary to move from current state to future state.

### 6. Define measurable outcomes

For each major objective, attempt to capture:

- metric or KPI;
- baseline if known;
- target if known;
- owner;
- measurement window.

If quantitative measurement is unavailable, record the absence explicitly and propose a validation method instead of inventing numbers.

### 7. Add traceability scaffolding

Give each major requirement a stable identifier.

Prepare a seed traceability map linking requirements to downstream artifacts such as:

- PRD sections,
- SRS sections,
- epics,
- stories,
- acceptance criteria,
- test coverage,
- rollout checkpoints.

### 8. Run the BRD quality gate

Review the document requirement by requirement and section by section.

Check whether the BRD is:

- necessary;
- clear;
- complete enough for current stage;
- internally consistent;
- traceable;
- verifiable at outcome level;
- free of premature implementation detail;
- explicit about unknowns and approvals.

### 9. Produce the final package

Generate all relevant output sections:

- BRD draft;
- assumptions register;
- open questions log;
- traceability seed table;
- readiness assessment for downstream artifact creation.

## Output structure

Unless the user requests another format, produce BRDs using this structure:

1. Executive summary
2. Business context / problem statement
3. Objectives and expected outcomes
4. Current state and pain points
5. Scope
   - In scope
   - Out of scope
6. Stakeholders and decision rights
7. Assumptions, constraints, and dependencies
8. Business requirements
9. Stakeholder requirements
10. High-level solution capability requirements
11. Transition requirements
12. Risks and compliance considerations
13. Success metrics / KPIs
14. Traceability notes
15. Approval and change history
16. Open questions

## Review heuristics

Flag the BRD if any of the following appear:

- feature lists without business rationale;
- architecture or UI detail where business requirements should be;
- no out-of-scope section;
- no measurable outcomes or validation approach;
- no named approver or sponsor;
- requirements with words such as “easy,” “fast,” “user-friendly,” or “flexible” without qualification;
- no transition requirements for materially disruptive change;
- no visible path into downstream delivery artifacts.

## Anti-hallucination rules

Apply these rules strictly:

- Do not invent stakeholder approvals.
- Do not invent budget figures.
- Do not invent compliance obligations.
- Do not invent baselines or KPI targets.
- Do not infer system behavior beyond what business context supports.
- Mark unknowns as `Open Question`, `Assumption`, or `Needs Confirmation`.

## Suggested deliverable variants

Select the most appropriate variant based on user need:

- **Full BRD**: For cross-functional or enterprise initiatives.
- **Lean BRD**: For smaller software changes that still require business alignment.
- **BRD Review Report**: For auditing an existing BRD.
- **BRD-to-PRD Handoff Pack**: For moving from business requirements into product definition.

## Collaboration notes

When paired with other skills:

- Use [`feature-forge`](../feature-forge/SKILL.md) when the BRD must be decomposed into feature specifications and acceptance criteria.
- Use [`product-owner`](../product-owner/SKILL.md) when prioritization, roadmap, or product strategy is the main concern.
- Use [`techwriter`](../techwriter/SKILL.md) when the primary need is documentation polish rather than requirements analysis.

## Minimal response pattern

When producing a BRD, structure the work in this order:

1. State artifact type and scope.
2. List critical missing inputs if any.
3. Draft the BRD with explicit requirement layers.
4. Append assumptions and open questions.
5. Append a short readiness assessment for next-step artifacts.

## Success criteria for using this skill

A successful use of this skill results in a BRD that:

- explains the business need clearly;
- separates business intent from solution detail;
- defines scope boundaries explicitly;
- contains measurable outcomes or a credible validation method;
- identifies stakeholder governance;
- supports traceability into downstream delivery artifacts;
- leaves no hidden assumptions unmarked.
