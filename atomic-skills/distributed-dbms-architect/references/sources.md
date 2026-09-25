# Sources and evidence boundaries

Primary literature and upstream docs reviewed for this skill on 2026-09-25. Cite these when an architectural claim depends on an implementation, and recheck version-specific guarantees before coding. Sources illustrate different designs; they do **not** establish that a technique is appropriate for every DBMS.

## Algorithms and consistency

1. Ongaro & Ousterhout, [In Search of an Understandable Consensus Algorithm (Raft)](https://raft.github.io/raft.pdf) (2014). Leader election, replicated logs, safety and changing membership. Confirm the implemented Raft library's exact membership-change and read protocols.
2. Corbett et al., [Spanner: Google's Globally-Distributed Database](https://research.google/pubs/spanner-googles-globally-distributed-database-2/) (OSDI 2012) and [TrueTime/external consistency documentation](https://docs.cloud.google.com/spanner/docs/true-time-external-consistency). External consistency uses specific bounded-clock assumptions; this is not a drop-in property of ordinary NTP clocks.
3. Jepsen, [Consistency Models](https://jepsen.io/consistency/models), including [strict serializability](https://jepsen.io/consistency/models/strong-serializable) and [snapshot isolation](https://jepsen.io/consistency/models/snapshot-isolation). Use precise transactional versus single-object definitions; do not assume every listed model is totally ordered relative to every other one.
4. Jepsen, [Elle transactional consistency checker](https://github.com/jepsen-io/elle/blob/main/README.markdown). A checker detects anomalies supported by its workload and observed histories, not every possible anomaly.

## Production implementation references

5. Zhou et al., [FoundationDB: A Distributed Unbundled Transactional Key Value Store](https://www.foundationdb.org/files/fdb-paper.pdf) and [FoundationDB architecture](https://apple.github.io/foundationdb/architecture.html). Separation of transaction/log/storage roles, recovery epochs and database guarantees; read current docs alongside the paper.
6. FoundationDB, [Simulation and Testing](https://apple.github.io/foundationdb/testing.html). Deterministic, reproducible whole-cluster fault simulations.
7. TiKV, [Architecture / terminology](https://tikv.org/docs/7.1/reference/architecture/terminology/) and [PD scheduling](https://tikv.org/docs/7.1/reference/architecture/scheduling/). Independent replicated Regions, placement, safe rebalancing, control-plane concerns. Product-version-specific routing and transaction semantics must be checked against the deployment.
8. CockroachDB, [Developer Basics](https://www.cockroachlabs.com/docs/stable/developer-basics.html). Product-specific transactional isolation and retry behavior; do not infer another engine's semantics from these docs.

## Reliability and recovery

9. AWS Well-Architected, [Back up data](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/back-up-data.html) and [Periodic restore testing](https://docs.aws.amazon.com/wellarchitected/latest/framework/rel_backing_up_data_periodic_recovery_testing_data.html). Recovery evidence requires restore tests and measured RPO/RTO.
10. AWS Well-Architected, [Test disaster recovery implementation](https://docs.aws.amazon.com/wellarchitected/latest/framework/rel_planning_for_recovery_dr_tested.html). Test end-to-end failover and failback rather than treating a standby as sufficient proof.

## Evidence policy

Distinguish: paper/proof of an algorithm under assumptions; vendor description of one version; benchmark measurement of one workload; and unverified design hypothesis. Capture source URL, version/date, guarantee scope, fault model, contradictory evidence and the exact design decision it supports in each ADR. Prefer measured deployment behavior and adversarial correctness tests for implementation claims.
