---
name: verification
description: "Evidence-based verification of actual API, MCP, CLI, job or browser journeys with dependent-failure isolation."
metadata:
  priority: 7
  docs:
    - "https://vercel.com/docs/projects/project-configuration"
  sitemap: "https://vercel.com/sitemap/docs.xml"
  pathPatterns: []
  bashPatterns:
    - '\bnext\s+dev\b'
    - '\bnpm\s+run\s+dev\b'
    - '\bpnpm\s+dev\b'
    - '\bbun\s+run\s+dev\b'
    - '\byarn\s+dev\b'
    - '\bvite\s*(dev)?\b'
    - '\bvercel\s+dev\b'
    - '\bastro\s+dev\b'
  importPatterns: []
  promptSignals:
    phrases:
      - "verify the flow"
      - "verify everything works"
      - "test the whole thing"
      - "does it actually work"
      - "check end to end"
      - "end to end test"
      - "why isn't it working right"
      - "why doesn't it work"
      - "it's not working correctly"
      - "something's off"
      - "not quite right"
      - "almost works but"
      - "works locally but"
      - "verify the feature"
      - "make sure it works"
      - "full verification"
    allOf:
      - [verify, flow]
      - [verify, works]
      - [check, everything]
      - [test, end, end]
      - [not, working, right]
      - [something, off]
      - [almost, works]
      - [make, sure, works]
    anyOf:
      - "verify"
      - "verification"
      - "end-to-end"
      - "full flow"
      - "works"
      - "working"
    noneOf:
      - "unit test"
      - "jest"
      - "vitest"
      - "playwright test"
      - "cypress test"
    minScore: 6
---

# Full-Story Verification

Verify the user goal through its **actual supported interface**. API-only tasks require API calls, not browser checks. Use MCP, CLI, job execution, or visual/browser testing only when the user journey requires them.

## 1. Recover the contract

Read the request, relevant code, routes, schemas, approvals and existing tests. Identify a representative journey and its boundaries (input → identity/access → processing → persistence/effects → output). Include crash recovery or cancellation where those are meaningful risks. Use isolated fixtures and least-privilege credentials; never expose secrets.

Choose unit/contract checks for deterministic rules, integration tests for boundaries and a thin E2E for the user-critical full path. Do not turn an E2E request into UI testing when the interface is backend-only.

## 2. Execute and record

- Verify positive, failure/unauthorized and recovery paths proportionate to the change.
- Assert final outcome, authorized actions, and persistent effects. Explicit confirmation is required before irreversible actions.
- For each boundary retain sanitized command, expected and actual result, code revision, log/trace reference and status.
- Use `pass`, `fail`, `blocked`, `timeout`, `infrastructure_error`, `grader_error` and `not_run`. Missing evidence never means pass.
- If one boundary breaks, stop **dependent** checks but continue independent checks. Mark blocked steps explicitly.
- If the environment yields no useful signal, report an observability gap rather than retry indefinitely.

## 3. Report

State the journey and scope, each boundary's status and evidence, defect reproduction and minimal proposed fix. Distinguish fully exercised success, failures, blockers and untested areas. Do not report end-to-end success unless the complete relevant path was executed.

For agent trajectories and reproducible results use [the shared agent-test contract](../agent-evals-lab/references/agent-test-contract.md). For UI-only execution use [playwright-expert](../playwright-expert/SKILL.md); browser access is not a universal prerequisite.
