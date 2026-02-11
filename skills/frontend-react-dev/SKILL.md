---
name: frontend-react-dev
description: This skill should be used when drafting, reviewing, or refactoring modern React frontends that require senior-level guidance across SPA, Next.js App Router, or component-library contexts, with explicit decisions for architecture, state/data, TypeScript, CSS, accessibility, security, testing, and release quality.
---

# frontend-react-dev
<!-- NAV:skill=frontend-react-dev -->
<!-- NAV:contexts=[SPA|NEXT|LIB|GEN] -->
<!-- NAV:source=inline(frontendDev) -->

## Purpose
- Provide senior frontend guidance for React 18+, TypeScript 5+, and modern CSS across [SPA]/[NEXT]/[LIB] delivery contexts.
  Context summary: [SPA] means Vite-based client apps with CSS Modules + tokens by default; [NEXT] means App Router with server/client components and Tailwind + tokens by default; [LIB] means component libraries with explicit public APIs and semver discipline; [GEN] is framework-agnostic decision guidance.
- Translate the source guide into a reusable workflow with decisions, defaults, and quality gates.
  Context summary: Recommendations are organized into principles, decision matrices, defaults, anti-patterns, and validation gates covering architecture, state, TS, CSS, a11y, security, testing, performance, and release practices.

## When to Use (Triggers)
- Apply when designing or reviewing a React SPA architecture and state/data strategy.
  Context summary: Favor feature-first + shared kernel, keep shared code independent from feature code, and separate UI state from server state to reduce coupling and stale-data bugs.
- Apply when choosing [SPA] vs [NEXT] delivery or CSS strategy via decision matrices.
  Context summary: [SPA] fits client-only apps with client caching; [NEXT] fits server-first rendering with server caching/revalidation; CSS options trade scoped safety (CSS Modules), utility constraints (Tailwind), and runtime cost (CSS-in-JS).
- Apply when establishing UI library/public API discipline for a component library.
  Context summary: Treat props, tokens, DOM structure, and a11y behavior as public API; semver requires a declared public API and disciplined breaking-change review.
- Apply when defining quality gates: a11y, security, testing, performance, CI/release.
  Context summary: Use WCAG-aligned a11y checks, sanitize HTML injection and adopt CSP, keep test pyramid thin on E2E, enforce Core Web Vitals budgets, and gate releases with types/lint/tests.

## When NOT to Use (Non-goals)
- Do not use for backend architecture, infrastructure, or cloud ops unless required to explain frontend behavior.
  Context summary: The guide focuses on frontend quality gates and UI correctness; backend/infra topics are explicitly excluded except for frontend-facing implications.
- Do not use for non-React UI frameworks or non-TypeScript codebases.

## Inputs Required (Context Classification)
- Provide delivery context tag: [SPA] / [NEXT] / [LIB] / [GEN].
  Context summary: [SPA]=Vite client app; [NEXT]=App Router with server/client components; [LIB]=npm component library; [GEN]=decision matrices without a single default.
- Provide product constraints:
  - Rendering model requirements (client-only vs server-first).
    Context summary: [SPA] assumes client-only runtime; [NEXT] assumes server-first rendering with client islands.
  - Data caching preferences (client cache vs server cache).
    Context summary: [SPA] defaults to client cache via a server-state library; [NEXT] defaults to server fetch caching with revalidation.
  - Styling system preference or constraints (CSS Modules/Tailwind/CSS-in-JS).
    Context summary: CSS Modules are scoped by default, Tailwind enforces utility constraints, CSS-in-JS trades colocation for runtime/SSR cost.
  - A11y target (WCAG level, keyboard support, semantic constraints).
    Context summary: WCAG criteria are testable and tech-agnostic; semantic HTML is preferred, ARIA is a high-risk contract.
  - Test scope and release risk tolerance.
    Context summary: Favor unit+integration with a thin, isolated E2E suite; gate releases with types/lint/tests and performance budgets.
- If inputs are missing, classify as [GEN] and surface decision matrices before recommending defaults.

## Workflow (Step-by-step)
<!-- NAV:section=workflow -->

