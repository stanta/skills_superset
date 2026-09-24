---
name: trd-developer
description: This skill should be used when drafting, reviewing, restructuring, or quality-checking Technical Requirements Documents (TRDs) for software delivery initiatives, especially when the work requires technically actionable requirements, architecture and interface constraints, data contracts, non-functional requirements, validation criteria, and—when applicable—AI/LLM system requirements such as prompt/tool boundaries, evaluation, observability, guardrails, and fallback behavior.
license: MIT
metadata:
  author: Builder AI
  version: "1.0.0"
  domain: technical-requirements
  triggers: TRD, technical requirements document, technical specification, engineering spec, system requirements, interface requirements, non-functional requirements, API contract, technical handoff, AI technical requirements
  role: specialist
  scope: design
  output-format: document
  related-skills: technical, api-designer, architecture-designer, prd-developer, techwriter
---

# TRD Developer

Produce high-quality Technical Requirements Documents for software delivery work.

## Purpose

Transform product or business intent into a structured, technically actionable, reviewable, and validation-ready TRD that defines technical behavior, interfaces, constraints, data expectations, non-functional requirements, and operational requirements without collapsing into source code or low-level implementation instructions.

Base the work on the principles synthesized in [`docs/research/trd-best-practices-for-software-development.md`](../../docs/research/trd-best-practices-for-software-development.md).

## Use this skill when

Use this skill when the task requires any of the following:

- Draft a TRD from scratch for a system, subsystem, service, integration, workflow, or technical delivery scope.
- Convert a [`PRD`](../prd-developer/SKILL.md), BRD, architecture notes, or engineering discussion into technical requirements.
- Review an existing TRD, technical specification, or SRS-like artifact for ambiguity, missing constraints, weak interfaces, or poor validation logic.
- Specify functional technical requirements, non-functional requirements, interfaces, data contracts, and dependencies before implementation.
- Create a technical handoff artifact between product intent and engineering delivery.
- Define AI/LLM system requirements such as model/runtime boundaries, evaluation logic, observability, guardrails, or fallback behavior.

## Do not use this skill when

Do not use this skill for the following primary tasks:

- Write a business-facing artifact centered on organizational rationale; use [`brd-developer`](../brd-developer/SKILL.md).
- Write a product-facing artifact centered on user problem framing and release intent; use [`prd-developer`](../prd-developer/SKILL.md).
- Produce a full architecture decision record or architecture review as the main deliverable; use [`architecture-designer`](../architecture-designer/SKILL.md) when structural decision-making is primary.
- Write code, configuration, or implementation tickets as the main deliverable.
- Invent technical constraints, throughput numbers, latency targets, integration details, or safety guarantees without grounding.

## Related Skills

- Use [`brd-developer`](../brd-developer/SKILL.md) when the work is still at business-requirements and stakeholder-governance level.
- Use [`prd-developer`](../prd-developer/SKILL.md) when the work is still at product-behavior, user-value, and release-intent level.
- Use [`architecture-designer`](../architecture-designer/SKILL.md) when structural solution decisions, ADRs, and architecture trade-offs are primary.
- Use [`product-owner`](../product-owner/SKILL.md) when roadmap, prioritization, or product strategy decisions are broader than technical requirement specification.

## Core operating principles

Apply these principles in every TRD workflow:

1. Position the TRD between product intent and implementation.
2. State technical scope and technical out-of-scope explicitly.
3. Separate technical requirement classes clearly.
4. Treat interfaces and contracts as first-class requirements.
5. Elevate non-functional requirements to first-class status.
6. Specify data requirements and validation constraints explicitly.
7. Include verifiable validation and acceptance logic.
8. Keep the TRD versioned and evolvable.
9. For AI systems, include evaluation, guardrails, observability, and fallback logic where relevant.

## Required inputs

Collect or infer the following inputs before producing a final TRD:

