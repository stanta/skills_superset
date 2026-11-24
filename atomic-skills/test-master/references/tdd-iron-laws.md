# TDD Iron Laws

---

## The Fundamental Principle

> **For new behavior, establish a failing test before implementing whenever practical.**

Do not delete existing code or user changes because tests were written later. Add characterization or regression tests to protect working behavior; mark any missing RED evidence explicitly.

---

## The Three Iron Laws

### Iron Law 1: The Fundamental Rule

> "You shall not write any production code unless it is to make a failing test pass."

For new behavior, prefer a focused test that:
1. Defines an externally grounded expected result
2. Fails for the intended behavioral reason
3. Passes after the minimal fix

For legacy or already-written code, preserve work and add meaningful verification instead of restarting implementation.

### Iron Law 2: Proof Through Observation

> "If you didn't watch the test fail, you don't know if it tests the right thing."

Mandatory verification steps:
- Write the test
- Run it and **observe the failure**
- Verify the failure message is meaningful
- Only then implement the fix

A test not observed failing may still protect existing behavior; challenge its diagnostic strength with a targeted fault, mutation or prior-revision comparison when safe.

### Iron Law 3: The Final Rule

> "Production code exists → A test exists that failed first. Otherwise → It's not TDD."

If production code came first, state that test-first evidence is absent. This does not justify discarding work; use characterization/regression checks and report remaining gaps.

---

## The RED-GREEN-REFACTOR Cycle

### RED: Write One Minimal Failing Test

```typescript
// Start with the smallest possible failing test
it('should return 0 for empty array', () => {
  expect(sum([])).toBe(0);
});
// Run: ✗ FAIL - sum is not defined
```

**Requirements:**
- One test at a time
- Minimal scope
- Clear failure message
- Observe the red

### GREEN: Implement Simplest Passing Code

```typescript
// Write only enough code to pass this specific test
function sum(numbers: number[]): number {
  return 0;
}
// Run: ✓ PASS
```

**Requirements:**
- Simplest possible implementation
- No extra features
- No optimization
- Just make it pass

### REFACTOR: Improve While Keeping Tests Green

```typescript
// Now improve the code while tests stay green
function sum(numbers: number[]): number {
  return numbers.reduce((acc, n) => acc + n, 0);
}
// Run: ✓ PASS (still)
```

**Requirements:**
- Tests must stay green
- Remove duplication
- Improve clarity
- No new functionality

---

## Common Rationalizations to Reject

These thoughts indicate you're about to violate TDD:

| Rationalization | Why It's Wrong |
|-----------------|----------------|
| "I can manually test this quickly" | Manual testing doesn't prevent regression |
| "I'll write tests after to save time" | You'll skip edge cases and test implementation |
| "This is too simple to need a test" | Simple code changes; tests document expectations |
| "The existing code predates tests" | Preserve it; document current behavior and add regression checks |
| "I know this works, I've done it before" | Your memory isn't documentation |
| "We're in a hurry" | Technical debt costs more than TDD |

---

## Practical Application

### Starting a New Feature

```typescript
// 1. RED: Write failing test for simplest behavior
describe('UserValidator', () => {
  it('should reject empty email', () => {
    expect(validateEmail('')).toBe(false);
  });
});

// 2. GREEN: Implement minimal passing code
function validateEmail(email: string): boolean {
  return email.length > 0;
}

// 3. RED: Add next failing test
it('should reject email without @', () => {
  expect(validateEmail('invalid')).toBe(false);
});

// 4. GREEN: Extend to pass both tests
function validateEmail(email: string): boolean {
  return email.length > 0 && email.includes('@');
}

// Continue cycle...
```

### Fixing a Bug

```typescript
// 1. RED: Write test that exposes the bug
it('should handle negative numbers in sum', () => {
  expect(sum([-1, -2, -3])).toBe(-6);
});
// Run: ✗ FAIL - got 0 instead of -6

// 2. GREEN: Fix the bug
function sum(numbers: number[]): number {
  return numbers.reduce((acc, n) => acc + n, 0);
}
// Run: ✓ PASS

// Bug is now fixed AND protected against regression
```

---

## Verification Checklist

Before claiming any code is complete:

- [ ] Changed behavior has proportionate tests grounded in requirements
- [ ] RED evidence was captured for new work, or its absence documented for existing code
- [ ] Tests assert observable behavior and relevant effects, not only mocks
- [ ] No user or legacy work was deleted to manufacture RED
- [ ] Refactoring retained relevant regression coverage
- [ ] Unexecuted checks and limitations were reported

---

*Content adapted from [obra/superpowers](https://github.com/obra/superpowers) by Jesse Vincent (@obra), MIT License.*
