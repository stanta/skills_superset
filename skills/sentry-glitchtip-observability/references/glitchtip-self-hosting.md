# GlitchTip Self-Hosting

## Current baseline

Verified against GlitchTip documentation on 2026-09-20.

GlitchTip currently documents:

- PostgreSQL 14+ as required;
- one service or separate web/worker services for scaling;
- Valkey/Redis 7+ as optional;
- about 512 MB RAM recommended for a small instance;
- Docker Compose as a recommended deployment path;
- Helm support for Kubernetes;
- external managed PostgreSQL as the recommended production database approach for Kubernetes/HA scenarios.

Sizing depends on event volume and event size. Current docs give a rough example that 1 million events per month may require about 30 GB of disk.

Treat these as starting points, not capacity guarantees.

## Production architecture

Small:

```text
TLS reverse proxy
  -> GlitchTip web/worker
  -> PostgreSQL
  -> persistent file storage
  -> optional Valkey
```

Larger:

```text
load balancer / ingress
  -> multiple web replicas
  -> worker replicas
  -> managed HA PostgreSQL
  -> Valkey/Sentinel as appropriate
  -> S3-compatible object storage
  -> external monitoring
```

Use a proxy/load balancer that supports request buffering and chunked transfer handling, as recommended by GlitchTip.

## Persistent data

Protect all durable state:

- PostgreSQL database;
- uploaded source maps/debug files;
- cold-storage Parquet data when enabled;
- configuration/secrets required to restore the instance.

Do not rely on an ephemeral container filesystem for uploads.

For multi-node deployments, prefer S3-compatible object storage over a node-local volume.

## Backups

At minimum:

- automated PostgreSQL backups;
- object/file-storage backup or versioning policy;
- backup encryption;
- retention appropriate to incident and compliance needs;
- regular restore tests.

A backup that has never been restored is not a verified backup.

Document RPO and RTO.

## Data retention

Current GlitchTip configuration exposes retention controls including:

- `GLITCHTIP_RETENTION_DAYS` — default 90;
- `GLITCHTIP_EVENT_RETENTION_DAYS`;
- `GLITCHTIP_EVENT_HOT_DAYS` — default 30;
- `GLITCHTIP_TRANSACTION_RETENTION_DAYS`;
- `GLITCHTIP_LOG_RETENTION_DAYS`;
- `GLITCHTIP_LOG_HOT_DAYS` — default 7;
- `GLITCHTIP_UPTIME_RETENTION_DAYS`;
- `GLITCHTIP_FILE_RETENTION_DAYS`;
- `GLITCHTIP_RELEASE_RETENTION_DAYS` — default 365.

Choose retention from debugging, legal, and storage requirements. Do not keep sensitive telemetry forever by default.

## Cold storage

GlitchTip supports hot/cold storage using PostgreSQL for recent data and DuckDB + Parquet for older queryable data.

Current documented switch:

```env
GLITCHTIP_ENABLE_DUCKDB=true
```

Cold data can be stored in an S3 bucket or local filesystem.

For production:

- prefer durable object storage;
- lifecycle and backup policies must match GlitchTip retention;
- bound DuckDB memory;
- provide writable temporary spill storage.

## Valkey / Redis

Valkey is optional for small installations but recommended for faster/larger deployments.

For HA, GlitchTip documents Sentinel support.

Monitor:

- memory;
- connection count;
- latency;
- evictions;
- failover state.

Do not make Valkey publicly reachable.

## Database permissions

GlitchTip documents least-privilege separation:

- web service: row read/write;
- worker/migration paths: broader schema permissions including DDL where required.

Use separate credentials if the deployment model supports it.

## Security hardening

- Terminate TLS at a trusted ingress/proxy.
- Use a strong `SECRET_KEY`.
- Store database, mail, storage, OAuth, and API credentials in a secret manager.
- Disable open registration or organization creation unless intentionally public.
- Restrict admin access.
- Keep PostgreSQL and Valkey on private networks.
- Patch the OS/container runtime and GlitchTip regularly.
- Pin production image versions; review release notes before major upgrades.
- Rate-limit or protect public ingress at the reverse proxy/WAF layer.
- Monitor unusual ingest spikes that may be DSN abuse.
- Keep private-IP uptime targets disabled unless needed.

Current GlitchTip documentation defaults `GLITCHTIP_UPTIME_ALLOW_PRIVATE_IPS` to false specifically to reduce SSRF risk. Preserve that default unless internal monitoring is required and network access is intentionally constrained.

## Mail

Configure real SMTP/email delivery when alerts are operationally required.

`consolemail://` is acceptable for local/test setups but not for production alerting.

Test one alert after every mail-system change.

## File storage

Source maps and debug files require persistent storage.

Current GlitchTip docs support local volumes and django-storages-compatible backends such as:

- S3 / DigitalOcean Spaces;
- Azure Blob Storage;
- Google Cloud Storage;
- S3-compatible systems such as MinIO or R2 via supported configuration.

For multiple web/worker replicas, all replicas must see consistent file storage.

## Scaling

Scale based on measured bottlenecks:

1. PostgreSQL query/storage pressure.
2. Worker backlog.
3. ingest request rate.
4. file/object storage throughput.
5. performance/log event volume.

Add Valkey and split web/worker roles before scaling blindly.

For Kubernetes HA, current docs recommend multiple nodes, ingress/load balancer, pod disruption budget, anti-affinity, and managed HA PostgreSQL.

## Upgrade procedure

1. Read release notes, especially for major versions.
2. Back up database and file/object storage.
3. Stage the upgrade against a production-like copy.
4. Run migrations.
5. Verify login, ingest, worker processing, source maps, alerts, uptime, and retention jobs.
6. Observe database and worker load.
7. Keep a rollback plan for the application image; understand whether database migrations are reversible.

Do not auto-upgrade major versions in production without compatibility review.

## Monitoring GlitchTip itself

Use external infrastructure observability for:

- HTTP availability and latency;
- 5xx rate;
- PostgreSQL health/storage;
- worker failures and backlog;
- Valkey health;
- object-storage errors;
- disk usage;
- mail delivery failures;
- certificate expiration.

Keep at least one external uptime check outside the GlitchTip instance.

## Sources

- https://glitchtip.com/documentation/install/
- https://glitchtip.com/documentation/hosted-architecture/
- https://glitchtip.com/documentation/performance/
- https://glitchtip.com/documentation/logs/
- https://glitchtip.com/documentation/uptime-monitoring/
- https://glitchtip.com/documentation/cli/
