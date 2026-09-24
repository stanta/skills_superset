# TechWriter checklist

Use this checklist as acceptance criteria for drafting or revising documentation.

## 1) Audience and goal

- [ ] Identify primary audience (beginner / intermediate / expert).
- [ ] Identify audience context (user / operator / developer / contributor).
- [ ] State the document goal in 1 sentence.
- [ ] Define explicit non-goals (what is intentionally not covered).

## 2) Scope and sources of truth

- [ ] List sources of truth (code paths, configs, specs, tickets, SME notes).
- [ ] Resolve contradictions between sources (or call them out explicitly).
- [ ] Confirm versioning context (product version, API version, date, platform).

## 3) Information architecture

- [ ] Choose document type:
  - [ ] Guide (task-first)
  - [ ] Tutorial (learning-first)
  - [ ] Reference (lookup-first)
  - [ ] Release notes (change-first)
- [ ] Use scannable headings that match reader questions.
- [ ] Put prerequisites near the top.
- [ ] Keep each section focused on one job-to-be-done.

## 4) Clarity and concision

- [ ] Prefer short, direct sentences.
- [ ] Prefer active voice.
- [ ] Define new terms on first use.
- [ ] Avoid unnecessary jargon and vague phrases.
- [ ] Remove filler (“in order to”, “it is important to note”).

## 5) Procedural correctness

- [ ] Ensure steps are complete and in the correct order.
- [ ] Include required permissions, environment assumptions, and safety notes.
- [ ] Provide copy/pasteable commands where appropriate.
- [ ] Include expected outputs or verification steps.
- [ ] Document common failure modes and how to recover.

## 6) Examples

- [ ] Provide at least one realistic example for each major feature/operation.
- [ ] Keep examples minimal but complete.
- [ ] Use consistent placeholders and explain them.

## 7) API documentation (if applicable)

- [ ] Document authentication and authorization requirements.
- [ ] Describe endpoints with method + path, purpose, parameters, and responses.
- [ ] Include example requests and responses.
- [ ] Document errors (status codes, error schema, and remediation).

## 8) Consistency and style

- [ ] Use consistent terminology and capitalization.
- [ ] Use consistent formatting for code blocks, filenames, UI labels.
- [ ] Standardize “Note/Warning” patterns.
- [ ] Avoid switching between synonyms for the same concept.

## 9) Final review

- [ ] Remove ambiguity (pronouns without antecedents, unclear references).
- [ ] Proofread for grammar and typos.
- [ ] Confirm the doc is self-contained for the target audience.
- [ ] Confirm the doc meets the stated goal and success criteria.
