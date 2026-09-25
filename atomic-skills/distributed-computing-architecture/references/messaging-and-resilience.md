# Message semantics, flow control, and resilience

Load this reference for RPC, queues, brokers, event streams, peer-to-peer protocols, and asynchronous feedback.

## Envelope: separate identities

A useful starting schema (all fields are contract-dependent, not universally mandatory):

~~~yaml
schema_version: 1
message_id: uuid-of-this-delivery
operation_id: stable-id-across-retries
event_id: stable-id-of-the-activation-or-business-event
contribution_id: distinct-id-for-each-legitimate-branch-or-effect
causation_id: upstream-event-id
correlation_id: workflow-id
traceparent: w3c-trace-context
sender_id: authenticated-principal
recipient_id: target-or-partition-key
ownership_epoch: monotonically-increasing-fence-when-applicable
sequence: optional-per-producer-or-partition
attempt: 1
created_at: informational-time-not-proof-of-order
deadline_or_ttl: bounded-expiry-policy
payload_type: versioned-type
payload: schema-validated-data
signature_or_auth: transport-or-message-integrity
~~~

Do not reuse message_id as operation_id when retries create a new delivery. Do not use event_id alone to deduplicate feedback if multiple branches legitimately contribute to one event. Define whether contribution_id is created at fan-out, at every edge, or at aggregation. Treat source-provided IDs from untrusted senders as untrusted until scoped to an authenticated principal.

## Delivery / effect contract

| Stage | Possible outcome | Required behavior |
| --- | --- | --- |
| Send | Lost before receipt | Sender retries under budget when operation permits |
| Receive | Accepted in memory, crashes before persistence | May redeliver; do not ACK as durable |
| Persist | Durable receive, crashes before applying effect | Replay pending record |
| Effect | Effect commits, ACK is lost | Redelivery detects same effect identity and returns stored result |
| Publish | State commits, process crashes before event send | Transactional outbox/CDC retries publication |
| External side effect | Remote API succeeds, local state/ACK lost | Reconcile using remote idempotency key or explicit unknown-outcome state |

At-least-once delivery alone is not exactly-once processing. "Exactly-once effect" must name a bounded transactional state and the idempotent or transactional behavior of every external sink. An atomic database transaction can insert a unique (principal, operation_id/contribution_id, effect_kind) receipt and modify local state together. A check-then-act in two independent transactions has a race.

### Consumer state-machine sketch

~~~text
validate schema, authorization, epoch, size and expiry
derive durable effect_key at the correct semantic scope
BEGIN ATOMIC TRANSACTION
  insert unique inbox/effect_key receipt, or load prior outcome
  if inserted:
    assert current state/invariants
    apply the effect
    append any outbound event to transactional outbox
    persist outcome and receipt
COMMIT
ACK only after successful durability
on duplicate: return/re-ACK saved outcome; never apply effect again
on unknown commit outcome: re-read receipt before retrying side effects
~~~

For extremely high-throughput stateless transforms, skip durable per-message receipts only when replay does not violate business semantics and the checkpoint/source/sink protocol establishes the chosen guarantee. Dedup expiry requires a bound on redelivery/replay horizon; if indefinite replay is possible, compact into durable aggregate/version evidence rather than silently allowing old effects.

## Retry and timeout policy

Compute a total user or workflow deadline first. Each downstream call gets a connect timeout and request timeout inside that budget. Choose retryable statuses (transient failures, some overload signals) and never blindly retry validation errors, authorization errors, or irreversible writes without safe idempotency keys.

- One retry layer owns the policy; avoid multiplicative retries along the call chain.
- Cap attempts, total elapsed time, and retry traffic; use exponential backoff with randomized jitter and a retry budget.
- Honor server retry-after and no-retry hints where contractually defined; overload can require immediate rejection, not more retries.
- Propagate cancellation, but assume remote completion is possible until protocol state proves otherwise.
- Use hedged requests sparingly for safe read-only operations; cap speculative work and avoid correlated overload.
- Treat circuit breakers and bulkheads as protections for *specific* dependencies, not universal correctness substitutes.

## Backpressure and admission control

Every buffer needs capacity, admission policy, age limit, and instrumentation. Make overload observable and cheap:

1. Prioritize essential control and recovery traffic; assign per-tenant/per-workload quotas.
2. Bound worker concurrency, in-flight requests, fan-out, and queue bytes, not merely item counts.
3. Signal credits/window or broker lag to producers; slow/pause intake or reject early when no capacity remains.
4. Shed or degrade low-priority work before the system exhausts memory. DLQ poison items with reason and re-drive policy.
5. Make retries and replay participate in the same admission budget to avoid a recovery storm.

Avoid unbounded WebSocket sends/receives or infinite channels for per-node graph computation. If a peer cannot keep up, choose policy explicitly: spill to disk, defer, reroute, sample, degrade, or reject.

## Ordering, event time, and compatibility

Distinguish event time, processing time, and causality. For streams specify allowed lateness, watermarks, out-of-order windows, correction/retraction behavior, and replay from checkpoints. For actor/graph messages specify per-key/activation ordering and whether concurrent branches can arrive in any order. Version schemas additively where possible; use tolerant readers only within explicit validation/security boundaries. Simulate old and new nodes together before rolling out a new protocol.

## Security and observability

Authenticate the producer and destination, validate every payload, cap nesting/decompression ratios and message size, and prevent replay across tenants/epochs. Use mTLS where appropriate; it does not replace authorization of an operation. Propagate W3C trace context or causal IDs; sanitize headers arriving from other trust domains. Never put secrets or sensitive payloads in trace baggage. Track drop/duplicate/expiry/retry outcomes per operation class without creating unbounded metric cardinality.

Read [sources](sources.md) for AWS/Google overload practices, Microsoft idempotent consumer patterns, Flink effect-boundary semantics, and OpenTelemetry context propagation.
