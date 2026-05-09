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
8. [Research and Review Documents](#research-and-review-documents)
9. [Configuration Files](#configuration-files)
10. [Getting Started](#getting-started)
11. [Typical Usage Paths](#typical-usage-paths)
12. [Notes and Conventions](#notes-and-conventions)

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
