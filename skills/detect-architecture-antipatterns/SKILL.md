---
name: detect-architecture-antipatterns
description: This skill should be used when auditing an existing system for software architecture anti-patterns, including Big Ball of Mud, God Object, Lava Flow, Distributed Monolith, Shared Database, Chatty Services, and other structural maintainability risks. Use when reviewing codebases, service boundaries, dependency graphs, runtime integrations, or technical debt hotspots and when producing evidence-based remediation recommendations.
license: MIT
allowed-tools: Read, Grep, Glob, Bash
metadata:
  author: Builder AI Team
  version: "1.0.0"
  domain: architecture-review
  triggers: architecture anti-patterns, architectural smells, distributed monolith, big ball of mud, god object, service coupling, shared database, technical debt, architecture audit, dependency analysis
  role: specialist
  scope: review
  output-format: report
  related-skills: architecture-designer, microservices-architect, spec-miner, code-reviewer
---

# Detect Architecture Antipatterns

Detect recurring harmful architectural structures in an existing codebase or system design. Ground findings in evidence from source code, configuration, dependency structure, deployment topology, and operational conventions. Distinguish confirmed anti-patterns from weak signals and from acceptable trade-offs.

## When to use

- Audit a monolith, modular monolith, or microservice system for architecture degradation.
- Review whether a codebase is drifting toward Big Ball of Mud, God Object, or Lava Flow.
- Check whether a microservice estate is actually a Distributed Monolith.
- Investigate technical debt hotspots before modernization, decomposition, or platform migration.
- Produce an architecture health report with concrete evidence and remediation priorities.

## Anti-pattern catalog

Evaluate at least the following categories unless the task scope explicitly excludes them:

| Anti-pattern                             | Primary signals                                                                                                 |
| ---------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| Big Ball of Mud                          | Missing module boundaries, pervasive cross-layer imports, unclear ownership, mixed responsibilities             |
| God Object / Blob                        | One module, class, or service centralizes too much behavior, orchestration, or state                            |
| Lava Flow                                | Legacy areas nobody changes safely, dead or frozen codepaths, fear-driven avoidance                             |
| Distributed Monolith                     | Services require lockstep deployment, synchronous dependency chains, shared persistence, tight runtime coupling |
| Shared Database                          | Multiple services or modules read and write the same schema without ownership boundaries                        |
| Chatty Services                          | Excessive request chains for simple operations, high fan-out/fan-in, latency-sensitive synchronous coupling     |
| Stovepipe System                         | Isolated subsystems with duplicated logic and poor interoperability                                             |
| Golden Hammer                            | Tooling or architecture used by habit despite mismatch with actual requirements                                 |
| Analysis Paralysis / Design by Committee | Decision stagnation visible in ADR gaps, contradictory docs, or excessive design churn without delivery         |

## Core workflow

### 1. Define scope and unit of analysis

- Determine whether the audit target is a repository, a subsystem, a service mesh, or a deployment topology.
- Identify the architecture style claimed by the system: monolith, modular monolith, microservices, event-driven, layered, plugin-based, or hybrid.
- Record the expected quality attributes: maintainability, deployability, scalability, reliability, operability, or team autonomy.

Validation checkpoint:

- Do not classify anti-patterns before understanding the intended architecture and constraints.

### 2. Map the structural evidence

- Inspect entry points, service directories, build files, dependency manifests, infra descriptors, and architecture docs.
- Build a dependency view across modules or services.
- Trace ownership of data stores, queues, APIs, and shared libraries.
- Look for code concentration, cyclic dependencies, orchestration bottlenecks, and cross-boundary leakage.

Validation checkpoint:

- If architecture claims cannot be matched to observable structure, flag documentation drift.

### 3. Test anti-pattern hypotheses

For each suspected anti-pattern:

1. State the hypothesis.
2. Collect direct evidence.
3. Record counter-evidence.
4. Decide confidence level: high, medium, or low.
5. Estimate impact on quality attributes.

Use language such as:

- Confirmed anti-pattern
- Strong signal, needs runtime confirmation
- Weak signal, insufficient evidence
- Acceptable trade-off for current scale

### 4. Assess severity and causality

- Distinguish local smells from systemic structural failure.
- Identify likely drivers: deadline pressure, missing boundaries, weak ownership, absent tests, unsuitable platform choices, or organizational coupling.
- Prioritize findings by operational risk and refactoring leverage.

### 5. Recommend remediation path

- Prefer incremental remediation over rewrite-first advice.
- Link each finding to concrete next steps: extract module, define API contract, split data ownership, introduce async messaging, remove dead code, add characterization tests, or write ADRs.
- Sequence changes to reduce risk and preserve delivery flow.

## Evidence collection patterns

Start with repository-wide exploration. Prefer semantic or grep-driven discovery before detailed reading.

### Structural discovery examples

```bash
# Find architectural entry points and manifests
find . -maxdepth 3 \( -name 'package.json' -o -name 'pyproject.toml' -o -name 'pom.xml' -o -name 'go.mod' -o -name 'Dockerfile' -o -name 'docker-compose*.yml' -o -name 'kustomization.yaml' -o -name '*.tf' \)

# Find architecture documentation and ADRs
find . \( -iname '*adr*' -o -iname '*architecture*' -o -path '*/docs/*' \)

# Detect TODO/HACK debt concentrations
grep -RInE 'TODO|FIXME|HACK|XXX|temporary|workaround|do not touch' .
```

