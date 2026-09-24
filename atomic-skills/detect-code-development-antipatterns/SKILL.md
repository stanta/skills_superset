---
name: detect-code-development-antipatterns
description: This skill should be used when auditing a software project for code-level development anti-patterns across frontend, backend, databases, testing, and DevOps/CI/CD. Use when reviewing implementation quality, technical debt hotspots, delivery risks, or maintainability problems and when producing evidence-based findings with prioritized remediation guidance.
license: MIT
allowed-tools: Read, Grep, Glob, Bash
metadata:
  author: Builder AI Team
  version: "1.0.0"
  domain: code-quality-review
  triggers: code anti-patterns, frontend anti-patterns, backend anti-patterns, SQL anti-patterns, testing anti-patterns, CI/CD anti-patterns, technical debt audit, implementation audit, maintainability review
  role: specialist
  scope: review
  output-format: report
  related-skills: code-reviewer, spec-miner, test-master, devops, database-optimizer
---

# Detect Code Development Antipatterns

Audit an existing codebase and delivery setup for recurring implementation anti-patterns. Ground every conclusion in observable evidence from source code, tests, queries, pipeline configuration, and repository conventions. Separate confirmed anti-patterns from weak signals, contextual trade-offs, and style-only concerns.

## When to use

- Review a repository for maintainability, reliability, security, and performance risks.
- Audit frontend, backend, database, test, and delivery code before refactoring or modernization.
- Explain why a codebase is hard to change, flaky in CI, slow in production, or fragile during releases.
- Produce an actionable anti-pattern report with severity, confidence, and remediation sequence.

## Domain catalog

Evaluate all relevant domains in scope. If a domain is absent in the repository, state that explicitly.

| Domain         | Anti-patterns to check                                                                                                           |
| -------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| Frontend       | Props Drilling, Array Index as Key, Inline Styles Overuse, CSS-in-JS Overuse, `useEffect` Overuse, Missing Memoization, Div Soup |
| Backend        | Callback Hell, Unhandled Promise Rejections, Missing Input Validation, God Controller, Chatty API, Error Swallowing              |
| Databases      | N+1 Query Problem, `SELECT *`, EAV, Index Shotgun, No `EXPLAIN`, Spaghetti Query                                                 |
| Testing        | Flaky Tests, Test Coupling, Over-Mocking, Testing Implementation Instead of Behavior                                             |
| DevOps / CI/CD | Manual Steps in Pipeline, Infrequent Commits, No Rollback Strategy, Pipeline Without Observability, Big Bang Release             |

## Core workflow

### 1. Define audit scope

- Identify languages, frameworks, persistence layers, test stack, and pipeline tooling.
- Determine whether the goal is broad audit, incident diagnosis, pre-refactor assessment, or PR-level review.
- Record the quality attributes under review: maintainability, performance, security, reliability, developer experience, or delivery speed.

Validation checkpoint:

- Do not start classification before mapping the repository domains and stack.

### 2. Build an evidence map

- Inspect entry points, routing, component trees, services, repositories, SQL, test directories, and CI configuration.
- Track repeated patterns, duplicated logic, deep nesting, broad modules, fragile tests, and manual delivery steps.
- Collect direct code snippets and file locations for each suspected anti-pattern.

Validation checkpoint:

- If evidence is limited to one isolated file, avoid generalizing to the whole codebase.

### 3. Evaluate anti-pattern hypotheses by domain

For each finding:

1. Name the anti-pattern.
2. Cite direct evidence.
3. Note symptoms and impact.
4. Record counter-evidence or contextual justification.
5. Assign confidence: high, medium, low.
6. Assign severity: critical, major, moderate, minor.

Use these labels precisely:

- Confirmed anti-pattern
- Strong signal, needs broader confirmation
- Weak signal, insufficient evidence
- Acceptable trade-off in current context

### 4. Connect local findings to systemic causes

- Look for repeating causes across domains: poor boundaries, missing automation, over-coupling, premature optimization, fear-driven workarounds.
- Distinguish incidental mess from process-level or architectural drivers.

