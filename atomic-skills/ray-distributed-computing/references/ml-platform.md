# Ray Data, Train, Tune and Serve: selection and integration

## Choose the product by lifecycle

| Requirement | Component | Important boundary |
| --- | --- | --- |
| Scalable reading, transforms, batches and batch inference | Ray Data | Data pipeline, not durable database or general message queue |
| Launch distributed PyTorch/TensorFlow training jobs | Ray Train | Distributed training orchestration, not a custom PyTorch device backend |
| Search parameters and early-stop trials | Ray Tune | Declare trial resources, storage and resumability |
| Scale online model/HTTP serving | Ray Serve | Request routing/replicas; model-level effects still need application policy |
| Arbitrary Python tasks and stateful workers | Ray Core | Build task/actor, resource, state and retry contract explicitly |

## Ray Data

Use for datasets, column/batch transforms and scalable batch inference when Ray Data fits the source and execution mode. Benchmark row versus batch transforms, repartitioning, object-store pressure and ingest backpressure; streaming execution does not imply unbounded input is safe. Do not move a frequently mutated neuron state or event-by-event feedback ledger into a Ray Dataset.

## Ray Train

For standard distributed PyTorch work, select `TorchTrainer`, a worker-local training function and explicit `ScalingConfig`. Create/load datasets and model on workers rather than pickling a giant initialized model into `train_loop_config`. Save model/optimizer/checkpoint shards and report metrics through the supported Train APIs. Use external shared/cloud persistent storage for multi-node training checkpoints.

For TensorFlow use the trainer and integration supported by the installed Ray version; verify API before adopting examples. Ray Train launches framework workers: it does not make a new virtual accelerator (`danma:0`). A custom backend needs its own PyTorch/TensorFlow integration independently of Ray Train.

## Ray Tune

Use for a genuinely parallelizable experiment search. Choose concurrency and per-trial CPU/GPU reservations, explicit evaluation metric/mode and stopping rule; pin code/data versions and persist trial outputs. If trials are expensive, use a scheduler such as ASHA only when intermediate metrics are meaningful. Do not run many trials that contend for the same underlying native thread pool or data-storage bandwidth.

## Ray Serve

Use when the deliverable is a continuously served model or application. Set request concurrency, batch parameters, startup/readiness probes, bounded queues, deployment resource allocation and autoscaling from measured latency/throughput. A Serve replica is a process/actor; it does not guarantee exactly-once external effects or durable state. Start with manual replica scaling before tuning automatic autoscaling if throughput is not understood.

## End-to-end production handoff

Define versioned dataset/model/checkpoint artifacts, deterministic evaluation dataset, deployment rollback, per-request trace, SLO/error budget and an explicit owner for artifacts between Data -> Train/Tune -> Serve. Security and storage policies apply throughout the pipeline.

Primary docs: [Ray Train PyTorch quickstart](https://docs.ray.io/en/latest/train/getting-started-pytorch.html), [Train checkpoints](https://docs.ray.io/en/latest/train/user-guides/checkpoints.html), [Persistent storage](https://docs.ray.io/en/latest/train/user-guides/persistent-storage.html), [Ray Serve production practices](https://docs.ray.io/en/latest/serve/production-guide/best-practices.html), [Ray Serve autoscaling](https://docs.ray.io/en/latest/serve/autoscaling-guide.html). For Data/Tune APIs open the matching installed release documentation before writing code.
