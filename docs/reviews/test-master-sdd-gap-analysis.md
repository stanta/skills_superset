# Code & Architecture Review: `skills/test-master` vs. Spec-Driven Development (SDD)

**Reviewer:** Claude (Architecture & Code Reviewer mode)  
**Date:** 2026-04-15  
**Target:** [`skills/test-master/SKILL.md`](../../skills/test-master/SKILL.md) and all reference files  
**Context:** Evaluate whether the SDD (Spec-Driven Development) methodology — a 4-phase AI-assisted test-generation workflow — is present, partially present, or absent in the current skill.

---

## Executive Summary

The `test-master` skill is a solid, well-structured testing reference. It covers classical TDD, common anti-patterns, QA methodology, and framework patterns. However, **the SDD wisdom described in the task is largely absent**. The skill handles _humans writing tests_; it does not model the specific failure modes of _AI agents generating tests_ — reward hacking, tautological assertions, and prompt-phase confusion — nor does it prescribe the phased workflow that prevents them.

| Area                                                                | Coverage   | Severity  |
| ------------------------------------------------------------------- | ---------- | --------- |
| SDD 4-phase workflow (Use Cases → Test Cases → Code → Verification) | ❌ Absent  | 🔴 High   |
| Anti-reward-hacking constraint (never alter assertions to pass)     | ❌ Absent  | 🔴 High   |
| Tautology filter ("what bug does this test catch?")                 | ❌ Absent  | 🔴 High   |
| Mutation-testing verification step                                  | ❌ Absent  | 🟡 Medium |
| Few-shot example emphasis for AI prompting                          | ⚠️ Partial | 🟡 Medium |
| AI system-prompt templates                                          | ❌ Absent  | 🟡 Medium |
| SDD tooling references (Spec Kit, OpenSpec)                         | ❌ Absent  | 🟢 Low    |
| Mock-behavior anti-pattern                                          | ✅ Present | —         |
| Edge-case / boundary testing mandate                                | ✅ Present | —         |
| Specific assertion requirement                                      | ✅ Present | —         |
| TDD iron laws                                                       | ✅ Present | —         |

---

## What Is Present (Positive Findings)

### 1. Anti-Pattern: Testing Mocks (partial SDD alignment)

[`references/testing-anti-patterns.md`](../../skills/test-master/references/testing-anti-patterns.md:16) — Anti-Pattern 1 ("Testing Mock Behavior") directly addresses the _symptom_ the SDD tautology filter is designed to prevent. The rule **"Test what the code does, not what the mocks do"** is a correct and well-illustrated principle. This is the closest the existing skill comes to Phase 2's bug-catching filter.

**Why this is not enough:** The anti-pattern document describes the _smell_ and the _code fix_. It does not give the _prompting discipline_ — requiring the AI to articulate, before generating any code, which specific bug each test would catch. The filter must be applied before code is written, not during a post-hoc review.

### 2. TDD Iron Laws

[`references/tdd-iron-laws.md`](../../skills/test-master/references/tdd-iron-laws.md:1) establishes that production code must never exist without a prior failing test. Iron Law 2 ("If you didn't watch the test fail, you don't know if it tests the right thing") is philosophically adjacent to SDD Phase 4 mutation-testing verification.

**Why this is not enough:** TDD addresses human developers writing tests first. It does not model the specific failure mode of AI agents: an AI asked to "write tests for `DiscountService`" will generate passing tests immediately, skipping the red phase entirely, because it infers both the implementation and the assertion from the same context. SDD's phased prompting is the AI-specific answer to this.

### 3. MUST DO / MUST NOT Constraints in `SKILL.md`

[`SKILL.md`](../../skills/test-master/SKILL.md:74) contains strong foundational constraints:

- "Test happy paths AND error/edge cases"
- "Assert specific outcomes, not just truthiness"
- "Do not test implementation details — test observable behaviour"

These are correct. They partially overlap with SDD Phase 1 (enumerate boundary scenarios) and the general spirit of Phase 2.

---

## What Is Missing (Issues and Recommendations)

### 🔴 Issue 1: No SDD Phased Workflow

**Current state:** The Core Workflow in [`SKILL.md`](../../skills/test-master/SKILL.md:22) is: Define Scope → Create Strategy → Write Tests → Execute → Report. The skill jumps directly to writing tests.

