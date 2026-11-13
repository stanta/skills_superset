# Task Contract Designer: engineering playbook

## DSPy mechanism

**Signature, InputField, OutputField**. Verify actual imports, signatures and optimizer requirements against the installed DSPy release before writing production code.

## Implementation recipe

### Step 1

Identify user intent, decision boundary, side effects, permitted data and the exact measurable output.

### Step 2

Design a small typed DSPy Signature with meaningful input and output fields; distinguish required from optional.

### Step 3

Specify schema validation, input preconditions and deterministic postconditions outside the model.

### Step 4

Add a failure/abstention output for missing information; do not manufacture a result.

### Step 5

Build positive, invalid, ambiguous and prompt-injection examples.

### Step 6

Validate the schema on examples and hand it to the evaluation engineer before optimization.


## Examples and completion criteria

Example request: "Use task-contract-designer to improve one bounded AI component, with a frozen baseline, versioned examples and measured acceptance criteria."

- Required input: Task description, consumers and authoritative policy constraints
- Required input: Representative successful and failing examples

- Acceptance: Field names, formats and required evidence are explicit and machine-checkable.
- Acceptance: Safety/authorization constraints are enforced independently of LLM outputs.

Return **Versioned input/output schema, examples, invariants, failure contract and validation report.**

## Anti-patterns

- Optimizing on the final test set or treating generated examples as independently verified.
- Giving an optimizer or generated code permission to alter evaluator, policy, production resources or user approvals.
- Reporting only successful attempts while omitting failures, costs and uncertainty.
- Assuming DSPy changes the underlying foundation model weights.

## Fallback

When the library cannot be installed or API support is uncertain, supply the contract, test cases, decision criteria and runnable design rather than pretending the optimizer ran.
