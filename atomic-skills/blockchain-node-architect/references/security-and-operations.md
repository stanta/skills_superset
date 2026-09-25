# Безопасность, эксплуатация и верификация blockchain node

Справочник для [blockchain-node-architect](../SKILL.md). Проверять утверждения относительно **версии протокола, роли узла и топологии**. Отделять safety (не принимать невалидную цепь/не делать двойную подпись) от liveness (не пропускать очередные блоки/голоса) и availability (обслуживать запросы).

## 1. Threat model по границам

| Актив/граница | Угроза | Защитные меры | Проверка |
| --- | --- | --- | --- |
| Peer discovery | eclipse/Sybil, poisoned bootstrap | diversity, bounded inbound/outbound slots, независимые seeds, peer scoring | контролируемый eclipse, восстановление связности |
| Transport/codec | oversized frames, decompression bomb, parser ambiguity | max bytes/nesting/time, canonical encoding, fuzz/property tests | malformed corpus, CPU/memory budgets |
| Block/tx ingress | CPU/IO amplification, invalid proofs, hash flooding | cheap prefilter, quotas per peer, independent expensive-work budget | adversarial flood; no starvation of valid blocks |
| Gossip | propagation suppression, invalid message relay | message ID/dedup, scoring, mesh health, direct peers при допустимости | split topology/partition experiment |
| Sync/snapshot | malicious/truncated snapshot, wrong chain ID, stale checkpoint | verify commitment + trusted anchor + manifest; require source provenance | corrupt chunk, wrong root, stale anchor |
| State/disk | partial commit, bit rot, storage exhaustion, delayed compaction | recoverable log/atomicity, checksums, disk reserve, restore drills | crash at each durable boundary, disk-full |
| RPC/admin | public privileged endpoints, CPU-expensive queries, data leaks | listen ACL, auth where applicable, rate/size limits, network separation | unauthorized access, burst load |
| Validator signer | stolen key, concurrent signer, rollback of signing DB | least privilege, signer isolation, durable slashing protection, fencing | two-node failover and rollback test |
| Software supply chain | compromised dependency/image or protocol mismatch | pin tags/digests, signed releases where supported, independent build verification | reproducible config/build, dependency audit |
| Operator/update | incompatible DB/fork rollout, bad config | testnet/canary, backup/restore, compatibility matrix, reversible runbook | upgrade and rollback game day |

**Не включать секретные ключи в snapshots/diagnostic bundles.** Логи peer IDs/IP и транзакций могут быть персональными данными; установить retention и доступ по необходимости.

## 2. P2P: управление ресурсами и peer diversity

- Лимиты: connections, streams, memory, queued messages/bytes, in-flight block requests, DB reads, CPU-bound signature/proof verification, bandwidth, deadlines. Проверять как глобальные, так и per-peer/per-prefix лимиты.
- Разделить pools: consensus-critical traffic, block sync, transaction gossip, read RPC и background indexing не должны взаимно вытеснять друг друга без осознанной политики.
- Настроить retry budget и circuit breaking для remote dependencies; не ретраить бесконечно невалидные данные и не блокировать глобальную очередь одним медленным peer.
- Оценить topology: число peers, доля outbound, независимые AS/подсети/регионы, peer churn, time to first block, block propagation tail.
- При Gossipsub использовать спецификацию версии (peer score, adaptive gossip, optional explicit peers), но не копировать параметры без load/attack тестов. Explicit peering снижает некоторые риски eclipse, но не заменяет diversity.
- Любой ban/score — **локальная защита**, а не критерий валидности цепи; тестировать false positives и reset/decay.

## 3. Validator safety и ключи

Проводить отдельный design review для validator/proposer/voter, даже если full node уже безопасен.

1. Привязать ключ и подпись к правильным chain/genesis/fork domains и duties.
2. До выдачи подписи проверять историю несовместимых подписей; сохранение записи должно быть durable по гарантиям signer implementation.
3. Обеспечить single active authority: lease/fencing, защита от split brain, controlled key transfer; не запускать active-active с одним ключом.
4. Backup и restore signing-history согласовать с key material. Старый backup самой ноды **не** разрешает signer откатываться и переподписывать.
5. Для Ethereum при миграции учитывать EIP-3076 и официальные правила экспорта/импорта; перед переносом остановить старый signer, переносить полный допустимый signing history, затем безопасно активировать новый.
6. Для CometBFT и других BFT проверить собственные файлы/signing state, double-vote/evidence rules и supported remote signer/failover. Не переносить EIP-3076 на чужие протоколы.
7. Продумать outage: умеренный missed duty может быть безопаснее необоснованного failover. RTO для validator задавать после safety analysis.

Отдельные signer health метрики: conflicting-signature rejection, unexpected domain/height, clock skew, key-authority mismatch, storage durability errors.

## 4. Observability: мерить свойства, не только uptime

**Минимальная телеметрия с chain/network/client-version labels:**

