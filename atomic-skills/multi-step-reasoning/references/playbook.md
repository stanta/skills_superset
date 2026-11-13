# Multi-Step Reasoning: engineering playbook

## DSPy mechanism

**Module, Predict, ChainOfThought**. Verify actual imports, signatures and optimizer requirements against the installed DSPy release before writing production code.

## Implementation recipe

### Step 1

Prove whether a single-call baseline is insufficient.

### Step 2

Decompose only at observable failure boundaries with typed step outputs.

### Step 3

Implement minimal Module composition using Predict and optionally ChainOfThought.

### Step 4

Validate intermediate artifacts, propagate uncertainties and stop on hard failures.

### Step 5

Avoid logging or requesting private internal chain-of-thought; expose concise justifications instead.

### Step 6

Compare multi-step and single-step approaches on quality, latency, cost and simplicity.


## Examples and completion criteria

Example request: "Use multi-step-reasoning to improve one bounded AI component, with a frozen baseline, versioned examples and measured acceptance criteria."

- Required input: Task contract, baseline complexity/cost and failure taxonomy
- Required input: Explicit intermediate evidence and required deterministic validators

- Acceptance: Every added stage improves a measured failure class or is removed.
- Acceptance: Internal reasoning is not treated as proof and no hidden chain-of-thought is exposed.

Return **Minimal program graph, intermediate schemas, validation gates and A/B report.**

## Anti-patterns

- Optimizing on the final test set or treating generated examples as independently verified.
- Giving an optimizer or generated code permission to alter evaluator, policy, production resources or user approvals.
- Reporting only successful attempts while omitting failures, costs and uncertainty.
- Assuming DSPy changes the underlying foundation model weights.

## Fallback

When the library cannot be installed or API support is uncertain, supply the contract, test cases, decision criteria and runnable design rather than pretending the optimizer ran.
