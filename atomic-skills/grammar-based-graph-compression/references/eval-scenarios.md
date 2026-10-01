# Skill evaluation scenarios

These scenarios target common reasoning failures in grammar-based graph compression.

## Scenario 1: frequency trap

Prompt: "I found a 2-edge motif 50,000 times. Should I make it a grammar token?"

Pass if the agent asks for or estimates rule, interface, reference and overlap cost and does not equate raw frequency with net compression.

## Scenario 2: cluster-as-symbol trap

Prompt: "Wishart produced cluster 7 on every level. Use cluster 7 as the same Huffman symbol."

Pass if the agent rejects level-local cluster IDs as persistent identity and requires canonical/persistent symbol mapping or residualized family semantics.

## Scenario 3: boundary loss

Prompt: "Two induced subgraphs are internally isomorphic, so replace both with one supernode."

Pass if the agent checks external attachment ports, relation direction/labels and reconstruction semantics.

## Scenario 4: WL overclaim

Prompt: "The typed-WL hashes match, so exact lossless substitution is safe."

Pass if the agent treats WL as a filter/descriptor and requires exact canonical/isomorphism verification when exact identity matters.

## Scenario 5: fake compression metric

Prompt: "We reduced vertices by 70%, therefore compression is 70%."

Pass if the agent reports storage in bits/bytes including grammar, ports, residuals/indexes and rejects node reduction as a storage ratio.

## Scenario 6: approximate grammar

Prompt: "Group structurally similar but non-isomorphic motifs under one rule and still call it lossless."

Pass if the agent requires residual edit scripts/corrections or labels the representation lossy.

## Scenario 7: generative/compression confusion

Prompt: "An HRG generates realistic graphs, therefore it is the best lossless compressor for this graph."

Pass if the agent distinguishes generative fit from exact code length and requires a compressor benchmark.

## Scenario 8: direct-query claim

Prompt: "Grammar compression always speeds up graph queries."

Pass if the agent ties query support to the grammar/data structure/workload and benchmarks compressed size including query indexes.

## Scenario 9: semantic graph

Prompt: "Compress ConceptNet but relation labels may be discarded because topology is preserved."

Pass if the agent treats relation labels and direction as terminal semantics unless the user explicitly defines a lossy objective.

## Scenario 10: natural grammar overclaim

Prompt: "The recursive dictionary proves the graph has a natural semantic grammar."

Pass if the agent asks for stability/null controls and uses cautious language such as "reusable compression symbols under the tested representation."
