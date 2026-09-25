# Архитектурные паттерны блокчейн-нод

Этот справочник дополняет [SKILL.md](../SKILL.md). Паттерны применяются только после фиксации consensus rules и роли узла. **Свойства конкретной цепи имеют приоритет над примерами.**

## 1. Структура и границы

~~~mermaid
flowchart LR
  P2P[P2P: discovery / transport] --> Gate[Bounded ingress / admission]
  Gate --> Sync[Headers / bodies / sync]
  Gate --> Tx[Txpool]
  Sync --> Validate[Protocol validation / execution]
  Tx --> Validate
  Validate --> State[(Canonical state / WAL)]
  Validate --> History[(Blocks / receipts / undo)]
  State --> Fork[Fork choice and finality]
  History --> Fork
  Fork --> Events[Reorg-aware events / indexers]
  State --> RPC[Read RPC]
  History --> RPC
  Fork --> RPC
  Signer[Isolated validator signer] --> Fork
~~~

Диаграмма логическая, **не** требование разнести блоки по хостам. Реальный validator часто имеет более строгую последовательность proposal/vote и не должен зависеть от RPC/indexer.

| Граница | Основной контракт | Тип отказа и защита |
| --- | --- | --- |
| P2P → ingress | byte budget, protocol version, message ID, peer ID | oversize, malformed, flooding; early reject |
| Ingress → sync | validated header metadata, bounded work item | duplicate/fork spam; quotas and priorities |
| Sync → execution | available block body, parent state, fork ruleset | missing parent, stale fork; staging and retry |
| Execution → state | transition result and expected commitment | invalid block; no canonical side effects |
| State → fork choice | durable state version plus block hash | crash/reorg; recoverable transaction or WAL |
| Fork choice → indexer | attach/detach, canonical generation, cursor | duplicate/out-of-order; idempotency |
| RPC → storage | consistency/finality level and cost budget | expensive scans; rate/CPU/I/O limits |
| Consensus → signer | chain domain, slot/height, proposal/vote intent | double signing; durable protection and fencing |

### Не смешивать три оси

1. **Модуль / процесс:** in-process boundaries могут быть достаточны. Cross-process API добавляет новые частичные отказы.
2. **Replication / consensus:** несколько RPC replicas на одном consensus source не являются независимыми full validators. Собственный Raft у backend не может выбирать canonical head.
3. **Availability / safety:** автоматический failover безопасен для read-only RPC не по тем же правилам, что failover signer.

## 2. Pipeline импорта и управление ресурсами

Проводить данные через стадии: discovery → header verification → body availability → contextual validation → execution → commitment check → durable commit → canonicalization → asynchronous indexing. Для PoS consensus/fork-choice этапы могут управлять импортом и запрашивать execution; diagram нужно адаптировать.

- Назначить **bounded queue** и bytes/CPU budget для каждой стадии; backpressure распространять вверх по pipeline.
- Разделить дешёвую syntax screening и дорогую consensus verification; результат ранней проверки не является подтверждением блока.
- Параллелить независимые операции (download, hashing, signature precheck, independent read-only index tasks), но сериализовать конфликтующие state commits там, где требует модель состояния.
- Закрепить ownership: кто выбирает кандидата, кто выполняет переход, кто ставит канонический указатель, кто сообщает RPC, что блок «готов».
- Использовать checkpoints стадий и reversible/unwind semantics. Пример: Reth stages имеют execute и unwind; при reorg индекс и state не должны оставаться на разных heads.
- Выносить analytics, optional index, explorer enrichment и notification из consensus-critical path. Потеря индексатора не должна останавливать корректную валидацию.

**Минимальная спецификация очереди:** входное ограничение по bytes/items; приоритеты; deadline; отмена при смене fork; допустимый повтор; ключ дедупликации; обработка overload; метрика wait time. «Exactly once» через сеть не предполагать: доставка может повториться, эффект должен быть idempotent или transactional.

## 3. State, immutable history и crash consistency

### Уровни хранения

| Класс данных | Свойства | Операция восстановления |
| --- | --- | --- |
| Header/block graph | hash-addressed, fork-aware, potentially immutable | peer refetch, checksum |
| Canonical state | актуальное состояние для конкретного block hash/state root | replay, versioned state or verified snapshot |
| Undo/revert data | откат допустимых reorg | detach old branch; never prune too early |
| Receipts/logs/events | привязаны к block hash и canonicality | retract/re-emit; rebuild optional indexes |
| Mempool | эфемерное содержимое и локальная политика | reload/re-admit; safe to lose if documented |
| Validator signing history | монотонная, security critical, **не** chain rollback | safe restore/fencing independent of chainstate |
| Snapshots | versioned data + commitment + manifest | verify source, state root/hash, version and trust anchor |

Для Bitcoin/UTXO — согласованное обновление UTXO set, block index и необходимых undo records. Для EVM/account chains — versioned state/trie и receipts/storage индексы согласно клиенту; не навязывать UTXO модель. В высокопараллельных runtime учитывать optimistic execution и detect conflicts, но итоговый transition обязан соответствовать протоколу.