- known header height, downloaded height, executed/validated height, canonical head hash/height, safe/finalized hash/height (если применимо), highest trusted checkpoint, IBD/sync stage и прогресс background validation;
- head lag относительно нескольких независимых peers/источников с пометкой uncertainty; local wall clock/peer clock skew;
- block import latency p50/p95/p99, execution CPU, queue wait/bytes, verification failure categories, commit fsync latency, storage stalls, cache hit/miss, compaction backlog, disk free/daily growth;
- peer count by inbound/outbound/network diversity, churn, handshake failures, mesh/gossip delay и rejected message counts;
- reorg count/depth/common ancestor, indexer cursor vs canonical generation, receipts/event retract backlog;
- RPC p95/p99 по method+consistency, rate-limit actions, expensive-query CPU, error rates и queue saturation;
- validator duties performed/missed, signed messages, signing DB health и slashable-attempt rejection (без записи приватных данных).

При алертах различать **«узел online»**, **«узел отстаёт»**, **«состояние недоверенно»** и **«validator unsafe»**. Пример: успешный HTTP healthcheck при блокированном block import не означает здоровье ноды.

SLO формировать из пользовательского сценария: sync readiness, lag, p99 RPC, successful canonical updates, missed validator duties, RPO/RTO. Численные пороги — измеряемые параметры конкретной сети, а не универсальные константы.

## 5. Test matrix: adversarial + deterministic

| Уровень | Сценарий | Обязательный oracle / invariant |
| --- | --- | --- |
| Codec/fuzz | malformed length, nesting, crypto edge, replay | no panic/UB/OOM, bounded resources, reject invalid |
| State unit/property | same valid block + same parent/ruleset | deterministic state root/UTXO set |
| Consensus/fork choice | competing forks, equivocation, finality edge | reference spec and test vectors |
| Differential | same blocks across independent implementations | identical canonical state/receipts where spec requires |
| Sync | genesis, headers-first, corrupt snapshots, stale checkpoint | correctly classified trust + verified commitments |
| Crash consistency | kill before/after each WAL, state, head and index stage | deterministic replay/rollback, no phantom acknowledged block |
| Reorg | short/deep allowed reorg during txpool/indexer/RPC load | state, indices, event retract/attach all converge |
| Network | eclipse, partition, high latency, clock skew, byzantine peers | no invalid state; liveness recovers under model |
| Disk | disk-full, slow fsync, DB corruption, restart during compaction | fail safe, no silent canonical corruption |
| Validator | simultaneous replicas, outdated signing backup, failover, time skew | no conflicting signature emitted |
| Upgrade | rolling version skew, hard fork boundary, DB migration and rollback | correct protocol selection and state preservation |
| Load | realistic head following + RPC + reorg + historical queries | p99 SLO within declared hardware and budgets |

Зафиксировать **seed**, workload, hardware, DB size, block height, fork version, cache warm/cold и expected result. Для performance regression хранить baseline и variance; cold-cache IBD нельзя сравнивать с прогретым steady-state.

Использовать модельные проверки (TLA+/state-machine model checking), когда ошибка конкурентного commit/finality/signing порядка опасна; отдельная formal spec не заменяет integration tests реальных БД и сети.

## 6. Capacity и SRE

- Считать отдельно steady state, initial sync, archive backfill и worst-case reorg. Для каждого оценить input bytes/s, verification CPU/s, write amplification, storage/day, compaction bursts, spare capacity.
- Проверять системные лимиты: file descriptors, sockets, ephemeral ports, network queues, IO scheduler, filesystem и corruption strategy. Указывать версии kernel/storage engine, NUMA/SSD профиль только после измерений.
- Выделить disk reserve и защиту от disk-full; тестировать graceful degradation read RPC до полной остановки node.
- Snapshot backup проверять restore, а не только создание. Зафиксировать совместимость snapshot version/chain/fork и различие between backup of state и signing-history.
- Для зависимых услуг (L1 RPC, DA, sequencer, remote signer, KMS) задать outage behavior; отдельная operational зависимость не должна незаметно менять consensus validity.
- Canaries: сначала isolated testnet → shadow/read-only или non-signing observer → ограниченный production rollout. Validator key migration — отдельный, ручной, проверяемый шаг.
- Incident runbook: isolate faulty signer; record state/head/hash and client versions; preserve evidence; verify checkpoint and chain divergence; restore from verified state; reconcile indexers and reorg events; resume signing only after anti-slashing checks.

## 7. Архитектурный pre-mortem

Перед approval дать 3–5 конкретных контрпримеров: «что если snapshot имеет корректный transport checksum, но неверный root?», «что если подписной WAL откатился после failover?», «что если node догнала header head, но execution на 50k блоков позади?», «что если reorg пришёл во время публикации индексатору?», «что если peer-score изолировал честных peers?». Для каждого зафиксировать detection, containment, recovery и тест. Общие фразы «добавить мониторинг» не засчитывать.

Источники спецификаций и операторских рекомендаций: [sources.md](sources.md).