### Dependency and coupling heuristics

```bash
# Cross-layer import leakage examples
grep -RInE 'from .*infrastructure|from .*controllers|import .*repository|import .*service' src app services

# Potential cyclic or broad dependency hubs
grep -RInE 'client|gateway|orchestrator|manager|util|common|shared' src app services

# Shared database usage across multiple services
grep -RInE 'DATABASE_URL|postgres|mysql|mongodb|redis' services apps packages
```

### Microservice anti-pattern probes

```bash
# Synchronous HTTP chatter between services
grep -RInE 'http://|https://|fetch\(|axios\.|requests\.|grpc' services apps

# Shared schema or same table names across services
grep -RInE 'users|orders|payments|inventory' services/*/migrations services/*/models

# Lockstep deployment hints
grep -RInE 'depends_on|required_services|startup order|wait-for' .
```

## Heuristics by anti-pattern

### Big Ball of Mud

Confirm only when most of the following are present:

- No stable layering or bounded contexts
- Frequent imports across unrelated domains
- Business logic mixed with transport, persistence, and view concerns
- No clear module ownership or dependency rules

Suggested remediation:

- Define bounded contexts
- Introduce module boundaries and dependency rules
- Move side effects to edges
- Add architecture fitness checks

### God Object / Blob

Signals:

- One file or class receives disproportionate edits
- Central manager or service coordinates unrelated domains
- Excessive method count, dependencies, or state ownership

Suggested remediation:

- Split by responsibility and workflow phase
- Extract interfaces and collaborators
- Move orchestration to dedicated application services only where justified

### Lava Flow

Signals:

- Dead modules retained “just in case”
- Legacy code wrapped in fear-based comments
- Low test coverage concentrated in oldest codepaths
- Repeated workaround layers over unclear behavior

Suggested remediation:

- Add characterization tests
- Isolate behind façade or adapter
- Remove unused branches and dependencies
- Replace incrementally using strangler-style migration

### Distributed Monolith

Confirm only when multiple forms of coupling coexist:

- Shared database or schema ownership violations
- Synchronous request chains for core business flows
- Lockstep deployment or version pinning across services
- Cross-service changes required for routine feature work

Suggested remediation:

- Re-draw service boundaries around business capabilities
- Enforce database-per-service ownership
- Convert selected sync flows to async events
- Introduce explicit contracts and compatibility policy

### Shared Database

Signals:

- Same tables referenced by multiple services
- Cross-service joins or direct reads bypassing owning API
- Shared migration ownership

Suggested remediation:

- Assign data ownership
- Expose data through APIs or events
- Migrate reads via anti-corruption layers

### Chatty Services

Signals:

- One user request fans out to many synchronous calls
- UI or gateway composes too many service round-trips
- Latency spikes correlate with dependency depth

Suggested remediation:

- Coarsen APIs
- Introduce aggregation or read models
- Shift to event-driven propagation where appropriate

## Confidence model

Assign confidence explicitly:

| Confidence | Meaning                                                                            |
| ---------- | ---------------------------------------------------------------------------------- |
| High       | Direct repository or runtime evidence supports the classification                  |
| Medium     | Strong static signals exist, but runtime or organizational confirmation is missing |
| Low        | Symptoms are suggestive but can also be explained by benign constraints            |

Do not overstate certainty. If evidence is mixed, say so.

## Deliverables

Produce a report with these sections:

1. Scope and target architecture.
2. Evidence map: modules, services, data ownership, deployment coupling.
3. Findings table with anti-pattern, evidence, confidence, severity, impact.
4. Root-cause analysis.
5. Prioritized remediation roadmap.
6. Open questions and data needed for stronger confirmation.

## Output template

```markdown
# Architecture Antipattern Audit

## Scope

- Target:
- Claimed architecture:
- Quality attributes at risk:

## Findings Summary

| Anti-pattern | Confidence | Severity | Why it matters |
| ------------ | ---------- | -------- | -------------- |

## Detailed Findings

### 1. <Anti-pattern name>

- Hypothesis:
- Evidence:
- Counter-evidence:
- Impact:
- Confidence:
- Recommended action:

## Root Causes

- Organizational:
- Technical:
- Documentation / ownership:

## Remediation Roadmap

1. Immediate stabilizers
2. Near-term structural changes
3. Longer-term modernization

## Unknowns

- Runtime telemetry needed:
- Ownership clarifications needed:
- Architecture decisions missing:
```

## Constraints

### MUST DO

- Ground every finding in observable evidence.
- Separate symptoms from confirmed anti-pattern classifications.
- Include counter-evidence and uncertainty.
- Prioritize by architectural impact, not by style preference.
- Prefer pragmatic remediation with sequencing.

### MUST NOT DO

- Declare microservices “bad” solely because they are complex.
- Confuse code smell with architecture anti-pattern without structural evidence.
- Recommend full rewrites without incremental alternatives.
- Ignore organizational causes behind technical symptoms.
- Treat temporary trade-offs as permanent failures without context.
