---
name: distributed-dbms-architect
description: Design, review, and validate distributed database management systems (distributed SQL/NoSQL, replicated KV stores, storage and metadata control planes). Use for sharding, Raft/Paxos replication, transaction protocols, MVCC, consistency and availability contracts, online reconfiguration, failover, storage engines, and database correctness testing. Distinct from ordinary application schema/query tuning or deploying an existing DB without architectural changes.
license: MIT
metadata:
  category: systems-architecture
  version: "1.0.0"
  domain: distributed-databases
  triggers: distributed DBMS, distributed database architecture, database control plane, distributed SQL, distributed KV, sharding, consensus, replication, MVCC, distributed transactions, failover, rebalancing
  related-skills: architecture-designer, database-optimizer, chaos-engineer, rlm-roec-context-reasoning
---

# Distributed DBMS Architect

Design and audit a **database management system**, not merely an application's use of a database. Work from observable guarantees and failure assumptions to protocols and storage. Prefer a proven database over building a new one when requirements allow it. Distinguish established theory, an implementation-specific guarantee, a design proposal, and an unverified hypothesis.

## Selective companion skills

Read only when the subtask needs them: ../architecture-designer/SKILL.md for ADRs and architectural alternatives; ../database-optimizer/SKILL.md or ../postgres-pro/SKILL.md for a concrete query/storage diagnosis; ../chaos-engineer/SKILL.md for controlled failure experiments; ../rlm-roec-context-reasoning/SKILL.md for multi-source evidence and adversarial cross-checks. Do not conflate their application-level advice with DBMS correctness guarantees.

## Core workflow

1. **Specify the contract.** Inventory workloads (read/write mix, multi-key transactions, joins/range scans, hot keys, data size and growth, tenants), latency/throughput including p95/p99, geographic topology, failure model, cost, migration and compliance. State availability *per operation* during node/AZ/region partitions; define acknowledged-write durability, RPO/RTO, and allowed stale reads. Record whether linearizability is required per key, serializability across transactions, strict serializability, causal consistency, snapshot isolation, or eventual convergence. Never use "strongly consistent" without scope.
2. **Compare architecture families.** Consider single-primary with replicas, independently replicated shards, shared-disk/disaggregated storage, leaderless/quorum, and deterministic ordering only where relevant. Compare build versus existing FoundationDB, TiKV, CockroachDB, Spanner, or PostgreSQL plus a sharding/control layer against actual requirements; do not imply interchangeable semantics. Model latency from quorum geography and cross-shard hops before claiming performance.
3. **Draw separate planes.** Define query/API, transaction/concurrency, partition routing and replication, storage/WAL, control/metadata and operator/observability planes. Name each authoritative state owner and show how a client discovers and refreshes shard placement. Define the safe degraded mode if the metadata quorum is unavailable.
4. **Prove the critical invariants.** Specify exactly which operation becomes durable when, who may serve authoritative reads/writes under lease/epoch changes, how shard membership changes safely, how transaction decisions survive coordinator failure, and how old nodes are fenced. Tie every guarantee to durable state, message sequence and recovery rules; use the detailed decision guides in references/architecture-playbook.md and references/transactions-and-consistency.md.
5. **Design lifecycle and operations.** Detail bootstrap, identity and PKI, rolling upgrades, admission control, split/merge/rebalance, backup/PITR, failover and failback, decommission, geo-DR, observability, capacity and safe operator automation. Use references/verification-and-operations.md.
6. **Seek counterexamples before implementation.** For every invariant, construct a schedule involving a crash, delay, duplicate, reorder, network partition, stale route or clock anomaly. Run deterministic simulation/model checking where feasible, Jepsen/Elle-style history checks on suitable workloads, fault injection, and restore drills. An absence of failures in tests is not proof of correctness.
7. **Deliver an implementable decision packet.** Produce the contract, diagram, protocol and state machine, ADRs, fault matrix, acceptance tests, staged rollout and rollback. Explicitly identify unknowns and assumptions; do not prescribe an algorithm before its safety and cost consequences are documented.

## Non-negotiable safety properties

- **Replication is not a transaction protocol.** A per-shard Raft quorum cannot by itself make a multi-shard transaction atomic. Two-phase commit is not consensus and requires durable decisions, consensus-backed participants or an equivalent recovery strategy.
- **Quorum is not a magic integer.** Define read/write quorum intersections, membership epoch, geographic failure domains and actual durability boundaries. A majority that excludes an isolated former leader must not accept its stale writes.
- **Clock time is not transaction order by default.** Treat clock skew, uncertainty, lease bounds and HLC/TSO failure modes explicitly. Do not copy Spanner's TrueTime guarantees into a deployment without equivalent assumptions.
- **Retry is not exactly-once.** Treat timeouts as ambiguous outcomes; use durable idempotency tokens, transaction-status lookup and explicit retry semantics. Do not silently replay external side effects.
- **No unsafe resharding.** Use epoch/versioned placement, linearization points, write barriers or dual-write protocols with proofs, resumable copy plus incremental catch-up, and fencing. Never expose two active owners of the same writable range.
- **No automatic data-loss failover.** On quorum loss, stop operations that require a quorum. Allow degraded/stale reads only under an explicit client-visible contract. A backup, read replica or async replica is not evidence of zero RPO.
- **Test actual recovery.** A green backup job without restoration, consistency checks and measured RPO/RTO is not a validated recovery plan.

## Required outputs

For a new design or substantial review, include: (a) requirements and consistency matrix by API; (b) component/data-flow diagram and one write/read/transaction sequence; (c) ownership, shard-map and membership state machine; (d) transaction and durability invariants with counterexamples; (e) per-failure behavior and decision on safe unavailability; (f) benchmark and correctness-test plan; (g) operational runbooks, metrics and rollout; (h) ADRs listing alternatives and costs. Use source links in references/sources.md and revalidate product/version-specific behavior before adopting it.

## Reference routing

- [architecture-playbook.md](references/architecture-playbook.md) — design choices, control/data planes, placement, replication, storage, shard lifecycle and cost.
- [transactions-and-consistency.md](references/transactions-and-consistency.md) — consistency contracts, MVCC, cross-shard transactions, timestamp and retry semantics.
- [verification-and-operations.md](references/verification-and-operations.md) — invariant-driven test matrix, observability, backup/DR and upgrade runbooks.
- [sources.md](references/sources.md) — authoritative papers, primary documentation and scope cautions.
