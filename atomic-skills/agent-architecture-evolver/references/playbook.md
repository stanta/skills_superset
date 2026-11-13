# Experimental architecture search

## Change envelope

Allowed examples: combine two redundant model calls, add a deterministic validator, change bounded aggregation, or select among existing modules. Protected surfaces: evaluator and labels, held-out cases, access policy, approval logic, secrets, deployment workflow, budget enforcement and dependency allowlist. Define the envelope before generating candidates and enforce it outside the optimizer.

## Optional DSPy Flex

Current DSPy documentation describes `Flex` as a module whose source code can be optimized with GEPA. Check that the installed version exposes the needed class, code-optimization path and interpreter factory. A legacy DSPy environment may not support them. Do not silently upgrade a production dependency or substitute unrestricted execution.

Validate generated code and run it through an approved interpreter/sandbox. Even with a sandbox, exposed tools need independent authorization and resource limits. A candidate that fails to compile or execute is a failed experiment, not a reason to weaken tests. Record whole-program quality, critical slices, total calls and complexity; more code is not automatically an improvement.

## Promotion record

Keep source and artifact hashes, dependency lock, test/scorer hashes, sandbox configuration, resource usage, reviewed diff, rollback identifier and approval status. Rebuild and verify the candidate outside the optimizer before promotion. With no trustworthy execution environment, deliver static proposals and explicitly mark all runtime claims untested.

## Primary source

Checked 2026-11-13; original protected-search procedure:

- https://dspy.ai/current/diving-deeper/flex/

No upstream runtime or generated code is imported by this skill package.