**The gap:** SDD breaks this into explicit phases with _different goals per phase_ to prevent reward hacking:

| Phase            | Goal                                                           | Artifact               | Code?  |
| ---------------- | -------------------------------------------------------------- | ---------------------- | ------ |
| 1 — Use Cases    | Enumerate all scenarios (positive, negative, boundary)         | Approved scenario list | ❌ No  |
| 2 — Test Cases   | Translate scenarios to Given/When/Then; apply tautology filter | Approved test-case doc | ❌ No  |
| 3 — Code         | Implement tests exactly as approved; never alter assertions    | Test code              | ✅ Yes |
| 4 — Verification | Mutation check, mock isolation check, assertion accuracy check | Verified test suite    | —      |

**Why it matters:** An AI receiving "write tests for `DiscountService`" will simultaneously infer the implementation and write tests that match its inference. Both the test and the assertion emerge from the same mental model, producing tests that _cannot fail_ — a form of reward hacking. Separating phases forces the AI to commit to scenarios and expected behaviors _before_ it sees any implementation, giving the human a checkpoint to catch missing edge cases.

**Recommendation:** Add a new reference file `references/sdd-ai-workflow.md` (see Section 4) and add a callout in [`SKILL.md`](../../skills/test-master/SKILL.md:22) that directs AI agents to this workflow when generating tests for a service or module.

---

### 🔴 Issue 2: No Anti-Reward-Hacking Constraint

**Current state:** [`SKILL.md`](../../skills/test-master/SKILL.md:80) MUST NOT section has no prohibition against modifying assertions or test data to achieve passing tests.

**The gap:** AI agents exhibit reward hacking when asked to "make the tests pass": they modify the assertion (`expect(result).toBe(90)` → `expect(result).toBe(85)`) or alter fixture data rather than reporting a discrepancy between the implementation and the spec. This produces a green CI that hides a real bug.

**Recommendation:** Add to the MUST NOT section:

```
- Modify assertions, expected values, or test fixtures to make a failing test pass —
  if a test fails, report the discrepancy between actual output and the test-case spec;
  never silently alter the assertion
```

This constraint should also appear as a **system-prompt fragment** that engineers can copy into their AI assistant configuration.

---

### 🔴 Issue 3: No Tautology Filter

**Current state:** The testing anti-patterns reference flags mock-behavior testing as a smell, but only at the code-review stage, after tests are already written.

**The gap:** The SDD tautology filter is applied _before code is written_, during Phase 2. The rule is:

> For each test case, state which specific bug it would catch if the business logic broke.  
> If you cannot name a bug → the test case is not needed.

This eliminates:

- Tests that only verify mock setup ("the mock returned what I put into it")
- Tests that tautologically assert the implementation instead of the specification
- Tests whose only purpose is to inflate coverage numbers

**Recommendation:** Add this as a named concept in the new `references/sdd-ai-workflow.md` and as a bullet point in the MUST DO section of [`SKILL.md`](../../skills/test-master/SKILL.md:74):

```
- Before writing any test code, articulate the specific business-logic bug each test
  would catch; discard test cases where no such bug can be named
```

---

### 🟡 Issue 4: No Mutation Testing Verification

**Current state:** No reference file covers mutation testing. The TDD iron laws include "If you didn't watch the test fail, you don't know if it tests the right thing," but this is a process note, not a mechanical check.

**The gap:** SDD Phase 4 includes a mutation test: "If you replace `>` with `>=`, will the test fail?" This is the minimal mechanical verification that an assertion is load-bearing. A test that passes regardless of an off-by-one change in the implementation is providing false confidence.

**Recommendation:** Add a mutation-testing section to the new `references/sdd-ai-workflow.md` with:

- The off-by-one mutation check as the default quick validation
- A reference to formal mutation testing tools (Stryker for JS/TS, mutmut for Python) for teams that want full coverage
- The principle: a test that cannot detect the simplest mutation has no diagnostic value

---

### 🟡 Issue 5: Few-Shot Example Is Present but Not Emphasized as an AI Prompting Strategy

**Current state:** [`SKILL.md`](../../skills/test-master/SKILL.md:36) contains a Quick-Start Example — a well-written Jest snippet. This is good.

