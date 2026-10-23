# Sources and Evidence Limits

Use these primary sources for rationale, exceptions, and deeper discussion.
The workflow is an engineering synthesis, not a validated universal ranking.
Sources reviewed: 2026-10-23.

- **Martin Fowler, Yagni.** Use the distinction between speculative capabilities
  and maintaining the ability to change a system. Include carrying and delayed
  value costs when comparing building now with building later.
  https://martinfowler.com/bliki/Yagni.html
- **Mary and Tom Poppendieck, Lean Software Development: An Agile Toolkit.**
  Use learning, delayed commitment, delivery, integrity, and whole-system value
  as connected concerns rather than equating lean with less code.
  https://www.oreilly.com/library/view/lean-software-development/0321150783/
- **Martin Fowler, Monolith First.** Treat the recommendation as contextual
  engineering experience; the author explicitly discusses sparse evidence,
  counterarguments, and the difficulty of establishing stable boundaries.
  https://martinfowler.com/bliki/MonolithFirst.html
- **John Ousterhout, Stanford CS190: Modular Design.** Evaluate interface cost,
  information hiding, deep modules, and pass-through layers. Avoid interpreting
  the argument as a requirement for either tiny or giant classes.
  https://web.stanford.edu/~ouster/cgi-bin/cs190-winter18/lecture.php?topic=modularDesign
- **Dan McKinley, Choose Boring Technology.** Account for the system-wide
  operational and cognitive cost of an additional technology.
  https://mcfunley.com/choose-boring-technology
- **DORA, Loosely Coupled Teams; Working in Small Batches.** Use independence of
  change, test, and release and short feedback loops as outcomes. Observational
  findings do not prove that a named architecture is universally superior.
  https://dora.dev/capabilities/loosely-coupled-teams/
  https://dora.dev/capabilities/working-in-small-batches/
- **Neal Ford, Rebecca Parsons, Patrick Kua, Building Evolutionary Architectures.**
  Protect required architectural properties with incremental change and selected
  fitness functions; do not create checks merely to freeze today's structure.
  https://evolutionaryarchitecture.com/precis.html
- **Michael Nygard, Documenting Architecture Decisions.** Capture motivation and
  consequences in short records of significant decisions.
  https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions
- **W3C TAG, The Rule of Least Power.** Apply the choice of sufficient
  expressiveness to data and rule languages. Treat extension to general
  architecture as an analogy, and avoid a language too limited for the problem.
  https://www.w3.org/2001/tag/doc/leastPower.html
