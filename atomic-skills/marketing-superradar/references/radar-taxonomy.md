# Таксономия 13 радаров Маркетингового Суперрадара

Использовать радары как независимые генераторы сигналов. Один рынок может быть найден несколькими радарами; это повышает confidence, но не должно создавать двойной счёт.

## 1. Боли и жалобы пользователей

**Искать:** Reddit, форумы, reviews, communities, support threads, professional publications, GitHub issues, app-store reviews.

**Сильный сигнал:** повторяющаяся конкретная проблема с текущим workaround, потерей времени/денег или заметным frustration.

**Фиксировать:** persona, контекст, frequency, current workaround, willingness-to-pay proxies.

**Красный флаг:** жалоба громкая, но редкая; пользователь не является payer; проблема решается привычкой, а не покупкой.

**Поисковые формулировки:** "hate", "frustrating", "manual", "takes hours", "spreadsheet", "workaround", "why is there no", "expensive", "broken", "we still use".

## 2. Коммерциализация технологий 1–3 года

**Искать:** capital flows, late-stage funding, corporate pilots, production deployment, procurement, revenue, signed contracts, standards, regulation dates, infrastructure readiness, vendor marketing.

**Сильный сигнал:** технология переходит `demo → paid pilot → production → scale`, появляются бюджеты и dedicated buyers.

**Фиксировать:** maturity stage, production evidence, buyer, budget source, unit economics, bottleneck after deployment.

**Красный флаг:** только lab/demo/funding; нет платящего production use.

## 3. Денежные утечки

**Искать:** overpayments, billing errors, penalties, unclaimed reimbursements, unused licenses, discount leakage, chargebacks, missed credits, waste, failed collections.

**Сильный сигнал:** потеря измерима, повторяется, доказуема и допускает outcome pricing.

**Шаблон:** `найти потерю → доказать → определить допустимое исправление → выполнить → зафиксировать экономический результат`.

**Красный флаг:** recoverable amount слишком мал относительно cost of investigation.

## 4. Дорогой ручной труд

**Искать:** vacancies, BPO, repetitive professional workflows, Excel/email/copy-paste, document review, reconciliation, call-center ops.

**Сильный сигнал:** `high salary × repetition × structured/semi-structured inputs × verifiable output`.

**Фиксировать:** labor cost, volume, error rate, verification method, exception rate.

**Красный флаг:** задача требует уникального tacit judgment, а output нельзя быстро проверить.

## 5. Переходы между состояниями

Искать transitions:

- manual → automatic;
- human → AI;
- pilot → production;
- one → fleet;
- local → distributed;
- read-only → write/action;
- reversible → irreversible;
- unregulated → regulated;
- small → scale;
- recommendation → execution.

**Сильный сигнал:** старые controls перестают работать именно в момент перехода.

Особо искать момент, когда машина впервые получает право самостоятельно менять **дорогое, регулируемое, физическое или необратимое состояние**.

**Красный флаг:** переход описан концептуально, но не создаёт нового budget owner или контрольной точки.

## 6. Регуляторно создаваемые рынки

**Искать:** new law, delegated acts, reporting obligations, certification, audit, disclosure, traceability, record retention, enforcement dates.

**Сильный сигнал:** fixed deadline + identifiable obligated entity + recurring operational burden.

**Фиксировать:** exact date, affected population, duty, penalty/exposure, required evidence, incumbent compliance stack.

**Красный флаг:** обязанность однократная, легко закрывается консультантом или существует много готовых платформ.

## 7. Бюджетные сдвиги

**Искать:** new corporate budget lines, new executive roles, RFPs, headcount categories, dedicated procurement categories, large public commitments.

**Сильный сигнал:** `problem → dedicated budget → recurring procurement`.

**Фиксировать:** budget owner, spend proxy, new titles, RFP language, reallocated budget source.

**Красный флаг:** headline funding не означает customer budget.

## 8. Не-потребление

**Искать:** сегменты с проблемой, которые ничего не покупают, потому что existing solution слишком дорогой, complex или enterprise-only.

**Сильный сигнал:** AI/software способен снизить cost/complexity достаточно, чтобы новый сегмент начал потреблять.

**Фиксировать:** current alternative = do nothing / freelancer / spreadsheet / expert service; minimum viable willingness to pay.

**Красный флаг:** non-consumption вызван отсутствием ценности, а не ценой/сложностью.

## 9. Перекос цена/ценность

**Искать:** услуги/процессы, где software/AI снижает cost of result в 10–100×.

**Сильный сигнал:** удешевление меняет frequency of use, а не только margin.

Примеры логики:

- annual expert review → continuous monitoring;
- $20k consulting → $500 self-serve audit;
- quarterly analysis → per-transaction verification.

**Красный флаг:** после 10× удешевления customer всё равно не хочет результат.

## 10. Межотраслевой перенос

**Искать:** control pattern или workflow, ставший стандартом в отрасли A, но отсутствующий в B.

Типовые переносы:

- Git/CI-CD → documents / policies / robotics / AI agents;
- observability → compliance / physical operations;
- payment authorization → AI action authorization;
- SBOM → model/tool/configuration bill of materials;
- chain of custody → data/evidence workflows.

**Сильный сигнал:** underlying problem структурно аналогичен, а receiving industry уже имеет data infrastructure.

**Красный флаг:** различия regulation/physics/workflow делают аналогию поверхностной.

## 11. Инфраструктурные изменения

**Искать:** new primitives, protocols, APIs, platforms, identity rails, payment rails, sensors, robots, LLM tool-use, persistent agents, DPP registries.

Задавать три вопроса:

1. Что стало впервые технически возможным?
2. Что стало впервые экономически возможным?
3. Какое действие машина впервые получает право выполнять самостоятельно?

**Сильный сигнал:** новый primitive порождает вторичный control/data/distribution layer.

**Красный флаг:** инфраструктура существует, но нет production adoption.

## 12. Организационные изменения

**Искать:** new roles, changed accountability, agent workforce, remote/distributed operations, AI-native teams, machine-run organizations.

Задавать:

> Если изменение станет массовым, какую новую должность, ответственность или бюджет придётся создать?

**Сильный сигнал:** появление dedicated owner означает будущую закупку инструментов.

**Красный флаг:** организационный change модный, но headcount/budget ownership не меняется.

## 13. Расхождение «намеренное/утверждённое ↔ фактическое состояние»

Искать рынки, где существует дорогое, регулируемое или рискованное расхождение между тем, что **разрешено/заявлено/согласовано/обещано**, и тем, что реально существует.

### Базовые паттерны

- approved → published;
- authorized → executed;
- contract → actual vendor state;
- contract → invoice;
- policy → actual configuration;
- declared provenance → evidence;
- approved code → production code;
- approved ad/claim → externally visible ad/claim;
- safety-approved configuration → deployed configuration;
- intended workflow → actual outcome;
- AI intent → downstream consequence;
- recall/withdrawal → actual availability.

### Для каждого сигнала фиксировать

| Поле | Вопрос |
|---|---|
| Intended State | Что должно/разрешено/обещано быть истинным? |
| Actual State | Что реально наблюдается? |
| Reconciliation Trigger | Когда требуется сверка? |
| Cost of Drift | Что стоит расхождение? |
| Evidence Source | Чем доказать фактическое состояние? |
| Existing Control Point | Где контроль уже есть? |
| Buyer | Кто несёт экономический/правовой риск? |
| Shadow Mode | Можно ли начать без write-access? |

### Усилитель межсистемной границы

Повышать приоритет, если:

- A создаёт/утверждает intended state;
- B изменяет или распространяет объект;
- C несёт ответственность;
- A не контролирует B;
- фактическое состояние видно только после прохождения этой границы.

Это более сильный structural gap, чем сравнение двух таблиц внутри одной системы.

### Сильные типы продуктов

- independent monitoring;
- external-state observability;
- reconciliation layer;
- evidence receipt;
- release/change assurance;
- contract-as-policy monitor;
- continuous attestation.

### Красный флаг

Если incumbent уже владеет и intended state, и actual state, и может закрыть gap простым feature, резко понижать возможность.

# Перекрёстные сильные паттерны

Считать особенно сильным сигнал, когда совпадают 3+ радара:

- regulation + state drift + evidence;
- money leakage + verifiable result + success fee;
- pilot→production + new safety/control layer;
- AI write/action + irreversible state;
- new infrastructure primitive + new dedicated budget;
- non-consumption + 10–100× cost collapse;
- expensive manual labor + deterministic verification.

# Генерация поисковых гипотез

Для каждого радара строить запросы вокруг:

`[role/process] + [pain/trigger] + [evidence/money/deadline]`

Не искать только названия предполагаемых продуктов. Искать сам процесс:

- "how do teams verify...";
- "manual process";
- "audit errors";
- "new requirements 2026 2027";
- "production rollout";
- "renewal";
- "overpayment recovery";
- "incident reporting";
- "proof of";
- "continuous monitoring";
- "what happens after";
- "supplier evidence";
- "deployment safety";
- "actual vs approved";
- "still available after recall";
- "contractual requirement monitoring".