1) Classify context and set defaults  
   - Choose [SPA] vs [NEXT] using the decision matrix.  
     Context summary: [SPA] fits client-only rendering with client caching; [NEXT] fits server-first rendering with server caching and revalidation.  
   - Apply default styling per context.  
     Context summary: [SPA]=CSS Modules + tokens; [NEXT]=Tailwind + tokens; [LIB]=vanilla-extract or CSS Modules + tokens.  
   - If [LIB], enforce public API surface and semver discipline.  
     Context summary: Public API includes component props, tokens, DOM structure, and a11y behavior; semver requires declaring and protecting this API.

   **Decision matrix: [SPA] vs [NEXT] (summary)**  
   | Dimension | Prefer [SPA] | Prefer [NEXT] |
   |---|---|---|
   | Rendering | Client-only | Server-first + islands |
   | Data caching | Client cache | Server cache + revalidation |
   | Error boundaries | App-level client | Per-segment error boundaries |

2) Define architecture boundaries and dependency rules  
   - Use feature-first + shared kernel for apps; package-first for [LIB].  
     Context summary: Feature-first reduces coupling and keeps refactors cheap; package-first keeps public API explicit for libraries.  
   - Enforce import-direction rules (shared must not depend on feature).  
     Context summary: Shared primitives stay stable and pure; features may depend on shared utilities, not the reverse.  
   - Avoid “components/” as a dumping ground.  
     Context summary: Ungoverned component buckets create implicit coupling and undocumented dependencies.

3) Enforce React purity and effect discipline  
   - Treat render as pure; keep side effects out of render.  
     Context summary: Concurrency assumes render is a pure calculation; impure render breaks under re-renders and interruptions.  
   - Use Strict Mode in dev and treat failures as design bugs.  
     Context summary: Strict Mode double-invokes render/effects to surface impurity and missing cleanup.  
   - Use effects only for external synchronization; avoid derived-state effects.  
     Context summary: Effects are for external systems; derived values belong in render or memoization.

4) Choose state/data strategy  
   - Compute derived values during render; use memoization only if needed.  
     Context summary: Derived state in effects creates cascades and stale bugs; calculate from props/state during render.  
   - Use reducers + scoped context for complex screen-local state.  
     Context summary: Reducers consolidate update logic; scoped context avoids deep prop drilling without global rerenders.  
   - For server state:  
     - [SPA] default to TanStack Query.  
       Context summary: Server state is remote, async, and stale-able; dedicated caching handles invalidation and deduping.  
     - [NEXT] default to server fetch + framework caching/revalidation.  
       Context summary: Server fetch caching and revalidation are first-class semantics; client caching is for interactive islands only.

5) Set TypeScript policy  
   - Enable `strict` as default.  
     Context summary: `strict` enables stronger correctness checks; TS upgrades can surface new errors, so treat upgrades as planned changes.  
   - Use `satisfies` for config-like objects where inference matters.  
     Context summary: `satisfies` validates shape without losing inferred specificity for config maps and tokens.  
   - Forbid blanket `any` and uncontrolled casts.  
     Context summary: `any` hides defects; prefer `unknown` + narrowing or well-scoped assertions.

6) Define CSS and design-system constraints  
   - Use design tokens via CSS variables.  
     Context summary: Tokens provide a design contract; CSS variables allow runtime theming without rebuilds.  
   - Establish cascade layers to control override order.  
     Context summary: Layer order (reset → tokens → base → components → utilities) prevents specificity wars.  
   - Apply context defaults: [SPA]=CSS Modules, [NEXT]=Tailwind, [LIB]=vanilla-extract/CSS Modules.  
     Context summary: Choose scoped or utility-first approaches based on delivery context and runtime constraints.

   **Decision matrix: CSS strategy (summary)**  
   | Option | Strengths | Risks |
   |---|---|---|
   | CSS Modules | Scoped by default | Needs token/layer discipline |
   | Tailwind | Utility constraints | Class sprawl, token governance |
   | CSS-in-JS | Colocation | Runtime/SSR complexity |

7) Enforce accessibility requirements  
   - Prefer semantic HTML; treat ARIA as a high-risk contract.  
     Context summary: WCAG criteria are testable and tech-agnostic; ARIA roles require correct keyboard behavior and state management.  
   - Require keyboard interactions and focus management for custom widgets.  
     Context summary: Custom roles imply full keyboard support, not just visual styling.  
   - Add automated a11y checks + manual keyboard audits.  
     Context summary: Automated checks catch regressions; manual audits validate real keyboard and focus flows.

8) Apply frontend security gates  
   - Gate `dangerouslySetInnerHTML` behind a single audited module and sanitize.  
     Context summary: Framework escape hatches reintroduce XSS risk; sanitize and centralize usage.  
   - Adopt CSP with staged rollout (report-only → enforce).  
     Context summary: CSP is defense-in-depth and not a replacement for sanitization.

