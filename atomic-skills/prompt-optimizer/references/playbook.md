# Prompt Optimizer: engineering playbook

## DSPy mechanism

**GEPA, MIPROv2**. Verify actual imports, signatures and optimizer requirements against the installed DSPy release before writing production code.

## Implementation recipe

### Step 1

Measure the unoptimized baseline and determine whether errors are prompt-related.

### Step 2

Select GEPA for reflective feedback-driven improvement, or MIPROv2 for joint instruction and demonstration search.

### Step 3

Freeze evaluation code, hard constraints, data access, authorization and permitted optimizer surface.

### Step 4

Run compilation offline using only training data and validation feedback, with explicit spending limits.

### Step 5

Inspect generated instructions for leaked answers, reward hacking, unsupported claims and policy bypasses.

### Step 6

Select by validation; evaluate once on untouched test data and send candidate to regression gate.


## Examples and completion criteria

Example request: "Use prompt-optimizer to improve one bounded AI component, with a frozen baseline, versioned examples and measured acceptance criteria."

- Required input: Frozen task and baseline, train/validation data, sealed tests
- Required input: Metric, optimizer budget, allowed modification surface and provenance

- Acceptance: No test-set leakage or modification of authorization policy.
- Acceptance: Reported improvement includes all judge/reflection calls and an independent test result.

Return **Versioned optimized program, prompt diff, configuration, candidate trace and evaluation evidence.**

## Anti-patterns

- Optimizing on the final test set or treating generated examples as independently verified.
- Giving an optimizer or generated code permission to alter evaluator, policy, production resources or user approvals.
- Reporting only successful attempts while omitting failures, costs and uncertainty.
- Assuming DSPy changes the underlying foundation model weights.

## Fallback

When the library cannot be installed or API support is uncertain, supply the contract, test cases, decision criteria and runnable design rather than pretending the optimizer ran.
