# Methods and formalisms for grammar-based graph compression

## 1. What counts as grammar-based compression

A grammar compressor does more than merge vertices. It identifies repeated graph fragments, assigns nonterminal symbols, replaces selected occurrences, and stores productions that reconstruct the fragments. A recursive sequence of replacements forms a derivation DAG.

A useful decomposition is:

\[
\text{candidate discovery}
\rightarrow
\text{matching/canonicalization}
\rightarrow
\text{occurrence selection}
\rightarrow
\text{rule creation}
\rightarrow
\text{replacement}
\rightarrow
\text{coding/query structures}.
\]

Different research families change different pieces of this pipeline.

## 2. Straight-line hyperedge-replacement grammars (SL-HR)

Hyperedge-replacement (HR) grammars replace a nonterminal hyperedge with a graph whose ordered external nodes are glued to the incident nodes of the replaced edge. The nonterminal's **rank** is the number of interface nodes.

A straight-line grammar is acyclic and has one production per nonterminal. In the compression setting it represents one graph up to isomorphism rather than a general language.

Why HR is useful for compression:

- the interface is explicit;
- nested rules form a compact hierarchy;
- directed and labeled edges can be terminals;
- repeated fragments can cross ordinary binary-edge boundaries while still exposing a bounded interface;
- some queries can be evaluated without full decompression.

The interface/rank is not bookkeeping noise. A fragment with many external nodes may be expensive to replace even when its internal topology repeats.

## 3. gRePair / graph RePair

Maneth & Peternek generalize string/tree RePair to directed edge-labeled hypergraphs.

Core idea:

1. a graph **digram** is a pair of connected hyperedges;
2. count non-overlapping occurrences;
3. pick a most frequent active digram;
4. introduce a fresh nonterminal whose rank equals the digram's external-node count;
5. replace chosen occurrences;
6. update occurrence lists;
7. repeat; then prune.

Important engineering facts from the paper:

- finding a maximum non-overlapping occurrence set is expensive, so the implementation uses a greedy approximation;
- node traversal order can materially change the compression ratio;
- a max-rank limit controls interface complexity and affects compression;
- rules referenced only once can be pruned;
- disconnected components can require special handling;
- reachability can be evaluated directly over the compressed grammar, and the extended journal work also studies regular-path queries.

Use gRePair when exact repeated local structure and lossless reconstruction are primary.

Do **not** infer that the most frequent digram is globally MDL-optimal.

## 4. SUBDUE: compression-guided substructure discovery

SUBDUE searches a broader subgraph space using beam search. Candidate structures are extended edge-by-edge and ranked by their ability to compress the graph using Minimum Description Length (MDL). Replacing discovered instances and rerunning the process yields hierarchical abstractions.

Strengths:

- discovery is not limited to two-edge digrams;
- MDL favors structures that explain data rather than frequency alone;
- it can use inexact matching with user-defined distortion costs.

Cautions:

- the search is heuristic/beam-limited;
- approximate matching needs a principled reconstruction-error code if one wants a true lossless or two-part MDL interpretation;
- replacing a substructure by a single vertex can obscure the full external-interface structure unless the representation explicitly stores it.

Use SUBDUE-like search when discovery/interpretability matters more than a pure RePair implementation.

## 5. ITR: query-oriented RePair

Incidence-Type-RePair (ITR) is a later grammar-based scheme for graphs with labeled nodes and labeled edges. Its design emphasizes compressed neighborhood and triple queries. The 2023 preprint and 2024 DCC publication report millisecond-scale query evaluation in their tested settings with compression sizes comparable to other graph compressors.

Use ITR-style design when node/edge labels and neighborhood/triple query latency are first-class requirements.

Do not transfer its reported performance to a new dataset without benchmarking.

## 6. HRG extraction for graph generation

Aguinaga, Chiang & Weninger learn/extract hyperedge-replacement grammars from graph decompositions and use them to generate graphs whose global and local properties resemble observed networks.

This is related but different:

- **compressor:** encode a specific graph compactly and, in lossless mode, recover it exactly;
- **generative HRG:** learn reusable production statistics and sample new graphs.

A stored extraction order can reproduce an isomorphic original graph in some HRG constructions, but stochastic rule application is a generative model, not a lossless compressed file.

## 7. Graph grammar induction

Graph grammar induction asks for a concise grammar that covers positive graph examples and optionally rejects negative examples. It may merge/generalize productions and use parsers during search.

This objective can be valuable for discovering a structural language, but it is not equivalent to minimizing the byte size of one graph.

## 8. MDL graph summarization is a neighboring baseline

VoG and other MDL summarizers use vocabularies such as stars, cliques, bipartite cores and chains plus corrections. These are useful baselines because they make the same information-theoretic question explicit:

\[
L(M)+L(G\mid M).
\]

However, a vocabulary summary is not necessarily a recursive graph grammar. Use it as a comparator or as a candidate generator, not as interchangeable terminology.

## 9. Method-selection table

| Goal | Strong starting point | Main caveat |
|---|---|---|
| Exact recursive compression | gRePair / SL-HR | Order, overlap approximation, rank/interface cost |
| Discover larger explanatory motifs | SUBDUE-like MDL search | Beam-search bias; approximate-error coding |
| Fast labeled neighborhood/triple queries | ITR-like grammar | Workload-specific; benchmark on target data |
| Generate similar graphs | learned/extracted HRG | Generation != compact exact encoding |
| Interpretable pattern summary | VoG/MDL summary | Not necessarily recursive or grammar-based |
| Approximate symbol families | metric/density proposal + residual grammar | Candidate similarity != symbol identity |

## 10. Boundary between exact and approximate rules

An exact rule has a single structural right-hand side under the chosen label/interface semantics:

\[
A(\mathbf p)\rightarrow H(\mathbf p).
\]

An approximate family should instead be modeled as

\[
o_i = \mathrm{prototype}(A) + \Delta_i,
\]

where \(\Delta_i\) encodes edits, label substitutions, port differences, or exceptional edges. Without \(\Delta_i\), family clustering is lossy even if the grammar syntax itself is exact.
