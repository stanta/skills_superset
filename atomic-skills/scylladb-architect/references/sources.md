# Sources

Last verified: 2026-10-06.

Use stable/version-matched documentation for implementation. URLs below are authoritative ScyllaDB documentation unless noted.

## Architecture, topology and data distribution

- ScyllaDB Architecture: https://docs.scylladb.com/manual/stable/architecture/
- Data Distribution with Tablets: https://docs.scylladb.com/manual/stable/architecture/tablets.html
- Ring Architecture: https://docs.scylladb.com/manual/stable/architecture/ringarchitecture/
- Fault Tolerance: https://docs.scylladb.com/manual/stable/architecture/architecture-fault-tolerance.html
- Raft in ScyllaDB: https://docs.scylladb.com/manual/stable/architecture/raft.html
- CQL DDL / NetworkTopologyStrategy / tablets: https://docs.scylladb.com/manual/stable/cql/ddl.html

## Data modeling and consistency

- Data Modeling: https://docs.scylladb.com/stable/get-started/data-modeling/
- Query Design: https://docs.scylladb.com/stable/get-started/data-modeling/query-design.html
- Data Modeling Best Practices: https://docs.scylladb.com/main/get-started/data-modeling/best-practices.html
- Consistency Levels: https://docs.scylladb.com/manual/stable/cql/consistency.html
- Lightweight Transactions: https://docs.scylladb.com/manual/stable/features/lwt.html
- CQL BATCH: https://docs.scylladb.com/manual/stable/cql/dml/batch.html
- CQL Limits: https://docs.scylladb.com/manual/stable/reference/limits.html
- Large Partitions diagnostics: https://docs.scylladb.com/manual/stable/troubleshooting/large-partition-table.html

## Compaction and storage

- Compaction overview: https://docs.scylladb.com/manual/stable/kb/compaction.html
- Choose a Compaction Strategy: https://docs.scylladb.com/manual/stable/architecture/compaction/compaction-strategies.html
- System Requirements: https://docs.scylladb.com/manual/stable/getting-started/system-requirements.html
- System Configuration / XFS / tuning: https://docs.scylladb.com/manual/stable/getting-started/system-configuration.html
- Configuration Parameters: https://docs.scylladb.com/manual/stable/reference/configuration-parameters.html
- Maximizing ScyllaDB Performance: https://docs.scylladb.com/manual/branch-2026.3/operating-scylla/procedures/tips/benchmark-tips.html

## Drivers

- CQL Drivers and tablet support: https://docs.scylladb.com/stable/drivers/cql-drivers.html
- Driver Support: https://docs.scylladb.com/stable/versioning/driver-support.html
- Java driver load balancing: https://java-driver.docs.scylladb.com/stable/manual/core/load_balancing/
- Java driver idempotence: https://java-driver.docs.scylladb.com/stable/manual/core/idempotence/
- Java driver paging: https://java-driver.docs.scylladb.com/stable/manual/core/paging/
- Rust driver statement best practices: https://rust-driver.docs.scylladb.com/stable/statements/statements.html
- Rust driver batching: https://rust-driver.docs.scylladb.com/stable/statements/batch.html

## Repair, backup and monitoring

- Automatic Repair: https://docs.scylladb.com/manual/stable/features/automatic-repair.html
- ScyllaDB Manager Repair: https://manager.docs.scylladb.com/stable/repair/
- Backup and Restore Overview: https://docs.scylladb.com/manual/stable/features/backup-and-restore.html
- Backup procedure: https://docs.scylladb.com/manual/stable/operating-scylla/procedures/backup-restore/backup.html
- Restore procedure: https://docs.scylladb.com/manual/stable/operating-scylla/procedures/backup-restore/restore.html
- ScyllaDB Monitoring Stack: https://monitoring.docs.scylladb.com/stable/intro.html

## Version-sensitive notes

- Tablets are now the default for new keyspaces in current stable ScyllaDB, but old clusters and feature-specific deployments may still use vnodes.
- Consistent topology changes through Raft are mandatory in ScyllaDB 2025.2 and later according to current stable documentation.
- Driver tablet support and supported driver minor versions change over time; verify the live support matrix.
- Automatic repair is evolving and applies to tablet tables; verify the deployed release before treating it as a replacement for external repair scheduling.
- Object-storage keyspaces have feature restrictions that differ from ordinary local-storage deployments; verify current admin docs before using them.
