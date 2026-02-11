---
name: frontend-vue-developer
description: This skill should be used when drafting, reviewing, or refactoring modern Vue 3 frontends that require senior-level guidance across SPA, Nuxt, or component-library contexts, with explicit decisions for architecture, reactivity discipline, TypeScript, CSS, accessibility, security, testing, and release quality.
---

# frontend-vue-developer
<!-- NAV:skill=
# frontend-vue-developer -->
<!-- NAV:contexts=[SPA|NEXT|LIB|GEN] -->
<!-- NAV:source=inline(frontendDev) -->

## Purpose
- Provide senior frontend guidance for Vue 3, TypeScript 5+, and modern CSS across [SPA]/[NUXT]/[LIB] delivery contexts.
- Translate the research guide into a reusable workflow with decisions, defaults, and quality gates.

## When to Use (Triggers)
- Apply when designing or reviewing a Vue SPA architecture and state/data strategy.
- Apply when choosing [SPA] vs [NUXT] delivery or deciding SSR/data-fetching semantics.
- Apply when establishing UI library/public API discipline for a Vue component library.
- Apply when defining quality gates: a11y, security, testing, performance, CI/release.

## When NOT to Use (Non-goals)
- Do not use for backend architecture, infrastructure, or cloud ops unless required to explain frontend behavior.
- Do not use for non-Vue UI frameworks or non-TypeScript codebases.

## Inputs Required (Context Classification)
- Provide delivery context tag: [SPA] / [NUXT] / [LIB] / [GEN].
- Provide product constraints:
  - Rendering model requirements (client-only vs server-first).
  - Data fetching model (Nuxt composables vs client cache).
  - Styling system preference or constraints (CSS Modules / scoped CSS / utility-first).
  - A11y target (WCAG level, keyboard support, semantic constraints).
  - Test scope and release risk tolerance.
- If inputs are missing, classify as [GEN] and surface decision guidance before recommending defaults.

## Workflow (Step-by-step)
1) Classify context and set defaults
   - Choose [SPA] vs [NUXT] based on rendering and data-fetching requirements.
   - Apply default styling per context.
   - If [LIB], enforce public API surface and semver discipline.

2) Define architecture boundaries and dependency rules
   - Use feature-first + shared kernel for apps; package-first for [LIB].
   - Enforce import-direction rules (shared must not depend on feature).

3) Enforce Vue reactivity discipline
   - Use computed for derived state; watchers for side effects.
   - Treat deep watch and sync flush as exceptional and justify.

4) Choose state/data strategy
   - [NUXT]: prefer useFetch/useAsyncData for SSR-visible data; avoid $fetch in setup.
   - [SPA]: use client caching for server state; keep UI state local unless justified.

5) Set TypeScript policy
   - Enforce vue-tsc in CI and document TS config constraints.

6) Define CSS and design-system constraints
   - Use tokens via CSS variables; apply cascade control; prefer scalable CSS architecture.

7) Enforce accessibility requirements
   - Prefer semantic HTML; treat ARIA roles as a contract.
   - Require keyboard/focus behavior for custom widgets.

8) Apply frontend security gates
   - Gate unsafe HTML/DOM escape hatches and sanitize inputs.
   - Adopt CSP with staged rollout; do not treat CSP as a sanitization substitute.

9) Build the testing portfolio
   - Unit + component dominate; E2E is thin and isolated.
   - Prefer public-interface testing for components.

10) Enforce CI/release gates
   - Gate on types, lint, tests, and minimal E2E; include a11y and performance budgets.

## Output Format Template
- **Summary**
  - Goal, constraints, and chosen context tag ([SPA]/[NUXT]/[LIB]/[GEN]).
- **Context Classification**
  - Decision rationale + defaults applied.
- **Architecture**
  - Structure choice, dependency rules, boundary checks.
- **Vue Patterns**
  - Reactivity discipline, watcher usage, `<script setup>` practices.
- **State & Data**
  - Derived vs UI vs server state approach; Nuxt data loading policy.
- **TypeScript**
  - Strictness policy, typing boundaries, escape hatches.
- **CSS & Design System**
  - Token strategy, styling default, cross-browser strategy.
- **Accessibility**
  - Semantic elements, keyboard/focus requirements, test gates.
- **Security**
  - HTML injection policy, CSP stance.
- **Testing**
  - Test pyramid, E2E scope.
- **Performance**
  - Profiling findings, optimization choices, CWV budgets.
- **Tooling & CI**
  - Build assumptions, lint/type gates, release checks.
- **Risks / Trade-offs**
  - Explicit trade-offs and mitigation actions.
- **Next Steps**
  - Concrete to-dos with owners and acceptance checks.
- **References**
  - Cite relevant sections in the research guide.

## Quality Gates / Validation Checklist
- `<script setup>` used by default; top-level side effects reviewed.
- Derived state computed; watchers used for side effects only.
- Deep watch and sync flush justified and rare.
- [NUXT] SSR data uses useFetch/useAsyncData; avoid $fetch in setup.
- vue-tsc enforced in CI; tsconfig aligns with Vite pipeline.
- WCAG 2.2 AA constraints applied; ARIA role promises fulfilled.
- HTML injection gated and sanitized; CSP staged rollout planned.
- Test pyramid aligned; E2E suite isolated and minimal.

## Navigation Tags / Context Comments
<!-- NAV:tags=frontend,vue,typescript,css,a11y,security,testing,performance -->
<!-- NAV:contexts=[SPA|NUXT|LIB|GEN] -->
