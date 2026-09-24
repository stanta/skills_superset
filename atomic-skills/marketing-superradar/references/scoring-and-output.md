# Scoring, market sizing и adversarial-проверка

## 1. Evidence grades

Оценивать ключевые доказательства по качеству.

| Grade | Значение |
|---|---|
| A | официальный нормативный акт, audited/filing data, reproducible large-sample research, confirmed production/procurement |
| B | качественные observational data, несколько независимых credible sources |
| C | case study, small sample, один credible source |
| D | vendor marketing, anecdote, forum thread без corroboration |
| F | утверждение без evidence |

Не позволять одному A-сигналу автоматически компенсировать отсутствие payer или workflow.

## 2. Opportunity score

По умолчанию использовать 100-балльную модель.

| Критерий | Вес |
|---|---:|
| Боль / деньги / обязательность | 20 |
| Срочность / trigger / timing | 15 |
| Платёжеспособность и ясность buyer | 15 |
| Structural Competitive Gap | 15 |
| Доступность данных и проверяемость результата | 10 |
| Реалистичность MVP 8–12 недель | 10 |
| Размер достижимого рынка | 10 |
| Скорость роста / expansion option | 5 |

Ставить каждому критерию 0–10 и переводить в weighted score.

Не использовать score как замену reasoning. При близких баллах предпочитать идею с лучшим falsification path и более дешёвым paid pilot.

## 3. Competition score 0–10

Оценивать конкуренцию **для wedge v2**, а не широкой категории.

| Балл | Интерпретация |
|---:|---|
| 0–2 | почти нет прямых решений; substitutes слабые |
| 3–4 | несколько adjacent игроков; workflow mostly open |
| 5 | заметная конкуренция, но clear gap существует |
| 6 | несколько прямых стартапов/интеграторов |
| 7 | плотный рынок; wedge требует точного positioning |
| 8 | много прямых решений и крупные incumbents |
| 9 | почти commodity / feature parity |
| 10 | клин практически полностью закрыт |

При scoring учитывать:

- direct competitors;
- adjacent platform;
- service firms;
- internal build;
- incumbent feature roadmap;
- open-source;
- regulatory/industry standard that commoditizes the layer.

## 4. Competitive Gap

Оценивать по шести измерениям 0–10:

| Gap | Что проверять |
|---|---|
| Product | отсутствует ли нужная функция или object of control |
| Workflow | есть ли незакрытый handoff между ролями/системами |
| Distribution | есть ли более дешёвый route-to-market |
| Business Model | можно ли изменить risk/cashflow/pricing |
| Trust/Adoption | можно ли снизить permission/integration barrier |
| Transition | создаёт ли переход отдельный момент покупки |

### Structural vs feature gap

**Feature gap:** incumbent способен добавить функцию в существующий UI/API без изменения distribution, data rights или organizational ownership.

**Structural gap:** проблема возникает между независимыми systems/organizations/budgets/rights, поэтому одной функции недостаточно.

Повышать score structural gap.

## 5. Low-Cost Entry Vectors

Для каждого финалиста сформировать 3–5 вариантов.

### Product wedge

Узкая критичная функция для одного painful job.

### Workflow insertion

Overlay/sidecar/integration-first: вставиться между существующими systems без замены incumbent.

### Transition trigger

Продавать в момент renewal, audit, incident, migration, regulation deadline, pilot→production, first fleet, write access, scale-up.

### Distribution arbitrage

Использовать channel owner: MSP/MSSP, broker, accountant, insurer, consultant, systems integrator, marketplace partner, association, OEM, bank.

### Business-model arbitrage

- success fee;
- outcome pricing;
- savings share;
- free audit → paid recovery;
- concierge/service → software;
- pay-per-case;
- white-label;
- portfolio pricing вместо seats.

Допускать соседние стратегии: open-source beachhead, prosumer→enterprise, white-label/OEM, geography arbitrage, unbundling/rebundling, shadow-mode entry.

## 6. Adversarial re-check

Для **каждого** entry vector выполнить отдельный competitor pass.

Искать минимум:

1. exact phrase;
2. buyer + trigger;
3. input + output;
4. "platform/software/service for [workflow]";
5. incumbent documentation;
6. recent startup/funding/product launch;
7. consultancy/BPO substitute.

Проверять, совпадает ли:

- buyer;
- trigger;
- workflow;
- data;
- output;
- pricing;
- distribution.

Не считать конкурента прямым только из-за одинаковой category label.

### Decision

- ✅ **выжил** — прямого workflow match нет или structural gap остаётся.
- ⚠️ **сузить** — часть клина закрыта; указать новое отличие.
- ❌ **убить** — конкурент уже делает essentially same job.

## 7. Falsification и competing explanations

Для каждого финалиста сформулировать 3–5 ключевых claims.

Пример:

> «Brands готовы платить за external claim drift monitoring».