- system or product context;
- technical scope boundaries;
- architecture assumptions and constraints;
- services, components, or modules in scope;
- interfaces and integrations;
- data contracts, schemas, or validation rules;
- non-functional requirement targets;
- dependencies and third-party constraints;
- error/failure expectations;
- security and compliance expectations;
- verification or acceptance expectations;
- expected downstream artifacts such as API specs, test plans, implementation plans, or design docs;
- for AI systems, evaluation, prompt/tool boundaries, observability, and fallback expectations.

If critical inputs are missing, stop and produce an explicit open-questions list before finalizing the TRD.

## Workflow

Follow this workflow in order.

### 1. Calibrate the artifact boundary

Determine whether the request truly needs a TRD.

Check for these signals:

- Need to explain business rationale -> BRD
- Need to define product/user behavior -> PRD
- Need to define technical behavior, constraints, and interfaces -> TRD
- Need to justify structural decisions and trade-offs -> architecture artifact
- Need to write implementation-ready code/tasks only -> backlog or implementation plan

If the request mixes artifact types, separate them clearly and keep the TRD at technical-requirements level.

### 2. Frame technical context and scope

Document:

- technical system or subsystem in scope;
- operational context;
- upstream and downstream dependencies;
- technical in-scope and out-of-scope boundaries;
- assumptions that affect implementation choices.

State system boundaries explicitly.

### 3. Separate technical requirement classes

Structure requirements into explicit classes.

#### Functional technical requirements

Describe what the system or component must do technically.

#### Non-functional requirements

Describe required performance, availability, scalability, security, maintainability, observability, compliance, and related qualities.

#### External interface requirements

Describe APIs, protocols, consumers, providers, request/response formats, versioning, and failure semantics.

#### Data and contract requirements

Describe entities, schemas, field constraints, validation rules, ownership, lifecycle assumptions, and storage/integration expectations.

#### Constraints and dependencies

Describe external systems, operational limits, technology constraints, and mandatory dependencies.

#### Validation and verification requirements

Describe how major technical requirements will be tested, verified, or accepted.

### 4. Surface architecture assumptions without replacing architecture artifacts

Capture architectural assumptions and constraints required to interpret the requirements correctly.

Examples:

- service boundaries assumed by the TRD;
- deployment topology constraints;
- required consistency or durability model;
- security isolation assumptions;
- integration or protocol limitations.

Do not turn the TRD into a full ADR set unless the user explicitly requests that.

### 5. Specify interfaces as contracts

For every important interface in scope, document:

- purpose;
- producer/consumer;
- protocol or transport;
- inputs/outputs;
- validation constraints;
- versioning expectations;
- error/failure behavior;
- rate, retry, timeout, or idempotency expectations where relevant.

### 6. Elevate NFRs and operational requirements

Document NFRs quantitatively where possible.

Include where relevant:

- latency;
- throughput;
- availability;
- reliability;
- scaling expectations;
- security controls;
- logging and tracing;
- alerting;
- compliance or auditability expectations.

Bind NFRs to specific system surfaces rather than writing only generic system-wide aspirations.

### 7. Add validation and acceptance logic

For each major technical requirement, identify a validation path.

Examples:

- automated test coverage;
- contract validation;
- load or resilience testing;
- security review;
- integration test scenarios;
- acceptance thresholds.

If verification is not yet possible, mark the gap explicitly.

### 8. Extend the TRD for AI/LLM systems when applicable

If the system includes AI/LLM behavior, add these sections as needed:

- model/runtime constraints;
- prompt and tool-use boundaries;
- evaluation and regression logic;
- observability and monitoring;
- safety and guardrails;
- fallback and human override behavior.

Treat these as engineering requirements, not optional commentary.

### 9. Run the TRD quality gate

Review the document section by section.

Check whether the TRD is:

- technically scoped;
- explicit about interfaces;
- explicit about data contracts;
- concrete about NFRs;
- clear about dependencies and constraints;
- verifiable;
- distinct from product or architecture-only artifacts;
- explicit about unknowns;
- for AI systems, explicit about evaluation, guardrails, and observability.