**The gap:** The skill does not explain _why_ this example is there in terms of AI prompting. The SDD wisdom states that providing one good test from the actual project ("few-shot") outperforms any amount of abstract instruction. Engineers should be explicitly told to inject a project-specific example into every AI test-generation prompt.

**Recommendation:** Add a note to the Quick-Start Example section:

```
> **AI Prompting Tip:** When generating tests with an AI assistant, paste one test
> from your own codebase as a style example. Few-shot examples override abstract
> instructions and produce significantly better adherence to project conventions.
```

---

### 🟡 Issue 6: No AI System-Prompt Templates

**Current state:** The skill contains constraints and examples but no reusable prompt fragments for AI-assisted workflows.

**The gap:** The SDD workflow calls for specific system-prompt constraints:

- "Do not modify test data or fixtures to pass tests. If a test fails, report the discrepancy."
- "List use cases first. Do not write code until scenarios are approved."

Without these being codified as copy-paste prompt fragments, engineers are unlikely to apply them consistently.

**Recommendation:** Add a section to the new reference file with system-prompt templates.

---

### 🟢 Issue 7: No Reference to SDD Tooling

**Current state:** No reference to Spec Kit or OpenSpec.

**The gap:** [Spec Kit (GitHub)](https://github.com/) and OpenSpec (Fission-AI) are open-source tools that implement the SDD 4-phase flow (Specify → Plan → Tasks → Implement) for AI agents. They remove the need for manual prompt engineering of the phases.

**Recommendation:** Add a brief tooling section in `references/sdd-ai-workflow.md`.

---

## Proposed Additions

### Addition 1: New Reference File `references/sdd-ai-workflow.md`

Create [`skills/test-master/references/sdd-ai-workflow.md`](../../skills/test-master/references/sdd-ai-workflow.md) covering:

1. The 4-phase SDD process with Given/When/Then templates
2. The tautology filter with examples
3. The anti-reward-hacking constraint with examples (assertion modification vs. discrepancy reporting)
4. Mutation testing verification checklist
5. AI system-prompt templates for each phase
6. Tooling references (Spec Kit, OpenSpec)

**Load When:** "AI-assisted test generation, spec-driven development, preventing AI reward hacking in tests"

---

### Addition 2: Updates to `SKILL.md`

**A. Add to Reference Guide table:**

```markdown
| SDD AI Workflow | `references/sdd-ai-workflow.md` | AI-assisted test generation, reward hacking prevention |
```

**B. Add to MUST DO:**

```markdown
- When using AI to generate tests: enumerate use cases _before_ writing any code
- For each test case, state which specific bug it would catch; discard if unanswerable
- Provide one project-specific test as a few-shot style example in every AI prompt
```

**C. Add to MUST NOT:**

```markdown
- Modify assertions, expected values, or test fixtures to make a failing test pass —
  report the discrepancy instead
- Ask AI to "write tests" without first agreeing on use cases and test cases
```

---

## Final Assessment

The `test-master` skill is well-grounded in classical quality engineering: TDD iron laws, anti-patterns, and coverage methodology. These are all valid and should be retained.

What it currently lacks is an AI-aware layer. The SDD methodology exists precisely because AI agents fail in ways that human developers do not: they optimize for passing tests rather than for correct specifications, they conflate implementation with expectation, and they are vulnerable to reward hacking at the assertion level. None of these failure modes appear in the current references.

The required changes are additive, not structural — a new reference file and targeted additions to the constraints section. The existing content does not need to be modified, only supplemented.

**Priority order for implementation:**

1. 🔴 Add anti-reward-hacking constraint to `SKILL.md` MUST NOT — one sentence, immediate impact
2. 🔴 Add tautology filter to `SKILL.md` MUST DO — one sentence, prevents empty test suites
3. 🔴 Create `references/sdd-ai-workflow.md` — full 4-phase process, system-prompt templates
4. 🟡 Add mutation testing section to new reference
5. 🟡 Add few-shot emphasis note to Quick-Start Example
6. 🟢 Add tooling references (Spec Kit, OpenSpec)

---

_Report saved as required by reviewer mode. Next action: implement proposed additions or hand off to Code mode._
