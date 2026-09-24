---
name: nats-jetstream
description: This skill should be used when building, debugging, or operating async Python microservices that communicate via NATS JetStream — including consumer/producer patterns, durable subscriptions, task retry logic, message acknowledgment, stream configuration, and worker orchestration with nats-py.
metadata:
  category: messaging
  source:
    repository: https://github.com/nats-io/nats.py
---

# NATS JetStream Async Python Patterns

## Source

- **nats.py** — GitHub: [nats-io/nats.py](https://github.com/nats-io/nats.py) (900+ stars, 170+ forks)
- **NATS Server** — GitHub: [nats-io/nats-server](https://github.com/nats-io/nats-server) (16k+ stars)
- **NATS Docs** — https://docs.nats.io/

## Trigger Keywords

`nats`, `jetstream`, `message queue`, `consumer`, `producer`, `durable subscription`, `nats worker`, `task queue`, `orker`, `publish`, `subscribe`, `ack`, `nak`, `stream`

## Core Patterns

### Connection & JetStream Setup
```python
import nats
from nats.js.api import StreamConfig, ConsumerConfig, AckPolicy, DeliverPolicy

async def connect_nats(uri: str) -> nats.NATS:
    nc = await nats.connect(uri)
    js = nc.jetstream()
    return nc, js
```

### Stream Configuration
```python
# Create or update a stream
await js.add_stream(
    StreamConfig(
        name="tasks",
        subjects=["tasks.>"],
        retention="workqueue",      # Messages removed after ack
        max_msgs=-1,
        max_bytes=-1,
        storage="file",
        num_replicas=1,
    )
)
```

### Consumer (Worker) Pattern
```python
# Durable pull consumer
sub = await js.pull_subscribe(
    subject="tasks.index",
    durable="index-worker",
    config=ConsumerConfig(
        ack_policy=AckPolicy.EXPLICIT,
        max_deliver=3,              # Max retry attempts
        ack_wait=300,               # 5 min ack timeout
        filter_subject="tasks.index",
    ),
)

# Consume loop
while True:
    try:
        msgs = await sub.fetch(batch=1, timeout=5)
        for msg in msgs:
            try:
                task = TaskModel.model_validate_json(msg.data)
                await process_task(task)
                await msg.ack()
            except NoRetry:
                await msg.term()    # Terminate - no retry
            except Exception:
                await msg.nak(delay=10)  # Retry after delay
    except nats.errors.TimeoutError:
        continue
```

### Producer Pattern
```python
# Publish task to stream
async def publish_task(js, subject: str, task: BaseModel) -> None:
    ack = await js.publish(
        subject=subject,
        payload=task.model_dump_json().encode(),
        headers={"Nats-Msg-Id": str(task.id)},  # Deduplication
    )
    logger.info(f"Published to {subject}, seq={ack.seq}")
```

### Worker Framework (Orker Pattern)
The project uses `orker` library which wraps NATS JetStream consumer with:
- Pre/post lifecycle hooks
- Automatic DB session management (SQLAlchemy async)
- Retry logic with configurable attempts and delay
- Sentry error tracking integration
- Graceful shutdown handling

```python
from orker import worker

worker(
    subject="index_tasks",
    task_model=IndexTask,
    work=process_index_task,
    on_fail=handle_failure,
    retry_attempts=3,
    stream="tasks",
    durable_name="anglerfish-index",
    nats_uri=settings.nats_uri,
    postgres_host=settings.postgres_host,
    # ... other DB settings
)
```

### Best Practices
- **Always use explicit ack** — never rely on auto-ack for critical tasks
- **Set `ack_wait`** longer than your maximum task processing time
- **Use `Nats-Msg-Id` header** for idempotent message deduplication
- **Implement graceful shutdown** — drain subscriptions before exit
- **Monitor consumer lag** — check `num_pending` to detect slow consumers
- **Use workqueue retention** for task queues (messages deleted after ack)
- **Separate streams** for different domains (indexing, chat, notifications)

### Error Handling
- `msg.ack()` — task completed successfully
- `msg.nak(delay=N)` — retry after N seconds
- `msg.term()` — permanently fail (e.g., NoRetry errors, invalid data)
- `msg.in_progress()` — extend ack deadline for long-running tasks

## When NOT to Use
- For HTTP API design → use `api-designer` or `fastapi-expert`
- For WebSocket real-time → use `websocket-engineer`
- For general async Python → use `python-dev`