### 10. Produce the final package

Generate all relevant output sections:

- TRD draft;
- interface and dependency register;
- assumptions and open technical questions log;
- verification/acceptance matrix;
- operational readiness notes;
- for AI systems, evaluation and guardrails appendix.

## Output structure

Unless the user requests another format, produce TRDs using this structure:

1. Title and change history
2. Technical context / system overview
3. Purpose and scope
4. Technical in scope / out of scope
5. Architecture assumptions and constraints
6. Functional technical requirements
7. Non-functional requirements
8. External interface requirements
9. Data models / contracts / validation rules
10. Error handling and failure behavior
11. Dependencies and third-party constraints
12. Security and compliance requirements
13. Observability and operational requirements
14. Verification / acceptance criteria
15. Open technical questions
16. Links to related artifacts

For AI/LLM systems, append as needed: 17. Model/runtime constraints 18. Evaluation and validation strategy 19. Prompt/tool boundaries 20. Safety and guardrails 21. Fallback and human override logic

## Review heuristics

Flag the TRD if any of the following appear:

- technical scope is unclear or absent;
- interfaces are mentioned but not specified as contracts;
- NFRs are generic, qualitative, or missing;
- data assumptions are implicit;
- error handling or failure behavior is unspecified;
- requirements are written like implementation tasks instead of technical requirements;
- architecture rationale dominates while requirements remain vague;
- no validation or acceptance logic is present;
- for AI systems, no evaluation plan, no prompt/tool boundaries, no observability requirements, or no guardrails.

## Anti-hallucination rules

Apply these rules strictly:

- Do not invent integration details.
- Do not invent capacity, throughput, or latency targets.
- Do not invent security/compliance guarantees.
- Do not invent architecture decisions that were not provided or justified.
- Do not invent AI safety, evaluation, or performance claims.
- Mark unknowns as `Assumption`, `Open Technical Question`, or `Needs Validation`.

## Suggested deliverable variants

Select the most appropriate variant based on user need:

- **Full TRD**: For cross-service or system-critical software delivery work.
- **Lean TRD**: For smaller technical scopes that still need explicit constraints and interfaces.
- **TRD Review Report**: For auditing an existing technical requirements artifact.
- **TRD-to-Implementation Handoff Pack**: For moving into API specs, test plans, stories, or engineering plans.
- **AI System TRD**: For copilots, RAG, tool-using agents, orchestration systems, or model-backed workflows.

## Collaboration notes

When paired with other skills:

- Use [`technical`](../technical/SKILL.md) when broader architecture and system design guidance is needed around the TRD.
- Use [`api-designer`](../api-designer/SKILL.md) when interface and API modeling is the main focus.
- Use [`architecture-designer`](../architecture-designer/SKILL.md) when architecture decisions, ADRs, and structural trade-offs are primary.
- Use [`prd-developer`](../prd-developer/SKILL.md) when the work is still at product-behavior level.
- Use [`techwriter`](../techwriter/SKILL.md) when documentation polish is the main need rather than technical requirements analysis.

## Minimal response pattern

When producing a TRD, structure the work in this order:

1. State artifact type and technical scope.
2. List critical missing technical inputs if any.
3. Draft the TRD with explicit technical requirement classes.
4. Append assumptions and open technical questions.
5. Append validation and operational readiness notes.
6. For AI systems, append evaluation and guardrails notes.

## Success criteria for using this skill

A successful use of this skill results in a TRD that:

- clearly defines technical scope and boundaries;
- distinguishes functional, non-functional, interface, and data requirements;
- treats interfaces and contracts as first-class requirements;
- includes validation and acceptance logic;
- is usable by engineering as a reliable technical handoff artifact;
- remains distinct from product-only or architecture-only documents;
- for AI systems, includes evaluation, observability, guardrails, and fallback considerations where needed.
