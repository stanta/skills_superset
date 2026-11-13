# AI Regression Gate: engineering playbook

## DSPy mechanism

**Evaluate, versioned artifacts**. Verify actual imports, signatures and optimizer requirements against the installed DSPy release before writing production code.

## Implementation recipe

### Step 1

Verify immutable identity of model, prompt/program, dataset, metric and source corpus versions.

### Step 2

Reject missing, stale, partial, leakage-affected or unverifiable evidence.

### Step 3

Evaluate non-negotiable safety and critical slice conditions before aggregate scores.

### Step 4

Compare candidate quality, cost and latency against the baseline with predefined tolerances.

### Step 5

Produce deterministic pass/fail/insufficient-evidence with reasons and retained artifacts.

### Step 6

Submit result to independent CI/OPA/human approval; never grant deployment permission itself.


## Examples and completion criteria

Example request: "Use ai-regression-gate to improve one bounded AI component, with a frozen baseline, versioned examples and measured acceptance criteria."

- Required input: Frozen baseline, versioned candidate and comparable sealed evaluation outputs
- Required input: Predeclared hard thresholds, evidence manifest and release approval policy

- Acceptance: Insufficient or missing evaluation evidence fails closed.
- Acceptance: A model's self-rating cannot override the independent policy gate.

Return **Machine-readable release evidence and independent deterministic gate decision.**

## Anti-patterns

- Optimizing on the final test set or treating generated examples as independently verified.
- Giving an optimizer or generated code permission to alter evaluator, policy, production resources or user approvals.
- Reporting only successful attempts while omitting failures, costs and uncertainty.
- Assuming DSPy changes the underlying foundation model weights.

## Fallback

When the library cannot be installed or API support is uncertain, supply the contract, test cases, decision criteria and runnable design rather than pretending the optimizer ran.