### 5. Recommend remediation roadmap

- Prioritize high-leverage fixes that reduce future change cost.
- Prefer incremental remediation over rewrite-first guidance.
- Sequence fixes so stabilizers come first: validation, observability, deterministic tests, query analysis, module boundaries.

## Repository exploration patterns

Start with structural exploration and targeted searches.

### General discovery

```bash
# Find manifests, app entry points, and pipeline configs
find . -maxdepth 4 \( -name 'package.json' -o -name 'pyproject.toml' -o -name 'pom.xml' -o -name 'go.mod' -o -name 'Dockerfile' -o -name 'docker-compose*.yml' -o -name '.github' -o -name '.gitlab-ci.yml' -o -name 'Jenkinsfile' \)

# Find debt markers and warning comments
grep -RInE 'TODO|FIXME|HACK|XXX|temporary|workaround|do not touch|legacy' .
```

### Frontend probes

```bash
# Potential props drilling and inline object recreation
grep -RInE 'props\.|useEffect\(|useMemo\(|useCallback\(|key=\{index\}|style=\{\{' src app components

# Excessive wrapper markup
grep -RInE '<div>|<span>' src app components
```

### Backend probes

```bash
# Nested callbacks, empty catches, weak validation
grep -RInE 'catch \(|catch\s*\{|console\.error|process\.on\(|req\.body|req\.query|schema|zod|joi|validator' src app services api

# Large controllers and service bottlenecks
grep -RInE 'Controller|handler|router|service' src app services api
```

### Database probes

```bash
# N+1 and broad query patterns
grep -RInE 'SELECT \*|JOIN|prefetch_related|select_related|findAll|query\(|execute\(' src app services db migrations

# Explain-plan culture and indexing hints
grep -RInE 'EXPLAIN|ANALYZE|INDEX|CREATE INDEX' db migrations sql
```

### Testing probes

```bash
# Retry-heavy or timing-sensitive tests
grep -RInE 'retry|sleep|waitForTimeout|setTimeout|beforeAll|afterAll|mock|spyOn|stub' test tests __tests__ e2e
```

### DevOps probes

```bash
# Manual deployment and missing rollback/observability signals
grep -RInE 'manual|rollback|revert|deploy|canary|blue-green|health|observability|metrics|trace|artifact' .github . gitlab ci ops infra scripts
```

## Anti-pattern heuristics by domain

### Frontend

#### Props Drilling

Confirm when the same data passes through multiple intermediate components that do not own or use it meaningfully.

Suggested remediation:

- Introduce context or scoped state management.
- Recompose component boundaries.
- Lift or localize state intentionally.

#### Array Index as Key

Confirm when dynamic lists use `index` as key and list order can change.

Suggested remediation:

- Use stable identifiers.

#### `useEffect` Overuse

Confirm when effects exist only to derive state from state or props.

Suggested remediation:

- Replace with derived values, memoization, or event-driven updates.

#### Missing Memoization

Confirm only when expensive recomputation or child rerender churn is observable.

Suggested remediation:

- Profile first, then add `useMemo`, `useCallback`, or component memoization selectively.

### Backend

#### Callback Hell

Confirm when nested asynchronous control flow materially harms readability, error handling, or composability.

Suggested remediation:

- Convert to `async`/`await`.
- Extract named functions.

#### Unhandled Promise Rejections

Confirm when async failures bypass structured handling.

Suggested remediation:

- Add boundary error handling, global rejection policy, and lint rules.

#### Missing Input Validation

Confirm when external inputs flow into business logic or persistence without schema validation.

Suggested remediation:

- Validate at API boundaries with explicit schemas.

#### God Controller

Confirm when controllers mix transport, business rules, validation, persistence orchestration, and error formatting.

Suggested remediation:

- Extract application services and validation middleware.

#### Error Swallowing

Confirm when errors are ignored, only printed, or transformed into ambiguous success paths.

Suggested remediation:

- Classify, log structurally, propagate or handle explicitly.