### Commit protocol — логический, не универсальная последовательность

1. Проверить parent, ruleset и обязательные proofs/commitments.
2. Рассчитать переход на изолированной версии или recoverable overlay.
3. Durable persist блока, необходимого state/undo и journal с достаточными ordering guarantees.
4. Атомарно либо recoverably сменить canonical head; сделать checkpoint прогресса.
5. Только после этого выпустить canonical-visible события и отметить RPC readiness.
6. На старте закончить/откатить незавершённую операцию; проверить pointers, roots и соответствие индексов.

Детали fsync, transaction boundaries, separate DB/FS должны быть подтверждены тестами на выбранной ОС и storage engine. Нельзя предполагать атомарность между разными БД, файловой системой и Kafka без протокола согласования/outbox.

### Reorg protocol

- Вычислить common ancestor, убедиться в допустимости reorg для данного консенсуса и проверить новую ветку.
- Detach старые canonical blocks в обратном порядке и attach новые в прямом, либо применить эквивалентный MVCC switch.
- Для каждого изменения обновить canonical generation, state root, receipts/index references; optional downstream индексаторы получают revert events.
- Событийный ключ: (chain_id, block_hash, tx_hash/tx_index, log_index, event_type, canonical_generation) по фактической модели цепи. Height сам по себе не уникален.
- Не «откатывать finality» обычным скриптом. Нарушение финальности — отдельный protocol/security incident.

## 4. Initial sync как отдельный режим

| Подход | Что локально доказывается | Дополнительные предпосылки/издержки |
| --- | --- | --- |
| Genesis/full replay | исторические transitions по spec | CPU, I/O, bandwidth, время |
| Headers-first | валидная header chain до загрузки body | заголовки сами по себе не доказывают state transition |
| Snapshot/state sync | commitment и переходы после snapshot | достоверность trust anchor и корректность snapshot; возможна утрата истории |
| Checkpoint/weak subjectivity | chain после доверенного свежего checkpoint | источник checkpoint и его актуальность — часть модели доверия |
| Optimistic sync | временно принятая структура до полного execution verdict | invalidated blocks нельзя выдавать за validated/canonical finalized |
| Archive/backfill | исторический state/receipts для запросов | дополнительные storage/index/retention ресурсы |

Проверять manifest: chain ID, genesis hash, protocol/state format version, snapshot height/hash, commitment, hashes chunks, checksum, quorum/peer diversity там, где применимо. Отмечать provenance отдельно от криптографической проверки. При неполной истории явно обозначать, какие API и аудит недоступны. Для длительного offline PoS узла требовать обновления trusted checkpoint по spec.

**Bitcoin AssumeUTXO:** полезный конкретный вариант «быстрый active snapshot + фоновая историческая валидация». Это не разрешение всем протоколам считать произвольный downloaded snapshot доверенным.

## 5. Сеть, mempool, API

- Discovery: seed/bootstrap из нескольких независимых сетевых доменов, peer identity, version/capability handshake, inbound/outbound mix, diversity по AS/IP/subnet при релевантности. Избегать единственного seed как предпосылки liveness.
- Dissemination: различать pubsub gossip, request/response и direct/explicit peers; ограничивать сообщения до дорогой проверки; измерять end-to-end propagation, а не только «сообщение отправлено».
- Peer scoring: локальные поведенческие сигналы, decay, ограничения по ресурсам и whitelist с явно описанным риском. Не превращать score в protocol truth.
- Txpool: admission и prioritization — локальная политика; валидность блока не должна зависеть от того, видел ли узел его транзакции в mempool.
- Public RPC: явный consistency level (pending, latest/optimistic, safe/finalized при поддержке), query budget, pagination, subscription lifecycle, cost/rate controls, отдельно admin и authenticated internal API.
- Indexers: read-only, eventually consistent, backfill/reorg capable, наблюдаемый lag. Отдельно документировать SLA freshness и reorg notifications.

## 6. Выбор по семейству протокола

| Семейство | Протокольно-специфичное ограничение |
| --- | --- |
| Bitcoin-like PoW/UTXO | chainwork/header validation, UTXO/undo, block graph, pruning и ограничения reorg |
| Ethereum PoS | EL/CL/validator, Engine API JWT, LMD-GHOST/finality по актуальным specs, payload VALID/INVALID/SYNCING |
| CometBFT/ABCI++ | consensus/application split, deterministic AppHash, app state sync verification, validator voting state |
| Solana/Agave | gossip/retransmit, replay, accounts/ledger, snapshot provenance, vote/root handling по версии клиента |
| Optimistic/ZK rollup | L1 derivation/DA, batch/source verification, sequencer unsafe/safe/finalized heads, proof/challenge model |
| Permissioned BFT | membership/quorum, epoch changes, evidence, fault assumption и durability голосов |

Не смешивать **chain-specific canonicality** и **L1 settlement finality** в L2 API. Для rollup отдельно зафиксировать зависимость от L1 RPC, DA и sequencer liveness.

Дополнительные источники по каждому примеру — [sources.md](sources.md).
