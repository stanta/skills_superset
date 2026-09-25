# Asynchronous graph and neuromorphic computation

Use this specialization when a distributed graph's nodes (actors, neurons, devices, GPU-backed workers) maintain local state, forward activations independently, and later receive asynchronous feedback. It is a protocol design pattern, **not** a claim that the resulting algorithm learns or converges without a mathematical model and tests.

## Architecture: local state, no global clock

A node owns its parameters and activation ledger. Incoming signals are keyed and processed through a bounded mailbox. Forward propagation carries a stable activation EventID plus per-hop provenance (source node, edge/branch, schema, bounded hop count, trace). A node computes with its currently available inputs under a declared policy: wait for a specified fan-in, aggregate within a time window, or compute opportunistically. Never assume peers share the same model version or simultaneous step.

A membership/discovery overlay can use gossip/SWIM-like suspicion. Discovery and membership are not a global truth oracle. Separate the control plane (node identity, capabilities, liveness suspicion, edge ownership, version advertisements) from the computation plane (signal payloads and feedback). Gossip does not by itself provide addressed reliable delivery, routing shortest paths, guaranteed reachability, or eventual training convergence; specify independent routing, retry, and reconciliation.

## Event and contribution identities

Use **activation identity** to match a feedback signal with the exact local forward computation. Use **contribution identity** to distinguish legitimate independent downstream gradients from network redelivery of one downstream gradient.

Example logical key set:

~~~yaml
activation:
  event_id: globally-or-origin-scoped-unique-id
  node_id: local-computing-node
  local_activation_id: immutable-id-for-this-forward-execution
  predecessor_contribution_ids: [input-branch-identities]
  parameters_version: snapshot-or-version-used-for-forward
  output: sufficient-forward-context
  expires_at: bounded-retention-horizon
feedback:
  event_id: parent-activation-event-id
  target_node_id: recipient
  target_local_activation_id: recipient-execution-id
  contribution_id: unique-downstream-branch-and-feedback-instance
  contributor_node_id: authenticated-downstream-node
  source_edge_id: graph-edge
  feedback_version: schema-or-gradient-version
  ttl_or_remaining_hops: bounded
  payload: gradient-or-other-feedback
~~~

The durable dedup/effect key should include at least the target activation execution identity and the **logical contribution identity**, scoped by trusted node/edge and feedback kind as required. The same contribution delivered twice must not be applied twice; different branch contributions for one EventID may both be valid. A second independently computed update from the same edge needs a different contribution identity under an explicit policy.

Do **not** deduplicate solely by EventID or by upstream node. Do not rely solely on ephemeral in-memory sets when restart and redelivery can occur.

## Local activation lifecycle

~~~text
ABSENT
  -- valid forward input --> COLLECTING / READY
READY -- compute with parameter snapshot --> ACTIVATED
ACTIVATED -- durable output + successor records --> AWAITING_FEEDBACK
AWAITING_FEEDBACK -- first valid contribution --> PARTIALLY_UPDATED
PARTIALLY_UPDATED -- new unique contribution --> PARTIALLY_UPDATED
AWAITING_FEEDBACK or PARTIALLY_UPDATED -- complete/expired --> FINALIZED
FINALIZED -- duplicate contribution --> return stored outcome; no new update
FINALIZED -- late new contribution --> apply declared late policy; no resurrection
~~~

Decide whether gradient contributions accumulate then update once or each triggers a versioned local update. Those policies are not mathematically interchangeable: applying a stale contribution after intervening parameter updates changes the optimizer behavior. Preserve the forward-time parameter snapshot/version and define staleness acceptance, clipping, weighting, and optimizer-state ownership. If a fan-out branch never returns feedback, choose a completion quorum, deadline, partial-gradient policy, or explicit cancellation.

Store enough forward context to compute the derivative or a safe replay reference. Track downstream contributions and predecessor edges without indefinitely retaining full activation tensors. Put hard limits on activation ledger size, fan-out, feedback TTL, replay horizon, input dimensionality, and message bytes.

## Graph cycles and delayed feedback

Detect or bound cycles with per-message hop TTL, loop detection/visited path when practical, and explicit recurrent-time-step semantics if cycles are intended. A repeated signal with the same EventID is not necessarily a new training example. Set what late feedback means after the activation ledger expires: reject and count, reconstruct from a durable checkpoint only with verified version, or use a separately justified approximate/stale-gradient algorithm.

Any hop TTL only bounds route length; it does not guarantee that a message disappears in real time. If the system needs time expiry, define clock assumptions and deadline checks at receiving nodes. Idempotency ledger retention must cover the maximum legitimate replay horizon or expired replays must be rejected by activation epoch/version.

## Resource, security, and correctness gates

- Gossip dissemination and peer churn must be capacity-limited; no O(N²) all-to-all control broadcast by default.
- Authenticate feedback origin and authorize graph-edge writes; a message knowing EventID is not sufficient permission to change weights.
- Version graph edges and local parameter state, particularly when 25% of connections are replaced or nodes change addresses. Preserve explicit edge lifecycle and distinguish retired-edge late feedback from legitimate new-edge feedback.
- Avoid assigning semantics to IPv6 addresses as immutable node identities. An authenticated stable node ID maps to current addresses/epochs in discovery.
- Treat GPU, network, CPU, and storage as distinct bounded queues; batch without violating the activation/contribution identity model.
- Test fork/join, duplicate delivery, replay after crash, late/expired feedback, stale weights, edge replacement, partial partitions, and malicious feedback. Track whether a local rule remains stable empirically; a distributed implementation can be protocol-correct yet mathematically unstable.

## Architecture outputs for a DANMA-like design

Produce a per-node state machine; forward and feedback envelopes; route/discovery policy; activation/contribution dedup keys; fan-out/join and local learning algebra; persistence/restart policy; expiry/hop TTL; checkpoint and reconciliation strategy; load/backpressure budgets; and a test matrix with the cases above. Explicitly say that no continuous global consistency is required **unless a specific global invariant demands it**.

Apply the general [consistency](consistency-and-coordination.md), [messaging](messaging-and-resilience.md), and [verification](verification-and-operations.md) references to the chosen semantics. Record any convergence claims as hypotheses until supported by a mathematical argument and reproducible experiments.
