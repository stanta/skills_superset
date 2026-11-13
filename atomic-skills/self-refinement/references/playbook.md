# Self Refinement: engineering playbook

## DSPy mechanism

**BestOfN, Refine**. Verify actual imports, signatures and optimizer requirements against the installed DSPy release before writing production code.

## Implementation recipe

### Step 1

Determine which output mistakes can be detected by independent validators.

### Step 2

Choose BestOfN for competing candidates or Refine for iterative feedback.

### Step 3

Set strict attempt, token, time and budget ceilings with explicit stop reasons.

### Step 4

Generate only side-effect-free candidates; never repeat purchases, sends or deployment actions.

### Step 5

Evaluate candidates with frozen validators; prevent reflection from modifying scoring rules.

### Step 6

Return the best validated candidate or abstain and report failed attempts.


## Examples and completion criteria

Example request: "Use self-refinement to improve one bounded AI component, with a frozen baseline, versioned examples and measured acceptance criteria."

- Required input: Task with a stable verifiable scoring/checking function
- Required input: Maximum attempts, cost/latency budget and side-effect classification

- Acceptance: Exactly bounded attempts and a deterministic stopping rule.
- Acceptance: No external side effect is retried without explicit idempotency and authorization.

Return **Best candidate, validation evidence, attempts trace and bounded cost accounting.**

## Anti-patterns

- Optimizing on the final test set or treating generated examples as independently verified.
- Giving an optimizer or generated code permission to alter evaluator, policy, production resources or user approvals.
- Reporting only successful attempts while omitting failures, costs and uncertainty.
- Assuming DSPy changes the underlying foundation model weights.

## Fallback

When the library cannot be installed or API support is uncertain, supply the contract, test cases, decision criteria and runnable design rather than pretending the optimizer ran.
