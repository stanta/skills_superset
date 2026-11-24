# Spec-Driven Development (SDD) for AI-Assisted Test Generation

<!-- SDD methodology synthesized from conference talk notes, MIT License compatible -->

---

## Why AI Needs a Different Workflow

Classical TDD requires a human to write a failing test, observe the failure, then implement. AI agents skip this cycle: given "write tests for `UserService`", an agent infers the implementation and the assertion from the same context — producing tests that **cannot fail** because the expectation is derived from the same model as the code. This is **reward hacking**: the goal "green tests" is achieved without testing anything meaningful.

SDD (Spec-Driven Development) reduces one reward-hacking opportunity by assigning **different goals to different phases**. It still requires independent expected outcomes and a validated evaluator. An agent optimising for Phase 1 (enumerate scenarios) cannot simultaneously optimise for Phase 3 (green code), because Phase 1 explicitly forbids writing code.

---

## The Four Phases

### Phase 1 — Use Cases (no code)

**Prompt pattern:**

```
Analyse [ServiceName] (code below).
List all usage scenarios, including:
- Positive (happy path)
- Negative (invalid input, wrong type, missing fields)
- Boundary (threshold values, empty collections, null, zero)

For each scenario provide:
- Input data
- Expected result
- Preconditions

Do NOT write any code yet.
```

**Expected size:** As many scenarios as the risk and actual behavior require; avoid filler.

**Human checkpoint:** Seek review when requirements, expected results or safety constraints are uncertain; otherwise record assumptions and continue.

- Are all boundary values covered (min, max, min−1, max+1)?
- Are all error paths enumerated (null, empty, negative, overflow)?
- Add any scenario the AI missed before moving to Phase 2.

---

### Phase 2 — Test Cases in Given/When/Then (no code)

**Prompt pattern:**

```
For each approved scenario, write a test case in Given/When/Then format.
For each test case, add one line: "This test catches: [specific bug description]."
If you cannot name a specific bug this test would catch → omit the test case.
Do NOT write any code yet.
```

**The tautology filter:** The requirement "name the bug" eliminates:

- Tests that only verify mock setup (`"the mock returned what I put into it"`)
- Tests tautologically asserting the implementation (`"calling getUser returns a User"`)
- Coverage-inflating tests with no diagnostic value

**Example — passes the filter:**

```
Given: a premium user and a price of 100
When: calculateDiscount is called
Then: returns 90
This test catches: a bug where the premium discount is applied at the wrong rate,
or not applied at all.
```

**Example — fails the filter and should be dropped:**

```
Given: discountRepository.getRate is mocked to return 0.1
When: calculateDiscount is called
Then: discountRepository.getRate was called once
This test catches: [cannot be named — it only verifies mock wiring]
```

---

### Phase 3 — Code

**Prompt pattern:**

```
Write test code for the approved test cases. Constraints:
1. Do NOT modify test data, fixtures, or expected values to make a test pass.
2. If a test fails, report the discrepancy between actual output and the test-case spec.
   Do NOT fix the test by changing the assertion.
3. Follow the style of this example: [paste one test from your project here]
4. Do not introduce helpers or abstractions that do not appear in the example.
```

**Anti-reward-hacking constraint explained:**

Without constraint #1, an AI agent will silently change `expect(result).toBe(90)` to `expect(result).toBe(85)` when the service returns 85. The test becomes green; the bug disappears from CI; production is wrong. The fix is explicit: _report, never alter_.

**System-prompt fragment (paste into your AI assistant settings):**

```
When generating or editing tests:
- Never modify assertions, expected values, or fixtures to achieve a passing test.
- If a test fails, output a discrepancy report: expected [X], got [Y], possible root cause.
- New discovered risks may justify additional tests: update and review their acceptance cases first; never secretly weaken an existing assertion to get green.
```

---

### Phase 4 — Verification

For each generated test, verify three properties before merging:

#### 4.1 Real Logic Check

> Does the test call the actual service logic, or is it closed over a mock?

❌ Closed over mock — no real logic exercised:

```typescript
it("returns discounted price", () => {
  const mockCalc = jest.fn().mockReturnValue(90);
  expect(mockCalc(100)).toBe(90); // only tests the mock
});
```