9) Build the testing portfolio  
   - Use unit + integration as the base; keep E2E thin and critical-path only.  
     Context summary: A test pyramid reduces cycle time and flakiness while preserving coverage of user flows.  
   - Use user-centric queries for component tests.  
     Context summary: Test visible behavior via roles/labels to avoid brittle implementation details.  
   - Ensure Playwright tests are isolated and parallel-safe.  
     Context summary: Browser contexts are clean-slate; tests must not depend on shared state.  
   - For [LIB], require stories/docs for public components.  
     Context summary: Stories act as executable documentation and define supported variants.

10) Address performance with measurement-first workflow  
    - Profile real user flows; optimize the smallest effective lever.  
      Context summary: Use React Profiler to find expensive subtrees before applying memoization or refactors.  
    - Consider `content-visibility` for long pages only after profiling.  
      Context summary: It can skip off-screen rendering work but requires QA and intrinsic size to avoid layout shifts.  
    - Define Core Web Vitals budgets for CI.  
      Context summary: LCP/INP/CLS thresholds create measurable release gates.

11) Align tooling and builds  
    - For [SPA], prefer Vite defaults and document any `optimizeDeps` overrides.  
      Context summary: Vite pre-bundles deps for CJS/UMD compatibility and faster dev reloads using esbuild.  
    - For [LIB], ensure build outputs match public API exports.  
      Context summary: Public exports are the compatibility contract; types and runtime outputs must align.

12) Enforce CI/release gates  
    - Gate on types, lint, tests, and minimal E2E.  
      Context summary: Fast deterministic checks catch regressions early; keep E2E limited to critical paths.  
    - For [LIB], enforce semver + changelog + API diff review.  
      Context summary: Versioning communicates compatibility; API diffs prevent accidental breakage.

13) Apply review and maintainability standards  
    - Prefer continuous improvement over perfection in code review.  
      Context summary: Review should improve overall code health and still ship incremental progress.  
    - Audit public APIs and deprecations on a regular cadence.  
      Context summary: Long-lived products require explicit deprecation policy and periodic API reviews.

## Output Format Template
<!-- NAV:section=output-template -->
- **Summary**
  - Goal, constraints, and chosen context tag ([SPA]/[NEXT]/[LIB]/[GEN]).
- **Context Classification**
  - Decision rationale + defaults applied.
- **Architecture**
  - Structure choice, dependency rules, boundary checks.
- **React Patterns**
  - Purity constraints, effect usage, Strict Mode stance.
- **State & Data**
  - Derived vs UI vs server state approach; caching policy.
- **TypeScript**
  - Strictness policy, typing boundaries, escape hatches.
- **CSS & Design System**
  - Token strategy, layering, styling default.
- **Accessibility**
  - Semantic elements, keyboard/focus requirements, test gates.
- **Security**
  - HTML injection policy, CSP stance.
- **Testing**
  - Test pyramid, E2E scope, Storybook/docs for [LIB].
- **Performance**
  - Profiling findings, optimization choices, CWV budgets.
- **Tooling & CI**
  - Build assumptions, lint/type gates, release checks.
- **Risks / Trade-offs**
  - Explicit trade-offs and mitigation actions.
- **Next Steps**
  - Concrete to-dos with owners and acceptance checks.
- **References**
  - Cite relevant sections in this skill.

## Quality Gates / Validation Checklist
<!-- NAV:section=quality-gates -->
- Purity enforced; no side effects in render.
- Strict Mode enabled in dev and failures addressed.
- Dependency boundaries enforced; no cross-feature imports.
- Derived state computed in render; effects used only for external sync.
- Server-state tooling aligns with context defaults.
- TypeScript `strict` enabled; no blanket `any`.
- Token and layer strategy documented and enforced.
- A11y checks automated + manual keyboard audit scheduled.
- HTML injection gated and sanitized; CSP rollout planned.
- Test pyramid aligned; E2E suite isolated and minimal.
- Performance budgets defined for CI.
- [LIB] releases follow semver + changelog + API diff.
- Code review standard emphasizes continuous improvement.

## Navigation Tags / Context Comments
<!-- NAV:tags=frontend,react,typescript,css,a11y,security,testing,performance -->
<!-- NAV:contexts=[SPA|NEXT|LIB|GEN] -->
