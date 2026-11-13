# Agent Architecture Evolver: engineering playbook

## DSPy mechanism

**Flex, GEPA**. Verify actual imports, signatures and optimizer requirements against the installed DSPy release before writing production code.

## Implementation recipe

### Step 1

Identify an architecture limitation and start from the smallest working module.

### Step 2

Specify which code paths, number of calls or composition graph may be changed.

### Step 3

Run Flex/GEPA experiments only with isolated credentials, no production network and resource quotas.

### Step 4

Lint, type-check and test every generated candidate; inspect dependency and tool changes.

### Step 5

Reject policy bypass, data exfiltration, dynamic untrusted imports and unbounded execution.

### Step 6

Compare against original on sealed tests and require human-reviewed change before deployment.


## Examples and completion criteria

Example request: "Use agent-architecture-evolver to improve one bounded AI component, with a frozen baseline, versioned examples and measured acceptance criteria."

- Required input: Frozen baseline, target metrics and permitted architecture/search surface
- Required input: Isolated build/test environment, hard execution/time/cost budgets

- Acceptance: Generated code has no production credentials and no direct deployment authority.
- Acceptance: Measured gains outweigh additional complexity and all regressions are independently checked.

Return **Architecture diff, candidate provenance, sandbox logs and independent evaluation report.**

## Anti-patterns

- Optimizing on the final test set or treating generated examples as independently verified.
- Giving an optimizer or generated code permission to alter evaluator, policy, production resources or user approvals.
- Reporting only successful attempts while omitting failures, costs and uncertainty.
- Assuming DSPy changes the underlying foundation model weights.

## Fallback

When the library cannot be installed or API support is uncertain, supply the contract, test cases, decision criteria and runnable design rather than pretending the optimizer ran.
