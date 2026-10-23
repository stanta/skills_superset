# Sources and Evidence Limits

Research snapshot: 2026-10-23. Use these primary sources for rationale; recheck current tool interfaces before giving tool-specific commands.
The workflow is an engineering synthesis. These sources do not establish a universal percentage improvement from deleting code.

| Source | Supported idea | Evidence and limits |
| --- | --- | --- |
| [Meta Engineering: Automating dead code cleanup](https://engineering.fb.com/2023/10/24/data-infrastructure/automating-dead-code-cleanup/) | Combine static dependency graphs with runtime and dynamic-use information | Industrial case study of Meta's environment; its results do not prove that a local search alone establishes non-use |
| [Uber Engineering: AI-assisted code cleanup](https://www.uber.com/us/en/blog/ai-code-cleanup/) | Continuously clean stale flags; combine deterministic transforms, CI and separate checks of scope and semantics | First-party report published 2026-10-20; automated validation and human review remain fallible, not a formal equivalence proof |
| [DORA: Code maintainability](https://dora.dev/capabilities/code-maintainability/) | Make code discoverable and dependencies manageable; track unused code and dependency costs | Research-backed capability guidance; do not turn an unused-code metric into a deletion quota |
| [Google Testing Blog: Test Behavior, Not Implementation](https://testing.googleblog.com/2013/08/testing-on-toilet-test-behavior-not.html) | Preserve tests of observable contracts during internal changes | Practitioner guidance; some implementation checks are justified by explicit requirements |
| [Google Engineering Practices: Small CLs](https://google.github.io/eng-practices/review/developer/small-cls.html) | Keep changes coherent and reviewable, with their relevant tests and context | Organizational guidance; no universal line-count threshold |

## Interpretation

- Treat cleaner code and reduced configuration as intermediate results; evaluate maintenance cost and regressions as outcomes.
- Preserve lifecycle distinctions: rollout scaffolding, operational control and user entitlement serve different purposes.
- Use independent review to challenge a cleanup result, not to declare it correct merely because another model agrees.
- Keep source-specific examples separate from product assumptions; do not import Uber's or Meta's infrastructure into a small repository.