### Databases

#### N+1 Query Problem

Confirm when a loop triggers per-row data fetches that can be batched.

Suggested remediation:

- Use eager loading, joins, or batch loaders.

#### `SELECT *`

Treat as anti-pattern when broad selection causes waste, weak contracts, or prevents index-friendly reads.

Suggested remediation:

- Select only required columns.

#### EAV

Confirm when flexible schema design destroys type safety, constraints, and efficient query paths.

Suggested remediation:

- Prefer normalized schema, JSONB, or document storage based on access patterns.

#### Index Shotgun

Confirm when indexes were added broadly without evidence from plans or workload.

Suggested remediation:

- Review plans, measure usage, remove dead indexes.

#### No `EXPLAIN`

Confirm when complex or slow queries lack plan analysis culture.

Suggested remediation:

- Require `EXPLAIN` or equivalent review for non-trivial queries.

### Testing

#### Flaky Tests

Confirm when tests are timing-sensitive, order-sensitive, or depend on unstable externals.

Suggested remediation:

- Remove nondeterminism, isolate dependencies, use explicit waits and seeded data.

#### Test Coupling

Confirm when tests depend on execution order or shared mutable state.

Suggested remediation:

- Reset state between tests and enforce isolation.

#### Over-Mocking

Confirm when tests mostly verify mocks instead of system behavior.

Suggested remediation:

- Increase behavior-focused and integration-level coverage for critical paths.

### DevOps / CI/CD

#### Manual Steps in Pipeline

Confirm when successful delivery depends on undocumented or human-only operations.

Suggested remediation:

- Automate delivery steps and infrastructure changes.

#### No Rollback Strategy

Confirm when failed deployments have no tested recovery path.

Suggested remediation:

- Add blue-green, canary, or scripted rollback procedures.

#### Pipeline Without Observability

Confirm when failures are hard to diagnose due to missing logs, metrics, timing, or flaky-test visibility.

Suggested remediation:

- Add structured pipeline telemetry and failure analytics.

## Confidence model

| Confidence | Meaning                                                                  |
| ---------- | ------------------------------------------------------------------------ |
| High       | Direct code, query, test, or pipeline evidence confirms the anti-pattern |
| Medium     | Strong static signals exist but operational confirmation is incomplete   |
| Low        | Symptoms are suggestive but also compatible with benign local trade-offs |

## Deliverables

Produce a report with:

1. Scope, stack, and audited domains.
2. Findings summary by domain.
3. Detailed findings with evidence, impact, counter-evidence, confidence, and severity.
4. Cross-domain root causes.
5. Prioritized remediation roadmap.
6. Unknowns and data needed for stronger confirmation.

## Output template

```markdown
# Code Development Antipattern Audit

## Scope

- Repository / subsystem:
- Stack:
- Domains reviewed:

## Findings Summary

| Domain | Anti-pattern | Confidence | Severity | Why it matters |
| ------ | ------------ | ---------- | -------- | -------------- |

## Detailed Findings

### <Domain> — <Anti-pattern>

- Hypothesis:
- Evidence:
- Counter-evidence:
- Impact:
- Confidence:
- Severity:
- Recommended action:

## Cross-Domain Causes

- Over-coupling:
- Missing boundaries:
- Missing automation:
- Fear-driven workarounds:

## Remediation Roadmap

1. Immediate stabilizers
2. Near-term refactors
3. Long-term process improvements

## Unknowns

- Runtime evidence needed:
- Ownership or workflow clarifications needed:
```

## Constraints

### MUST DO

- Ground every finding in observable evidence.
- Distinguish code anti-patterns from mere style differences.
- Include counter-evidence and uncertainty.
- Connect local findings to delivery or maintainability impact.
- Prefer incremental, practical remediation.

### MUST NOT DO

- Generalize from one isolated example to the entire codebase.
- Recommend broad rewrites without staged alternatives.
- Label optimization as anti-pattern without performance context.
- Ignore security and operational consequences of backend, DB, or pipeline findings.
