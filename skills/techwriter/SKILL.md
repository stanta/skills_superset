---
name: techwriter
description:  Write and maintain technical documentation (guides, API references, tutorials, release notes)  with clear structure, accurate details, and a reader-focused style.
allowed-tools:
- Read
- Edit
- Browser
- MCP
---

# TechWriter

Use this skill to produce clear, accurate technical documentation that readers can follow without guesswork.

## Use this skill when

- Author documentation for software features, user manuals, developer guides, installation steps, and FAQs.
- Maintain and refactor existing documentation for clarity, correctness, and consistency.
- Create or update API documentation (endpoints, parameters, authentication, error codes, examples).
- Draft technical tutorials, case studies, post-mortems, and other “tech stories”.
- Write release notes, changelogs, and summaries of code changes.

## Do not use this skill when

- Implement or change product behavior (unless the task is explicitly documentation-only).
- Make architecture decisions without requirements (unless the task is to document an agreed design).

## Workflow (apply in order)

1. Identify the audience, their baseline knowledge, and the primary task the document must enable.
2. Define scope and success criteria (what the document covers and what it does not cover).
3. Collect sources of truth (code, configuration, tickets, SME notes, existing docs) and reconcile conflicts.
4. Choose the appropriate document type:
   - Guide (task-first)
   - Tutorial (learning-first)
   - Reference (lookup-first)
   - Release notes (change-first)
5. Outline first; keep headings descriptive and scannable.
6. Draft with clarity and concision:
   - Prefer active voice.
   - Define terms on first use.
   - Avoid unexplained jargon.
7. Add examples:
   - Commands, code snippets, config fragments.
   - Expected outputs.
   - Common errors and how to fix them.
8. Validate accuracy:
   - Walk through steps mentally or by pseudo-testing.
   - Re-check names, flags, parameters, and defaults.
9. Enforce consistency:
   - Use consistent terminology.
   - Use consistent formatting for code blocks, notes, and warnings.
10. Review and refine:
   - Remove ambiguity.
   - Fix grammar and typos.
   - Ensure the document is complete and self-contained for the target audience.

## Templates and checklists

Load the detailed checklist when drafting or reviewing documentation:

- [`references/techwriter-checklist.md`](references/techwriter-checklist.md:1)
