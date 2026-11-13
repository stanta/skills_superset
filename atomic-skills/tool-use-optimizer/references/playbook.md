# Tool Use Optimizer: engineering playbook

## DSPy mechanism

**ReAct, Tool, MCP**. Verify actual imports, signatures and optimizer requirements against the installed DSPy release before writing production code.

## Implementation recipe

### Step 1

Map permitted tools to task contracts, least-privilege scopes and side-effect classes.

### Step 2

Instrument a baseline with tool selection, argument validation and stop reasons.

### Step 3

Construct sandbox fixtures for wrong tool, malformed arguments, failures and malicious tool output.

### Step 4

Evaluate ReAct or approved MCP tool adaptation under fixed tool permissions.

### Step 5

Optimize safe routing and recovery against trace-level metrics without expanding privileges.

### Step 6

Require confirmation/idempotency for irreversible actions; gate the candidate on held-out cases.


## Examples and completion criteria

Example request: "Use tool-use-optimizer to improve one bounded AI component, with a frozen baseline, versioned examples and measured acceptance criteria."

- Required input: Tool catalog with schemas, permissions, costs and side-effect classes
- Required input: Mock/sandbox fixtures and successful/unsafe action trajectories

- Acceptance: No tool call crosses the explicit authorization boundary.
- Acceptance: Mutating or external calls are not replayed during optimizer trials.

Return **Tool-use policy and test traces, schema checks, recovery plan and scorecard.**

## Anti-patterns

- Optimizing on the final test set or treating generated examples as independently verified.
- Giving an optimizer or generated code permission to alter evaluator, policy, production resources or user approvals.
- Reporting only successful attempts while omitting failures, costs and uncertainty.
- Assuming DSPy changes the underlying foundation model weights.

## Fallback

When the library cannot be installed or API support is uncertain, supply the contract, test cases, decision criteria and runnable design rather than pretending the optimizer ran.