Для каждого claim записать:

- что его опровергнет;
- какой быстрый тест это проверит;
- качество текущего evidence;
- альтернативное объяснение сигнала.

Типовые competing explanations:

- проблема существует, но buyer считает её ответственностью другой стороны;
- regulatory deadline создаёт consulting spike, но не recurring SaaS;
- высокий labor cost компенсируется низкой frequency;
- funding/marketing создают illusion коммерциализации;
- новая category будет absorbed incumbent-ом;
- автоматизация технически возможна, но data access закрыт;
- новый продукт экономит деньги, но switching cost выше.

## 8. Pre-mortem финалиста

Представить, что через 12 месяцев стартап провалился. Найти 3 наиболее вероятных причины.

Предпочитать конкретные failure narratives:

- buyer не владеет budget;
- integration cost > ACV;
- event слишком редкий;
- evidence false-positive rate ломает trust;
- incumbent ships feature;
- data provider revokes access;
- regulation changes;
- sales cycle > runway.

Добавить early warning signal для каждой.

## 9. Market sizing

### TAM

Оценивать весь economic spend/value pool, связанный с job-to-be-done.

Использовать bottom-up, если возможно:

`# potential buyers × plausible annual spend`.

Не смешивать value created и software revenue без пояснения.

### SAM

Сузить TAM до:

- нужной географии;
- доступного ICP;
- конкретного wedge;
- доступных data/integrations;
- текущего regulatory/technology horizon.

### SAMconc

Использовать:

`SAMconc = SAM × (1 − C/10)`

где `C` — competition score 0–10.

Примеры:

- C=5 → SAMconc = 50% SAM;
- C=7 → SAMconc = 30% SAM;
- C=10 → 0.

Объяснять, что SAMconc — внутренний comparative heuristic, а не стандартный market metric.

### SOM 1y

Считать снизу вверх:

`reachable accounts × close rate × annual contract value`

или:

`cases × average recovered/saved value × take rate`.

Учитывать реальный sales cycle и channel.

## 10. Paid-pilot test

Для каждого сильного кандидата предпочитать тест до полноценной разработки.

Примеры:

- €3–10k audit;
- success-fee recovery;
- 2-недельный shadow monitoring;
- manual evidence pack;
- concierge workflow;
- white-label pilot у одного channel partner.

Сильный signal — оплата или доступ к чувствительным данным/процессу, а не только «интересно».

## 11. Kill criteria

Kill criteria должны быть измеримыми.

Слабое:
- «если клиентам не понравится».

Сильное:
- «из 15 интервью менее 3 buyers признают ownership проблемы»;
- «drift встречается <2% объектов и median loss <€500»;
- «3 крупнейших incumbents уже предлагают exact workflow»;
- «для 80% cases нет доступного evidence source»;
- «paid audit не удаётся продать даже за €3k»;
- «integration требует >6 недель на клиента при ACV <€20k».

## 12. Формат Weekly Full Scan

### Top-10

| # | Возможность | Радары | Trigger | SAM | Конк. | SAMconc | MVP | Score |
|---|---|---|---|---:|---:|---:|---:|---:|

После таблицы кратко объяснить новые рыночные сигналы недели.

### Deep Top-3

Для каждого:

1. Почему сейчас.
2. Buyer / budget / money event.
3. TAM.
4. Конкуренты и substitutes.
5. Competitive Gap ×6.
6. 3–5 entry vectors.
7. Adversarial re-check каждого.
8. Wedge v2.
9. SAM / competition / SAMconc.
10. SOM 1y.
11. MVP.
12. Risks / pre-mortem.
13. 7-day tests.
14. Kill criteria.

### Финал

Выдать:

1. победителя недели;
2. почему он;
3. лучший low-cost entry vector;
4. что проверить за 7 дней;
5. kill criteria;
6. идеи, которые убиты и почему;
7. отдельный блок радара №13.

## 13. Формат Second Echelon 11–20

Не трактовать 11–20 как «плохие идеи». Для каждой указать **главный дефект, не позволивший войти в top-10**.

Таблица:

| # | Возможность | Главный радар | SAM | Конк. | SAMconc | MVP | Главный дефект |
|---|---|---|---:|---:|---:|---:|---|

Затем для каждой идеи дать компактно:

- signal;
- structural gap;
- direct competitors/substitutes;
- surviving wedge v2;
- почему не top-10;
- kill criterion.

В конце выделить 2–3 идеи, которые могут подняться в top-10 при одном конкретном подтверждении.

## 14. Confidence

Маркировать вывод:

- **Высокая уверенность** — несколько независимых A/B sources + ясный buyer/trigger.
- **Средняя** — хорошая логика, но один ключевой assumption не подтверждён.
- **Низкая** — market hypothesis требует первичных интервью/данных.

Не маскировать uncertainty точными десятичными оценками.
