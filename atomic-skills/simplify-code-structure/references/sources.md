# Sources and Evidence Limits

Use these primary sources to examine a particular tradeoff. The workflow is an
engineering synthesis; no source establishes a universal percentage improvement
or a mandatory threshold for lines, classes, or repeated uses.
Sources reviewed: 2026-10-23.

- **Kent C. Dodds, AHA Programming.** Delay premature abstraction until real
  variants are understood. The article credits Cher Scarlett for the AHA name
  and explicitly cautions against rigid DRY/WET rules.
  https://kentcdodds.com/blog/aha-programming
- **Dave Thomas and Andy Hunt, The Pragmatic Programmer: The Evils of Duplication.**
  Apply DRY to duplicated knowledge and intent, including situations where one
  fact requires coordinated changes in several representations.
  https://media.pragprog.com/titles/tpp20/dry.pdf
- **Sandi Metz, The Wrong Abstraction.** Consider inlining a shared mechanism
  that has combined unrelated ideas, then rediscover the real commonality.
  Treat the article as expert experience, not a rule that all conditionals fail.
  https://sandimetz.com/blog/2016/1/20/the-wrong-abstraction
- **Martin Fowler, Beck Design Rules.** Prioritize working behavior and clear
  intention alongside removing duplicated logic and unnecessary elements.
  https://martinfowler.com/bliki/BeckDesignRules.html
- **John Ousterhout, Stanford CS190: Modular Design.** Evaluate information
  hiding and interface cost; inspect shallow classes and pass-through layers.
  https://web.stanford.edu/~ouster/cgi-bin/cs190-winter18/lecture.php?topic=modularDesign
- **Jimmy Bogard, Vertical Slice Architecture.** Group along the axis of change;
  choose patterns according to each use case and keep the ability to refactor.
  This is the author's engineering experience, not a requirement for all systems.
  https://www.jimmybogard.com/vertical-slice-architecture/
- **Gary Bernhardt, Functional Core, Imperative Shell.** Separate deterministic
  computation from external effects where it makes state and tests clearer.
  https://www.destroyallsoftware.com/screencasts/catalog/functional-core-imperative-shell
- **Daniel Terhorst-North, CUPID: for joyful coding.** Evaluate composability,
  clear purpose, predictability, idiomatic code, and domain-aligned structure as
  contextual properties rather than rigid compliance rules.
  https://dannorth.net/blog/cupid-for-joyful-coding/
- **Google Testing Blog, Test Behavior, Not Implementation.** Keep checks
  independent of internal structure where possible; retain implementation checks
  when the mechanism itself expresses a requirement.
  https://testing.googleblog.com/2013/08/testing-on-toilet-test-behavior-not.html
- **Google Engineering Practices, Small CLs.** Keep changes coherent and
  reviewable; include a new interface with its use and relevant tests.
  https://google.github.io/eng-practices/review/developer/small-cls.html
