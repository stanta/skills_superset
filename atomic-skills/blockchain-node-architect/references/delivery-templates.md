# Шаблоны результата для проектирования blockchain node

Использовать выборочно: маленькому RPC proxy не нужна многостраничная BFT спецификация, но validator и новый client обязаны получить полный safety case.

## A. Architecture decision packet

~~~markdown
# Node architecture: <chain/network, client version, role>

## 1. Scope and evidence
- Role: full / archive / light / validator / sentry / bootnode / RPC / L2 derivation.
- Protocol: genesis ID, fork schedule, consensus/execution spec revision.
- Evidence ledger: claim -> primary source URL + tag/commit -> fact/inference/assumption.
- Out of scope / known unknowns.

## 2. Requirements and trust
- Functional: imports, validates, serves, signs, indexes, syncs.
- NFR: block import budget, RPC SLO, max sync lag, disk growth, RTO/RPO.
- Trust: checkpoint/snapshot provenance, remote L1/DA/RPC dependencies, keys.

## 3. Invariants
- Validated state is computed from a valid parent under protocol rules.
- Canonical/finalized pointers match consensus fork-choice rules.
- Crash/restart preserves acknowledged state and signing safety.
- Reorg detach/attach converges state, events and indexes.

## 4. Architecture
- Component diagram: P2P, consensus, execution, state, storage, txpool, RPC, signer.
- Dataflow: ingress -> validation -> commit -> fork choice -> downstream.
- Trust boundaries and resource budgets per stage.
- Storage and pruning, snapshot and reorg/undo design.

## 5. Decisions
- ADR links; chosen alternatives and rejected options with costs.
- Chain-family constraints and protocol-specific exceptions.

## 6. Failure/recovery
- Invalid block, network partition, snapshot corruption, disk-full, crash,
  stale signer, duplicate event, reorg, fork upgrade.
- Detection, isolation, durable recovery and manual authority gates.

## 7. Test and rollout
- Test vectors, differential/fuzz/property, fault injection, benchmark protocol.
- SLOs/alerts, canary, rollback criteria, operator runbooks, open risks.
~~~

## B. ADR с проверяемой альтернативой

~~~markdown
# ADR-NNN: <название>
Status: proposed | accepted | superseded
Context: <версия протокола, workload, bottleneck, trust constraints>
Safety invariants: <что изменение не вправе нарушить>
Options:
  A. <вариант> — correctness, latency, cost, complexity, rollback.
  B. <вариант> — correctness, latency, cost, complexity, rollback.
Decision: <какой вариант и почему>
Consequences: <positive, negative, irreversible, operational>
Experiment: <baseline, workload, metrics, attack/reorg/crash test>
Rollback: <какие данные совместимы и безопасный порядок действий>
Evidence: <spec links + commit/tag + test/benchmark artifacts>
~~~

Правило: ADR для storage или sync считается неполным, если не описывает **reorg/crash path** и trust assumptions.

## C. Таблица оценки вариантов sync

| Вариант | Исторические данные доступны? | Локальная проверка | Trusted anchor | RTO на запуск | Диск/сеть/CPU | Риски |
| --- | --- | --- | --- | --- | --- | --- |
| Genesis replay | заполнить | заполнить | заполнить | измерить | измерить | заполнить |
| Snapshot + background validation | заполнить | заполнить | заполнить | измерить | измерить | заполнить |
| Weak-subjectivity checkpoint | заполнить | заполнить | заполнить | измерить | измерить | заполнить |
| Light verification | заполнить | заполнить | заполнить | измерить | измерить | заполнить |

Никогда не заполнять модель доверия словом «trustless» без объяснения, какие commitments и подписи проверяются локально.

## D. Acceptance matrix

| Требование/инвариант | Дизайн-элемент | Тест/инъекция отказа | Измерение | Pass criterion |
| --- | --- | --- | --- | --- |
| no invalid canonical block | validation + fork choice | invalid block corpus | head hash vs oracle | точное совпадение |
| crash-safe commit | WAL/atomic pointer | kill each commit step | restored root/head | согласованы |
| reorg correctness | undo/MVCC + index events | competing fork | state and index hash | совпадают с replay |
| bounded adversarial input | resource manager | malicious peers | peak CPU/RAM/FD | ниже заявленных бюджетов |
| no double signing | fenced signer + history | simultaneous failover | conflicting signatures | 0 |
| honest sync readiness | trust-aware API | incomplete/stale snapshot | readiness and status | не объявлять verified |
| sustainable performance | staged import | realistic RPC + sync | p99 lag, throughput | заявленный SLO |

Адаптировать критерии к chain spec; утверждение «0 конфликтующих подписей» относится к локальному signer и проверяется под контролируемым failover.

## E. Список решений перед разработкой

- [ ] Точно определены роль ноды, protocol/fork версия, chain ID и правила finality.
- [ ] НФТ/наблюдаемость определены для sync и steady state отдельно.
- [ ] Доказан state transition, а не только успешный P2P broadcast.
- [ ] Canonical, safe, finalized, optimistic и snapshot-assumed статусы не перепутаны.
- [ ] Для каждой очереди установлены budget/backpressure и overload behavior.
- [ ] Для каждого durable write есть crash/replay или atomic transaction case.
- [ ] Snapshot trust anchor и state commitment проходят tampering test.
- [ ] Протокол reorg охватывает state, receipts, RPC, индексы, кэши и подписчиков.
- [ ] Signing safety независима от replica failover и chainstate restore.
- [ ] Privileged RPC и signer не доступны через публичный edge.
- [ ] Testnet/fuzz/differential/reorg/crash/load тесты запускаются воспроизводимо.
- [ ] Есть rollback runbook и ограничения на unsafe DB downgrade.
