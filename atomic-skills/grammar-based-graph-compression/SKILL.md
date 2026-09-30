---
name: grammar-based-graph-compression
description: >-
  Use when designing, implementing, evaluating, or researching compression of
  labeled, directed, RDF, knowledge, semantic, or hypergraphs by repeated
  subgraph replacement, graph grammars, RePair/gRePair, SL-HR/HR grammars,
  SUBDUE/MDL substructure discovery, approximate graph-symbol dictionaries, or
  queryable compressed graph representations.
metadata:
  category: data-analytics
  last_verified: "2026-09-30"
---

# Grammar-based graph compression

## Mission

Build or assess a graph compressor in which repeated structure becomes reusable grammar rules rather than merely merged supernodes. Keep **compression**, **grammar induction/generation**, **graph summarization**, and **entropy coding** distinct.

Read:
- [methods and formalisms](references/methods-and-formalisms.md) before choosing a method;
- [engineering playbook](references/engineering-playbook.md) before implementation;
- [evaluation protocol](references/evaluation-and-experiments.md) before claiming compression or discovered structure;
- [sources](references/sources.md) for evidence provenance.

## Non-negotiable distinctions

1. **Lossless grammar compression:** one grammar expands to a graph isomorphic to the input.
2. **Approximate/lossy dictionary:** a symbol may represent a family; exact reconstruction then requires residuals/corrections.
3. **Grammar induction/generation:** learns a language/distribution of graphs; it is not automatically a compact encoding of one observed graph.
4. **Summarization:** may preserve chosen patterns or queries without being a grammar.
5. **Huffman/arithmetic coding:** codes already chosen symbols; it does not discover graph rules.
6. **A cluster ID is not a graph symbol.** Density/frequency methods propose candidates; canonical structure and interface semantics define a reusable symbol.

## Formal contract

For exact straight-line hyperedge-replacement compression, use an acyclic grammar

\[
\mathcal G=(N,P,S)
\]

whose nonterminal \(A\) has a fixed rank equal to the number of ordered external/attachment ports of its right-hand-side graph. Expanding the start graph must reproduce an isomorphic copy of the original graph.

Treat edge direction, edge/relation label, node label policy, multiplicity, self-loops, and port ordering as part of the representation contract.

## Workflow

1. **Specify the objective.** Storage bits/bytes, direct-query latency, structural discovery, or a Pareto combination. State lossless vs lossy before searching for motifs.
2. **Choose candidate discovery.** Exact digram replacement (gRePair), MDL-guided search (SUBDUE-like), query-oriented RePair (ITR-like), or an approximate proposal layer such as embeddings/WL/Wishart. Do not compare methods as if they optimize the same objective.
3. **Canonicalize candidates.** Preserve terminal labels/direction and external ports. WL/hash signatures are filters; if exact identity matters, verify canonical isomorphism or an equivalent exact certificate.
4. **Select occurrences.** Occurrences that share consumed edges/nodes cannot both be replaced under a non-overlap grammar. Optimize estimated coding gain, not raw frequency alone.
5. **Create a rule and replace occurrences.** Update only affected neighborhood statistics when possible. Prune rules whose references do not repay their definition cost.
6. **For approximate families, encode residuals.** Use
\[
L_{\mathrm{total}}=L(\mathcal G)+L(S\mid\mathcal G)+L(\text{ports})+L(\text{residuals}).
\]
Accept a family only when total description length decreases.
7. **Verify reconstruction/query semantics.** Decode and compare a canonical graph digest for lossless mode. Benchmark required queries directly on the grammar if queryability is part of the goal.

## Selection score

Prefer a coding-aware score such as

\[
\mathrm{Gain}(T,O)=
L_{\mathrm{raw}}(O)
-
\left[
L_{\mathrm{rule}}(T)+
L_{\mathrm{refs}}(O)+
L_{\mathrm{interfaces}}(O)+
L_{\mathrm{residuals}}(O)
\right].
\]

A frequent motif with large interfaces can be worse than a rarer compact motif.

## Semantic / knowledge graphs

For ConceptNet-like graphs, keep relation type and direction terminal. Separate a reusable **core shape** from occurrence-specific **interface variants** when that reduces total code length. Preserve original-node membership for reversibility.

For Wishart-assisted discovery: use Wishart as a density-based proposal mechanism over graph descriptors; map modes to persistent symbols only after structural/interface validation. Aggregate full-graph occurrence frequencies after discovery. Then apply Huffman/arithmetic coding only to the resulting symbol stream.

## Required deliverable

Return: objective and fidelity contract; chosen grammar formalism; candidate/matching/overlap strategy; exact coding equation; grammar + residual schema; reconstruction/query tests; actual bytes/bits and build memory/time; baselines; seed/order sensitivity; and explicit negative results.

Never claim that recursion alone proves a natural grammar, semantic primitive, fractality, or optimal compression.
