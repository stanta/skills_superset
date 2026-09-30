# Evidence sources

Use primary papers first. Treat implementation and benchmark claims as dataset- and version-specific.

## Core grammar compression

1. Sebastian Maneth, Fabian Peternek. **Grammar-based graph compression.** *Information Systems* 76 (2018), 19–45. DOI: https://doi.org/10.1016/j.is.2018.03.002  
   Open preprint: https://arxiv.org/abs/1704.05254  
   Core evidence for gRePair, straight-line hyperedge-replacement grammars, repeated digram replacement, rank/order effects, pruning, and grammar-side query evaluation.

2. Sebastian Maneth, Fabian Peternek. **Compressing Graphs by Grammars.** ICDE 2016, 109–120. DOI: https://doi.org/10.1109/ICDE.2016.7498233  
   Accepted manuscript: https://www.pure.ed.ac.uk/ws/portalfiles/portal/23486332/Maneth_et_al_2016_compressing_graphs.pdf

3. Sebastian Maneth, Fabian Peternek. **Constant delay traversal of grammar-compressed graphs with bounded rank.** *Information and Computation* 273 (2020), 104520. DOI: https://doi.org/10.1016/j.ic.2020.104520  
   Evidence for traversal/query data structures over SL-HR grammars and why bounded rank matters.

## Compression-driven discovery / MDL

4. Lawrence B. Holder, Diane J. Cook, Surnjani Djoko. **Substructure Discovery in the SUBDUE System.** AAAI Workshop / related SUBDUE literature. Project bibliography and historical materials: https://ailab.wsu.edu/subdue/  
   SUBDUE literature is the basis for compression-guided substructure search, beam search, hierarchical replacement, and inexact matching.

5. Ashwin Ketkar et al. **Subdue: Compression-Based Frequent Pattern Discovery.** OSDM 2005. PDF: https://ailab.wsu.edu/subdue/papers/KetkarOSDM05.pdf

6. Esther Galbrun. **The minimum description length principle for pattern mining: a survey.** *Data Mining and Knowledge Discovery* 36 (2022). DOI: https://doi.org/10.1007/s10618-022-00846-z  
   Critical source on MDL pattern mining, including limitations of approximate SUBDUE-style error handling and comparison with graph-summary methods.

7. Danai Koutra, U Kang, Jilles Vreeken, Christos Faloutsos. **VoG: Summarizing and Understanding Large Graphs.** SDM 2014. DOI: https://doi.org/10.1137/1.9781611973440.11  
   Preprint: https://arxiv.org/abs/1406.3411  
   Not a recursive graph grammar; use as an MDL structural-summary baseline.

## Query-oriented grammar compression

8. Enno Adler, Stefan Böttcher, Rita Hartel. **ITR: Grammar-based Graph Compression Supporting Fast Triple Queries.** DCC 2024. DOI: https://doi.org/10.1109/DCC58796.2024.00062  
   Earlier full preprint on grammar compression and neighborhood queries: https://arxiv.org/abs/2306.01028

## Graph grammar induction / generation

9. Salvador Aguinaga, David Chiang, Tim Weninger. **Learning Hyperedge Replacement Grammars for Graph Generation.** *IEEE Transactions on Pattern Analysis and Machine Intelligence* 41(3), 2019, 625–638. DOI: https://doi.org/10.1109/TPAMI.2018.2810877  
   Preprint: https://arxiv.org/abs/1802.08068  
   Use to distinguish generative HRG learning from exact compression.

10. Salvador Aguinaga, Rodrigo Palacios, David Chiang, Tim Weninger. **Growing Graphs with Hyperedge Replacement Graph Grammars.** https://arxiv.org/abs/1608.03192

11. Luka Fürst et al. **Graph grammar induction.** *Advances in Computers* 116 (2020), 133–181. DOI: https://doi.org/10.1016/bs.adcom.2019.07.003  
    Evidence for the distinct problem of inducing graph languages from examples.

## Recent neighboring work / frontier

12. Enno Adler, Stefan Böttcher, Rita Hartel. **Compressing Hypergraphs using Suffix Sorting.** DCC 2026, 113–122. DOI: https://doi.org/10.1109/DCC66757.2026.00019  
    Preprint: https://arxiv.org/abs/2506.05023  
    Use as a modern hypergraph-compression comparator, not as evidence that grammar methods are universally best.

## Supporting graph matching

For exact reusable symbols, use graph-isomorphism/canonical-labeling machinery after cheap signatures. Weisfeiler–Lehman refinement is a useful filter/descriptor but is not a complete isomorphism test for arbitrary graphs. Practical exact options include VF2-style verification and canonical-labeling tools such as nauty/Traces or bliss, selected according to graph size, labels, and interface constraints.

## Evidence discipline

- Cite the exact method paper for an algorithmic property.
- Do not transfer published compression ratios or query latencies to a new graph.
- Distinguish a paper's theoretical guarantee from its implementation heuristic.
- Separate graph-generation quality from lossless code length.
- Treat recent preprints as provisional when a peer-reviewed version is not available.