✅ Real logic exercised:

```typescript
it("applies 10% discount for premium users", () => {
  const result = calculateDiscount({ price: 100, userTier: "premium" });
  expect(result).toBe(90); // calls real function
});
```

#### 4.2 Assertion Accuracy

> Does the assertion match exactly what the Phase 2 test case specified?

Check: expected value, type, error message string (if testing throws), and any side-effect assertions.

#### 4.3 Mutation Test (minimal)

> If you change `>` to `>=` (or `<` to `<=`, or `===` to `!==`) in the implementation, does the test fail?

A surviving mutation may reveal a missing boundary case, an invalid mutation, or equivalent behavior. Classify it before tightening assertions.

**Quick mutation checklist:**

```
[ ] Flip one comparison operator in the service → does the test turn red?
[ ] Remove the discount calculation entirely → does the test turn red?
[ ] Return a hardcoded value → does the test turn red?
If a mutation survives, first decide whether it is applicable and behavior-changing; only then improve the relevant test.
```

---

## System-Prompt Templates

### Minimal (one-liner, add to every test-generation session)

```
Never modify assertions or test data to pass tests. If a test fails, report the discrepancy.
```

### Standard (for a full SDD session)

```
We are following Spec-Driven Development. Keep phases traceable; request approval only for material uncertainty or high-risk contract decisions.
Phase 1: enumerate use cases (positive, negative, boundary). No code.
Phase 2: write Given/When/Then test cases. For each, name the specific bug it catches. No code.
Phase 3: write test code exactly matching Phase 2. Never alter assertions. Report failures.
Phase 4: verify each test — real logic, correct assertion, mutation resilience.
```

### Anti-reward-hacking addendum

```
You are forbidden from:
- Modifying expected values in assertions to match actual output.
- Adding try/catch blocks that swallow assertion errors.
- Changing fixture data so that the implementation produces the expected value.
If a test fails, output: TEST DISCREPANCY — [test name]: expected [value], received [value].
```

---

## Practical Checklist

**Before starting Phase 1**

- [ ] Have the service code and its public API visible
- [ ] Know the business rules (especially boundary values)

**After Phase 1**

- [ ] All positive flows covered
- [ ] All documented error conditions listed
- [ ] Boundary values: min, max, min−1, max+1, zero, null, empty collection

**After Phase 2**

- [ ] Every test case has a named bug it would catch
- [ ] No tautological test cases remain
- [ ] All Phase 1 scenarios have a corresponding test case

**After Phase 3**

- [ ] No assertion was altered compared to Phase 2
- [ ] All failing tests were reported as discrepancies, not silently fixed

**After Phase 4**

- [ ] Every test calls real service logic
- [ ] Every off-by-one mutation causes at least one test to fail
- [ ] Assertions match Phase 2 spec exactly

---

## Tooling

| Tool                                                            | Purpose                                                     | License     |
| --------------------------------------------------------------- | ----------------------------------------------------------- | ----------- |
| [Spec Kit](https://github.com/SpecKit/spec-kit)                 | Guides AI agents through Specify → Plan → Tasks → Implement | Open source |
| [OpenSpec (Fission-AI)](https://github.com/fission-ai/openspec) | Turns a spec into a living document with delta markers      | Open source |
| [Stryker](https://stryker-mutator.io/)                          | Mutation testing for JavaScript / TypeScript                | Apache 2.0  |
| [mutmut](https://github.com/boxed/mutmut)                       | Mutation testing for Python                                 | MIT         |

---

## Why This Works

SDD **reduces** the risk of reward hacking by separating objectives; it does not guarantee independent or correct test oracles:

- Phase 1 goal: completeness of scenario list
- Phase 2 goal: quality of bug-catching articulation
- Phase 3 goal: code that matches the approved spec
- Phase 4 goal: mechanical verification of test strength

No single phase has "green tests" as its goal. An agent can still bias expectations or weaken acceptance criteria. Ground oracles in independently reviewed requirements and evaluator-owned hidden checks.

The process can increase planning and token cost. Measure success, review effort and regression risk in controlled trials before claiming an efficiency improvement.
