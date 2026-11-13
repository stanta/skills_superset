# Bounded refinement patterns

## Candidate selection versus repair

DSPy `BestOfN` makes bounded attempts and selects an acceptable/high-reward output. `Refine` additionally uses feedback to guide subsequent attempts. Neither mechanism proves truth, and a selected best candidate may still be below the required acceptance level. Check that condition explicitly in application code.

Keep `N`, threshold, per-attempt token limit, total model-call/currency limit and timeout separate. Judge calls and repair calls count toward the budget. Inspect caching/rollout settings so repeated calls are not mistaken for independent samples.

## External checks

For structured extraction, validate schema and evidence spans. For code, run scoped tests in isolation. For a cited answer, verify the cited passage supports each claim. A model judge may supplement these checks after calibration but should not replace deterministic access control or domain review.

Preserve the initial candidate and all error statuses; reject a later revision that fixes formatting but invents facts. Test repeated invocation and concurrency with the installed library rather than assuming a wrapper is stateless. Execute side effects only once, after selection and authorization, with application idempotency controls.

## Source

Checked 2026-11-13. Original operating procedure with version-sensitive DSPy mapping:

- https://dspy.ai/3.1.2/tutorials/output_refinement/best-of-n-and-refine/
- https://dspy.ai/current/api/modules/BestOfN/
- https://dspy.ai/current/api/modules/Refine/

The versioned tutorial explains the pattern; verify current signatures and behavior before use.
