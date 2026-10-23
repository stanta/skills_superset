# Sources and Evidence Limits

Research snapshot: 2026-10-23. These are primary engineering sources and research summaries; use their methods proportionally.
The combined review workflow is a practical synthesis, not a validated scoring model or a guarantee of lower lifetime cost.

| Source | Supported idea | Evidence and limits |
| --- | --- | --- |
| [Google: What to look for in a code review](https://google.github.io/eng-practices/review/reviewer/looking-for.html) | Check unnecessary generality, future-only functionality and readability at several levels | Organizational engineering guidance, not a comparison proving one design style superior |
| [Google: The Standard of Code Review](https://google.github.io/eng-practices/review/reviewer/standard.html) | Improve overall code health without blocking progress for perfection | Context-dependent judgment; style preferences should not become invented requirements |
| [Google: Small CLs](https://google.github.io/eng-practices/review/developer/small-cls.html) | Review coherent changes with actual usage of new APIs | No universal numeric size limit |
| [Martin Fowler: Yagni](https://martinfowler.com/bliki/Yagni.html) | Account for speculative functionality and its continuing maintenance cost; preserve changeability | Practitioner reasoning; refactoring and necessary current quality attributes remain legitimate work |
| [Kent C. Dodds: AHA Programming](https://kentcdodds.com/blog/aha-programming) | Avoid premature abstractions and rigid repetition thresholds | Engineering heuristic, not evidence that duplication always wins |
| [John Ousterhout: Modular Design](https://web.stanford.edu/~ouster/cgi-bin/cs190-winter18/lecture.php?topic=modularDesign) | Evaluate information hiding and useful interface depth | Author's design framework; module size alone is not its objective |
| [DORA: Working in small batches](https://dora.dev/capabilities/working-in-small-batches/) | Short feedback loops and reviewable changes, including AI-assisted work | Research-backed capability guidance; association does not rank all architecture choices causally |
| [Uber: AI-assisted code cleanup](https://www.uber.com/us/en/blog/ai-code-cleanup/) | Independently inspect scope, retained behavior and test integrity after automated cleanup | First-party case study; reviewer agents and passing CI are not formal correctness proofs |
| [Microsoft Research: The SPACE of Developer Productivity](https://www.microsoft.com/en-us/research/publication/the-space-of-developer-productivity-theres-more-to-it-than-you-think/) | Assess outcomes across multiple dimensions rather than a single activity metric | Framework for productivity measurement; it does not supply a universal simplicity score |

## Applying the evidence

- Support each review finding with evidence from the reviewed change, not only a citation to a principle.
- Describe anticipated maintenance improvements as hypotheses until observed.
- Prefer current behavior, change radius, review/rework and operational outcomes over line-count or abstraction-count quotas.
- Recheck evolving tool behavior before recommending a particular automated fixer or CI integration.
