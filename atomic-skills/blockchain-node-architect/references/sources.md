# Primary sources and evidence map

Проверено по официальным спецификациям/документации и исходным design notes на **2026-09-25**. Версии протоколов и реализации меняются: перед production-проектированием закреплять конкретный tag/commit и актуальный fork schedule сети. Это справочник источников, а не гарантия, что все ссылки описывают одинаковую chain architecture.

## Protocol specifications — source of truth

1. [Ethereum consensus specifications](https://ethereum.github.io/consensus-specs/) — beacon consensus, fork choice, finality, upgrades и тестовые векторы. Использовать конкретную активную для сети версию; не копировать константы из произвольной старой фазы.
2. [Ethereum execution specifications (EELS)](https://github.com/ethereum/execution-specs) и [официальное описание](https://steel.ethereum.foundation/docs/execution-specs/specs/) — state transition и execution rules как проверяемая reference реализация; сверять с активной сетью.
3. [Ethereum node architecture](https://ethereum.org/developers/docs/nodes-and-clients/node-architecture) — граница EL/CL/validator, P2P и Engine API. Документ актуализирован в 2026 году; детали endpoints и настроек брать из versioned client docs.
4. [Ethereum run a node](https://ethereum.org/developers/docs/nodes-and-clients/run-a-node) — authenticated Engine API/JWT, operator setup и тестнет перед production.
5. [Ethereum weak subjectivity](https://ethereum.org/developers/docs/consensus-mechanisms/pos/weak-subjectivity) — trust assumption для новых и долго offline PoS узлов.

## Implementation design references

6. [Bitcoin Core P2P developer guide](https://developer.bitcoin.org/devguide/p2p_network.html) — концепция headers-first и блоковая доставка. Руководство содержит исторические примеры версий: не считать старые детали действующими defaults.
7. [Bitcoin Core AssumeUTXO design](https://github.com/bitcoin/bitcoin/blob/master/doc/design/assumeutxo.md) — отдельные chainstates, active snapshot, background full validation, проверка commitment, восстановление после restart. Привязывать к commit конкретного Bitcoin Core release.
8. [Reth staged sync design](https://github.com/paradigmxyz/reth/blob/main/docs/crates/stages.md) — pipeline stages, state/index updates и unwind. Паттерн реализации, **не** норма Ethereum consensus.
9. [CometBFT ABCI++ application requirements](https://github.com/cometbft/cometbft/blob/main/spec/abci/abci%2B%2B_app_requirements.md) — consensus/application boundary, snapshot/state sync, AppHash verification и история блоков после восстановления.
10. [CometBFT light-client specification](https://github.com/cometbft/cometbft/blob/main/spec/light-client/README.md) — trusted header/validator set, signature verification и attack detection; спецификация может содержать WIP разделы.
11. [libp2p Gossipsub v1.1 specification](https://github.com/libp2p/specs/blob/master/pubsub/gossipsub/gossipsub-v1.1.md) — peer scoring, adaptive gossip, explicit peering и eclipse/Sybil mitigations. Параметры настраивать и тестировать под собственный workload.
12. [libp2p Gossipsub specs index](https://github.com/libp2p/specs/blob/master/pubsub/gossipsub/README.md) — версионирование протокола и implementation status.
13. [Agave validator documentation](https://docs.anza.xyz/) и [Agave operations best practices](https://docs.anza.xyz/operations/best-practices/general) — Solana/Agave operations. Актуальные hardware и флаги смотреть в [requirements](https://docs.anza.xyz/operations/requirements) и docs конкретного релиза.
14. [EIP-3076: Slashing Protection Interchange Format](https://eips.ethereum.org/EIPS/eip-3076) — transfer подписной истории Ethereum validator при миграции; проверять статус EIP и совместимость поддерживаемых клиентов.

## Evidence → decision crosswalk

| Решение | Исходные свидетельства | Что является инженерным выводом этого скилла |
| --- | --- | --- |
| EL/CL/validator separation | Ethereum node architecture; consensus specs | изолировать signer и auth Engine API по trust boundaries |
| Reversible staged import | Reth stages/unwind; Bitcoin chainstates | commit protocol, bounded queues, reorg-aware secondary indexes |
| Snapshot trust matrix | Bitcoin AssumeUTXO; CometBFT state sync; weak subjectivity | не объявлять одинаковую степень trust для разных способов sync |
| Peer scoring/diversity | libp2p Gossipsub v1.1 | per-peer limits, attack/failure tests и measurable overload behavior |
| Safe validator migration | EIP-3076, chain-specific consensus specs | single active signer, durable history, fenced failover |
| Crash/reorg drills | implementation patterns выше | fault-injection матрица и проверка consistency после восстановления |

**Правило доказательности:** спецификация определяет MUST/SHOULD для своей сети и версии; implementation docs показывают конкретный подход; таблицы, ADR и тесты в этом скилле — обобщённые инженерные рекомендации, которые нужно подтвердить на выбранном протоколе. Не приписывать одному проекту практики другого.
