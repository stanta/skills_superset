---
name: blockchain-node-architect
description: >-
  This skill should be used when designing, implementing, reviewing, benchmarking or operating blockchain nodes: full/archive/light/RPC nodes, validators, sentries, bootnodes, execution and consensus clients, P2P networking, sync, fork choice, state storage and reorg recovery. Covers Bitcoin/UTXO, Ethereum/EVM, Solana/Agave, CometBFT/ABCI and rollup nodes. Use also for Russian requests: архитектура блокчейн-ноды, валидатор, синхронизация, P2P, форк, реорганизация, консенсус.
metadata:
  domain: blockchain-infrastructure
  role: architecture
  scope: design-review-implementation
  related-skills: architecture-designer, microservices-architect, rust-engineer, sre-engineer, security-reviewer, the-fool
---

# Blockchain Node Architect

Проектировать ноду как **проверяющую машину состояний с ненадёжной сетью и восстанавливаемым хранилищем**, а не как обычный API-сервис. Производительность не может менять правила консенсуса. Начинать с протокольной спецификации и модели доверия; проверять каждую оптимизацию на безопасность, восстановление и реорганизации.

## Когда применять

- Разработка новой блокчейн-ноды или независимого клиента; аудит существующего full node, archive node, validator, RPC, light client или L2 derivation node.
- Выбор компонентов P2P, mempool, block import, execution, fork choice, state, indexing, snapshot, RPC, signer; миграция монолита на модули.
- Оптимизация initial sync, latency, TPS, read amplification, хранения и GC без ослабления валидации.
- Подготовка ADR, threat model, отказоустойчивой топологии, тестового плана и операционных runbooks.

Не подменять этим скиллом действующие consensus specs конкретной цепи. Перед применением протокольных чисел, fork schedule, параметров клиента и аппаратных требований проверять актуальные спецификации и версию реализации; фиксировать commit/tag и network/chain ID.

## Принципы, которые нельзя нарушать

1. **Consensus correctness first.** Правила проверки блока/транзакции — детерминированная версионированная часть protocol kernel. Нельзя «ускорить» узел пропуском обязательных проверок, произвольной финализацией или принятием remote RPC за истину.
2. **Разделять известное, валидированное, canonical и finalized.** Head, safe/finalized, optimistic, snapshot-assumed и historical-validated — разные состояния с разными гарантиями. Никогда не показывать их пользователю как взаимозаменяемые.
3. **Crash consistency.** Зафиксировать порядок durable writes, атомарность canonical-head transition, журнал/undo или эквивалентное восстановление, правила fsync/checkpoint. Перезапуск между любыми двумя шагами не должен создавать подтверждённое, но недоказуемое состояние.
4. **Reorg is normal.** Индексы, уведомления и кэши должны быть привязаны к block hash и иметь detach/attach либо явную invalidation. Finality определяется протоколом; не «N подтверждений» для всех сетей.
5. **P2P is hostile.** Все сообщения, snapshot chunks, peer metadata и RPC — недоверенный ввод; ограничивать размер, глубину, CPU, память, диск, число соединений и очередь на каждом этапе.
6. **Validator safety before availability.** Единоличный активный signer на ключ/домен, долговечная история подписей и fenced failover. Два одновременно активных валидатора с одним ключом могут нарушить slashing safety.
7. **Modularity without accidental distributed consensus.** Разделять кодовые границы прежде чем дробить по процессам. Внутренние очереди, сеть и Raft не заменяют on-chain fork choice/consensus.

## Рабочий процесс

### 1. Зафиксировать профиль и источник истины

Составить карточку: chain/network/genesis; consensus family (PoW, PoS, BFT, rollup), client version/fork; тип ноды; уровень доверия к snapshot/checkpoint; роль в proposer/voter; требуемая история; RPC и типы потребителей; существующее состояние и ограничения. Отдельно записать latency budget, steady-state throughput, worst-case reorg, допустимое отставание, disk growth, RTO/RPO, стоимость и требования к геораспределению.

Выделить source of truth по убыванию: активная спецификация сети и тестовые векторы → проверяемая реализация/релиз клиента → официальные руководства оператора → проверенные исследования. Внешние советы, benchmarks и будущие EIP не считать активным протоколом.

### 2. Сформулировать инварианты и границы доверия

Описать валидность header/block/transaction, переход state, fork choice, safe/finalized transitions, подписные запреты и contract для genesis/fork upgrades. Задать входы, side effects и точку durable acknowledgement. Провести threat model: невалидные блоки, eclipse/Sybil, DoS, state poisoning, snapshot substitution, disk exhaustion, rollback signing history, утечка RPC и ключей.

### 3. Декомпозировать по функциям

Проверить необходимость следующих границ, **не создавая микросервисы автоматически**:

- **Network:** discovery, handshake/version negotiation, encrypted transport где предусмотрен протоколом, peer diversity, gossip и block/transaction request-response.
- **Ingress:** дешёвая валидация формата, дешёвые фильтры, dedup, очереди и приоритет блоков над второстепенным трафиком.
- **Consensus/fork choice:** проверка протокольных сообщений, веса/голоса и canonical/safe/finalized указатели.
- **Execution/validation:** детерминированная проверка блока и state transition без сетевых вызовов в критическом пути.
- **Storage:** immutable blocks/receipts, mutable canonical state, fork/undo history, snapshots, отдельные необязательные индексы.
- **Txpool:** admission, nonce/conflict handling, per-peer caps, fee policies и reorg reinsertion без влияния на валидность блока.
- **Serving:** read RPC, write RPC, subscriptions/indexers, rate limits; validator signer и admin API в отдельной зоне доступа.

Для Ethereum PoS учитывать фактическое разделение EL/CL/validator и аутентифицированный Engine API. Для CometBFT — ABCI boundary. Для Bitcoin/UTXO — chainstate и block index. Для Solana/Agave — высокопроизводительные replay, accounts и ledger/snapshot subsystems. Не переносить чужой pipeline буквально: сначала сопоставить protocol invariants.

### 4. Спроектировать dataflow и синхронизацию

Показать путь peer → bounded decode → header/consensus validation → body/data availability → execution/state transition → state-root check → durable commit → fork choice/canonical update → index/event publication. Определить независимые фазы download и verify, лимиты in-flight и end-to-end backpressure.

Сравнить genesis/full replay, headers-first, snap/state sync, checkpoint sync, light verification и archive backfill по CPU, bandwidth, disk, latency и явным trust assumptions. Snapshot принимать только при проверяемом commitment/корне состояния и корректном доверенном якоре; если модель сети позволяет, предусмотреть background historical validation. Явно указать, какого исторического материала узел после sync **не имеет**.

### 5. Спроектировать хранение и reorg

Выбрать UTXO set или account/state representation по протоколу; отделить hot state от immutable history, secondary indices и snapshots. Для каждого хранилища задать versioning, migrations, checksums, retention/pruning, space amplification, compaction, cache budgets и тест восстановления.

Описать attach/detach атомарно или через восстанавливаемую операцию; хранить ancestry/undo до требуемой глубины и не удалять данные, необходимые для разрешённых reorg/доказательств. У подписчиков событий — cursor, block hash, retracted/replaced события и идемпотентное применение. Сохранять валидную историю подписей вне процедуры rollback chainstate.

### 6. Защитить сеть, RPC и ключи

Ввести peer scoring/diversity, независимые bootstrap-источники, лимиты соединений и сообщений, запрет бесконечных retries, таймауты, per-peer/per-IP budget и изоляцию resource pools. Применять уместный транспорт/spec конкретного протокола; libp2p/Gossipsub — пример, не универсальный стандарт для всех цепей.

RPC и admin интерфейсы разделить; запретить публичный Engine API, небезопасные admin/debug endpoints и signer; ограничить expensive queries и подписки. Secrets/signing keys не хранить в образах, логах, снапшотах или базе индексов. Валидатору задать single-writer fencing и проверяемый switchover.

### 7. Доказать свойства экспериментами

Составить тестовую матрицу из [security-and-operations.md](references/security-and-operations.md): unit/property/fuzz для codec и state transitions; differential tests против независимого клиента/официальных vectors; reorg и finality edge cases; fault injection в каждую точку commit; snapshot tampering; peer eclipse/DoS; slow disk, partition, restart, protocol upgrade и устаревшие signing records. Замерять p50/p95/p99 при заданных workload, высоте сети, состоянии БД, cache hit ratio и hardware. Не выдавать synthetic TPS за mainnet TPS.

### 8. Выдать проверяемый пакет решений

Сформировать пакет по [delivery-templates.md](references/delivery-templates.md): assumptions, annotated component/dataflow diagram, trust boundaries, invariants, ADR с альтернативами, failure-mode table, state/storage/reorg protocol, sync trust matrix, SLO/metrics, test matrix, capacity model, rollout/rollback и unresolved risks. Каждое значимое решение сопровождать проверяемым критерием.

## Быстрый выбор справочника

- [architecture-patterns.md](references/architecture-patterns.md): модульные границы, storage, staged import, sync, chain-family и rollup варианты.
- [security-and-operations.md](references/security-and-operations.md): угрозы, validator safety, observability, тесты, SRE и релизы.
- [delivery-templates.md](references/delivery-templates.md): шаблоны архитектуры, ADR, решений, NFR и acceptance.
- [sources.md](references/sources.md): первичные спецификации и официальные implementation references; сверять freshness и версию перед использованием.

## Что считать ошибкой дизайна

- Равнять доступность RPC с валидностью цепи либо приравнивать snapshot-assumed к independently-validated.
- Хранить только height без block hash для транзакций/индексов/событий.
- Подписывать одним ключом в active-active; восстанавливать signer без signing history.
- Применять блок до проверки consensus-critical данных и без сценария crash/reorg recovery.
- Считать checkpoint «полностью trustless», если его provenance не проверен.
- Бесконтрольная параллельная загрузка, unbounded mempool/queues, открытый privileged RPC.
- Проводить load test без воспроизводимого workload, состояния БД и fault tests.

**Критерий готовности:** другой инженер может по документу реализовать ноду, назвать точные гарантии для каждого состояния, воспроизвести корректный reorg и восстановление после crash, развернуть безопасный валидатор и подтвердить свойства тестами — без недокументированных предположений.
