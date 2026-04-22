# Антипаттерны на Уровне Кода: Фронтэнд, Бэкэнд, Базы Данных, Тестирование и DevOps

---

## Содержание

1. [Введение и Область Исследования](#1-введение-и-область-исследования)
2. [Стратегический План Исследования](#2-стратегический-план-исследования)
3. [Антипаттерны Фронтэнда](#3-антипаттерны-фронтэнда)
4. [Антипаттерны Бэкэнда](#4-антипаттерны-бэкэнда)
5. [Антипаттерны Баз Данных](#5-антипаттерны-баз-данных)
6. [Антипаттерны Тестирования](#6-антипаттерны-тестирования)
7. [Антипаттерны DevOps и CI/CD](#7-антипаттерны-devops-и-cicd)
8. [Синтез: Перекрёстные Паттерны и Корреляции](#8-синтез-перекрёстные-паттерны-и-корреляции)
9. [Критический Обзор и Ограничения](#9-критический-обзор-и-ограничения)
10. [Направления Будущих Исследований](#10-направления-будущих-исследований)
11. [Заключение](#11-заключение)
12. [Список Источников](#12-список-источников)

---

## 1. Введение и Область Исследования

### 1.1. Определения

**Антипаттерн на уровне кода** — это повторяющаяся ошибка в реализации, которая проявляется в конкретных конструкциях, структурах или практиках разработки, приводя к снижению производительности, поддерживаемости, надёжности или безопасности системы.

В отличие от архитектурных антипаттернов (которые описывают структурные дефекты на уровне системы), кодовые антипаттерны проявляются на уровне отдельных модулей, функций, запросов, компонентов или конфигураций.

### 1.2. Область Исследования

Данный отчёт охватывает пять доменов:

| Домен            | Описание                                    | Примеры антипаттернов                                              |
| ---------------- | ------------------------------------------- | ------------------------------------------------------------------ |
| **Фронтэнд**     | Клиентский код: JavaScript, React, Vue, CSS | Props Drilling, Inline Styles, Missing Keys                        |
| **Бэкэнд**       | Серверный код: Node.js, Python, Java, API   | Callback Hell, Unhandled Rejections, Missing Validation            |
| **Базы Данных**  | SQL-запросы, схемы, индексы                 | N+1 Problem, SELECT \*, EAV Pattern, Index Shotgun                 |
| **Тестирование** | Unit, интеграционные, E2E тесты             | Flaky Tests, Test Coupling, Over-Mocking                           |
| **DevOps/CI/CD** | Пайплайны, инфраструктура, деплой           | Manual Steps in Pipeline, Infrequent Commits, No Rollback Strategy |

### 1.3. Ограничения

- **Временные рамки**: Источники 2010–2026 гг.
- **Язык**: Источники на английском; отчёт на русском.
- **Тип данных**: Качественный анализ с эмпирическими примерами.

---

## 2. Стратегический План Исследования

### 2.1. Декомпозиция

| #   | Подгипотеза                                                                     | Методология                                             |
| --- | ------------------------------------------------------------------------------- | ------------------------------------------------------- |
| H1  | Фронтэнд антипаттерны влияют на производительность рендеринга и UX              | Анализ React/JS-специфичных источников                  |
| H2  | Бэкэнд антипаттерны приводят к ошибкам обработки, уязвимостям и деградации API  | Анализ Node.js, Python, API-design источников           |
| H3  | Антипаттерны БД — основная причина медленных запросов и проблем масштабирования | Анализ SQL-антипаттернов (Karwin, DataCamp, Levitation) |
| H4  | Антипаттерны тестирования снижают доверие к CI и замедляют доставку             | Анализ flaky tests, test automation источников          |
| H5  | DevOps антипаттерны создают ручные шаги, увеличивают MTTR и снижают надёжность  | Анализ CI/CD, AWS Well-Architected, DZone источников    |

### 2.2. Источники

- **Фронтэнд**: ITNEXT, Medium, Caktus Group, DEV Community, Packt Books
- **Бэкэнд**: GitHub (goldbergyoni/nodebestpractices), AppSignal, Specmatic, PlexObject
- **Базы Данных**: Bill Karwin "SQL Antipatterns", DataCamp, Levitation, TXMinds
- **Тестирование**: Codepipes, TestDevLab, AWS Well-Architected
- **DevOps**: EM360Tech, DZone Refcards, Red-Gate Simple Talk, ContinuousDelivery.com

---

## 3. Антипаттерны Фронтэнда

### 3.1. Props Drilling

**Определение**: Передача данных через множество уровней компонентов без использования контекста или state management [Source: Caktus Group, 2023](https://www.caktusgroup.com/blog/2023/02/02/3-react-anti-patterns-and-how-fix-them/).

**Симптомы**:

- Компонент получает 5+ props, которые просто передаются дальше
- Промежуточные компоненты не используют данные, но объявляют их в сигнатуре
- Изменение структуры props требует правки 10+ файлов

**Влияние**: Снижение поддерживаемости, увеличение coupling между компонентами.

**Решение**: React Context, Zustand, Redux, или композиция компонентов.

**Уровень уверенности**: **Высокий**

### 3.2. Array Index as Key

**Определение**: Использование индекса массива в качестве `key` prop для списков [Source: Caktus Group, 2023](https://www.caktusgroup.com/blog/2023/02/02/3-react-anti-patterns-and-how-fix-them/); [Source: ITNEXT, 2024](https://itnext.io/6-common-react-anti-patterns-that-are-hurting-your-code-quality-904b9c32e933).

**Симптомы**:

- `items.map((item, index) => <Item key={index} />)`
- Неправильное состояние при сортировке/фильтрации списка
- Потеря фокуса ввода при ре-рендере

**Влияние**: Ошибки рендеринга, потеря состояния компонентов, деградация производительности.

**Решение**: Использовать уникальные идентификаторы (`item.id`).

**Уровень уверенности**: **Высокий**

### 3.3. Inline Styles и CSS-in-JS Overuse

**Определение**: Чрезмерное использование inline-стилей или создание стилей внутри render-функции.

**Симптомы**:

- `style={{ color: 'red', margin: '10px' }}` повсеместно
- Создание styled-компонентов внутри других компонентов
- Отсутствие дизайн-системы или токенов

**Влияние**: Каждый ре-рендер создаёт новые объекты стилей, блокируется браузерная оптимизация.

**Решение**: CSS Modules, Tailwind, или вынесенные styled-компоненты.

**Уровень уверенности**: **Средний** — зависит от масштаба приложения.

### 3.4. useEffect Overuse (Side Effects Everywhere)

**Определение**: Использование `useEffect` для синхронизации состояния вместо вычисляемых значений или event handlers [Source: ITNEXT, 2024](https://itnext.io/6-common-react-anti-patterns-that-are-hurting-your-code-quality-904b9c32e933).

**Симптомы**:

- `useEffect` для обновления state на основе другого state
- Цепочки `useEffect` → `setState` → `useEffect`
- Бесконечные циклы ре-рендеров

**Влияние**: Непредсказуемое поведение, сложность отладки, лишние рендеры.

**Решение**: Вычисляемые значения (`const total = items.reduce(...)`), event handlers, `useMemo`.

**Уровень уверенности**: **Высокий**

### 3.5. Missing Memoization

**Определение**: Отсутствие `useMemo`, `useCallback`, `React.memo` при тяжёлых вычислениях или передаче функций/объектов в props.

**Симптомы**:

- Тяжёлые вычисления на каждом рендере
- Новые объекты/функции в props дочерних компонентов
- Ре-рендер всего дерева при изменении одного узла

**Влияние**: Деградация производительности, особенно при больших списках.

**Решение**: Профилирование с React DevTools, применение memoization по необходимости.

**Уровень уверенности**: **Высокий**

### 3.6. Div Soup

**Определение**: Избыточная вложенность `<div>` без семантики [Source: Caktus Group, 2023](https://www.caktusgroup.com/blog/2023/02/02/3-react-anti-patterns-and-how-fix-them/).

**Симптомы**:

- `<div><div><div><div>...</div></div></div></div>`
- Отсутствие семантических тегов (`<section>`, `<article>`, `<nav>`)
- Сложность навигации в DevTools

**Влияние**: Проблемы доступности (a11y), сложность поддержки, SEO-штрафы.

**Решение**: Семантическая разметка, CSS Grid/Flexbox для layout.

**Уровень уверенности**: **Средний**

---

## 4. Антипаттерны Бэкэнда

### 4.1. Callback Hell (Pyramid of Doom)

**Определение**: Глубокая вложенность callback-функций в Node.js [Source: Medium, 2024](https://sunilrana123.medium.com/nodejs-anti-patterns-b23201304833); [Source: AppSignal, 2022](https://blog.appsignal.com/2022/02/23/patterns-and-anti-patterns-in-nodejs.html).

**Симптомы**:

```javascript
fs.readFile("a.txt", (err, data) => {
  fs.readFile("b.txt", (err2, data2) => {
    fs.readFile("c.txt", (err3, data3) => {
      // ...
    });
  });
});
```

**Влияние**: Нечитаемый код, сложность обработки ошибок, stack trace проблемы.

**Решение**: Async/await, Promise chaining, модульная декомпозиция.

**Уровень уверенности**: **Высокий**

### 4.2. Unhandled Promise Rejections

**Определение**: Отсутствие `.catch()` или `try/catch` вокруг async операций [Source: GitHub (goldbergyoni), 2024](https://github.com/goldbergyoni/nodebestpractices).

**Симптомы**:

- `process.on('unhandledRejection')` ловит ошибки в production
- Тихие падения без логирования
- Процесс завершается без предупреждения (Node.js 15+)

**Влияние**: Потеря данных, непредсказуемое поведение, downtime.

**Решение**: Глобальные обработчики, async middleware с try/catch, ESLint правила.

**Уровень уверенности**: **Высокий**

### 4.3. Missing Input Validation

**Определение**: Отсутствие валидации входных данных на сервере [Source: Specmatic, 2024](https://specmatic.io/appearance/how-to-identify-avoid-api-design-anti-patterns/); [Source: PlexObject, 2024](https://weblog.plexobject.com/archives/7439).

**Симптомы**:

- `req.body.email` используется без проверки
- Отсутствие Joi/Zod/express-openapi-validator
- SQL injection, XSS через непроверенные данные

**Влияние**: Уязвимости безопасности, corrupted data, crashes.

**Решение**: Schema validation на границе API (Zod, Joi, OpenAPI middleware).

**Уровень уверенности**: **Высокий**

### 4.4. God Controller / Fat Controller

**Определение**: Контроллер/роут-обработчик содержит бизнес-логику, валидацию, маппинг и обработку ошибок.

**Симптомы**:

- Файл контроллера > 500 строк
- Смешение HTTP-логики с бизнес-правилами
- Дублирование кода между контроллерами

**Влияние**: Сложность тестирования, нарушение SRP, дублирование.

**Решение**: Service layer, middleware decomposition, use cases (Clean Architecture).

**Уровень уверенности**: **Высокий**

### 4.5. API Chatty Interface

**Определение**: API требует множества последовательных вызовов для выполнения одной бизнес-операции [Source: The New Stack, 2024](https://thenewstack.io/the-5-worst-anti-patterns-in-api-management/).

**Симптомы**:

- GET /user → GET /user/orders → GET /order/1/items → GET /item/1/details
- Отсутствие batch endpoints или aggregation
- Клиент выполняет 10+ запросов для одной страницы

**Влияние**: Высокая латентность, network overhead, poor UX.

**Решение**: GraphQL, BFF (Backend for Frontend), batch endpoints, aggregation layer.

**Уровень уверенности**: **Высокий**

### 4.6. Error Swallowing

**Определение**: Пустые catch-блоки или `console.error` без дальнейшей обработки.

**Симптомы**:

```javascript
try {
  await saveOrder(order);
} catch (e) {
  // ничего
}
```

**Влияние**: Тихие failures, потеря данных, сложность диагностики.

**Решение**: Structured logging, error classification, retry policies, user-facing error messages.

**Уровень уверенности**: **Высокий**

---

## 5. Антипаттерны Баз Данных

### 5.1. N+1 Query Problem

**Определение**: Выполнение N дополнительных запросов в цикле вместо одного JOIN или batch-запроса [Source: TXMinds, 2024](https://www.txminds.com/blog/sql-query-optimization-techniques/); [Source: Codepipes](https://blog.codepipes.com/testing/software-testing-antipatterns.html).

**Симптомы**:

```python
for user in users:
    orders = Order.objects.filter(user=user)  # N запросов!
```

**Влияние**: Экспоненциальная деградация производительности при росте данных.

**Решение**: `prefetch_related`/`select_related` (Django), `JOIN`, DataLoader (GraphQL), batch queries.

**Уровень уверенности**: **Высокий**

### 5.2. SELECT \*

**Определение**: Выборка всех колонок вместо необходимых.

**Симптомы**:

- `SELECT * FROM users`
- Передача лишних данных по сети
- Зависимость от порядка колонок

**Влияние**: Network overhead, index coverage loss, breaking changes при ALTER TABLE.

**Решение**: Явное указание колонок, ORM с lazy loading.

**Уровень уверенности**: **Высокий**

### 5.3. EAV (Entity-Attribute-Value) Pattern

**Определение**: Хранение гибких данных в виде трёх таблиц: сущность, атрибут, значение [Source: Levitation, 2024](https://levitation.in/posts/anti-patterns-in-database-design-lessons-from-real-world-failures).

**Симптомы**:

- Таблица `attributes` с колонками `entity_id`, `key`, `value`
- Запросы с множеством JOIN и PIVOT
- Потеря типизации и constraints

**Влияние**: Невозможность эффективных индексов, медленные запросы, сложность миграции.

**Решение**: JSONB (PostgreSQL), document stores, или нормализованная схема с миграциями.

**Уровень уверенности**: **Высокий**

### 5.4. Index Shotgun

**Определение**: Создание индексов на каждой колонке без анализа query plans [Source: Stack Overflow, 2024](https://stackoverflow.com/questions/351615/best-practices-and-anti-patterns-in-creating-indexes-in-sql-server).

**Симптомы**:

- Индексы на всех колонках «на всякий случай»
- Медленные INSERT/UPDATE из-за перестроения индексов
- Оптимизатор выбирает wrong index

**Влияние**: Замедление записи, wasted storage, suboptimal query plans.

**Решение**: EXPLAIN ANALYZE, покрытие индексами только нужных запросов, мониторинг unused indexes.

**Уровень уверенности**: **Высокий**

### 5.5. Fear of the Unknown (No EXPLAIN)

**Определение**: Написание запросов без анализа execution plan [Source: Karwin, SQL Antipatterns](https://www.amazon.com/SQL-Antipatterns-Programming-Pragmatic-Programmers/dp/1934356557).

**Симптомы**:

- Запросы пишутся «наугад»
- Full table scan на таблицах с миллионами строк
- Отсутствие покрытия индексами

**Влияние**: Непредсказуемая производительность, production incidents.

**Решение**: Обязательный EXPLAIN для новых запросов, query review в PR.

**Уровень уверенности**: **Высокий**

### 5.6. Spaghetti Query

**Определение**: Один запрос выполняет слишком много операций: JOIN, подзапросы, агрегации, CASE.

**Симптомы**:

- Запрос > 100 строк
- 10+ JOIN в одном запросе
- Невозможность понять логику без документации

**Влияние**: Сложность оптимизации, хрупкость, сложность рефакторинга.

**Решение**: Декомпозиция на CTE, временные таблицы, или бизнес-логику в коде.

**Уровень уверенности**: **Средний** — иногда сложные запросы оправданы.

---

## 6. Антипаттерны Тестирования

### 6.1. Flaky Tests

**Определение**: Тесты, которые проходят/падают без изменений в коде [Source: Codepipes](https://blog.codepipes.com/testing/software-testing-antipatterns.html); [Source: TestDevLab](https://www.testdevlab.com/blog/5-test-automation-anti-patterns-and-how-to-avoid-them).

**Симптомы**:

- Тест падает 1 из 10 запусков
- Зависимость от таймингов, порядка выполнения, внешних сервисов
- `retry: 3` в CI конфигурации

**Влияние**: Потеря доверия к CI, игнорирование реальных failures, wasted developer time.

**Решение**: Детерминизм, моки внешних зависимостей, фиксированные seed, explicit waits.

**Уровень уверенности**: **Высокий**

### 6.2. Test Coupling

**Определение**: Тесты зависят от порядка выполнения или общего состояния.

**Симптомы**:

- Тест B проходит только после теста A
- Общий mutable state между тестами
- Зависимость от данных, созданных другими тестами

**Влияние**: Невозможность параллельного запуска, случайные failures.

**Решение**: Isolation, beforeEach/afterEach hooks, transactional rollback.

**Уровень уверенности**: **Высокий**

### 6.3. Over-Mocking

**Определение**: Мокирование всего, включая собственные модули.

**Симптомы**:

- Тест мокирует 80% кода
- Тест проверяет вызовы моков, а не поведение
- Зелёные тесты, но сломанный production

**Влияние**: Ложное чувство безопасности, тесты не ловят реальные баги.

**Решение**: Тестировать поведение, а не реализацию; интеграционные тесты для критичных путей.

**Уровень уверенности**: **Высокий**

### 6.4. Testing Implementation, Not Behavior

**Определение**: Тесты проверяют внутренние детали реализации, а не наблюдаемое поведение.

**Симптомы**:

- Тесты ломаются при рефакторинге без изменения функциональности
- Проверка приватных методов
- Assert на internal state

**Влияние**: Сопротивление рефакторингу, wasted effort на поддержку тестов.

**Решение**: TDD, тестирование через public API, behavior-driven assertions.

**Уровень уверенности**: **Высокий**

---

## 7. Антипаттерны DevOps и CI/CD

### 7.1. Manual Steps in Pipeline

**Определение**: Ручные шаги в процессе деплоя [Source: Red-Gate Simple Talk, 2024](https://www.red-gate.com/simple-talk/devops/devops-anti-patterns-what-they-are-and-how-to-avoid-them/); [Source: AWS Well-Architected](https://docs.aws.amazon.com/wellarchitected/latest/devops-guidance/anti-patterns-for-continuous-integration.html).

**Симптомы**:

- «Запусти скрипт deploy.sh после тестов»
- Ручная правка конфигов на сервере
- Деплой только у одного «деплой-мастера»

**Влияние**: Невоспроизводимость, bus factor = 1, human errors.

**Решение**: Полная автоматизация, IaC, self-service деплой.

**Уровень уверенности**: **Высокий**

### 7.2. Infrequent Commits

**Определение**: Редкие коммиты (раз в день/неделю) [Source: AWS Well-Architected](https://docs.aws.amazon.com/wellarchitected/latest/devops-guidance/anti-patterns-for-continuous-integration.html).

**Симптомы**:

- Long-lived feature branches
- Merge conflicts при каждом слиянии
- CI запускается раз в день

**Влияние**: Длинные feedback loops, integration hell, risk при деплое.

**Решение**: Trunk-based development, feature flags, мелкие коммиты.

**Уровень уверенности**: **Высокий**

### 7.3. No Rollback Strategy

**Определение**: Отсутствие автоматизированного отката при failed деплое [Source: DZone Refcards, 2024](https://dzone.com/refcardz/continuous-delivery-patterns).

**Симптомы**:

- «Если что-то сломается, будем чинить»
- Отсутствие blue-green/canary деплоя
- Ручной rollback через git revert

**Влияние**: Extended downtime, manual recovery, customer impact.

**Решение**: Blue-green, canary, automated rollback on health check failure.

**Уровень уверенности**: **Высокий**

### 7.4. Pipeline Without Observability

**Определение**: CI/CD пайплайн без мониторинга, логов и метрик [Source: EM360Tech, 2024](https://em360tech.com/tech-articles/cicd-anti-patterns-whats-slowing-down-your-pipeline/).

**Симптомы**:

- «Пайплайн упал, но мы не знаем почему»
- Отсутствие MTTR tracking
- Нет flaky test detection

**Влияние**: Blind spots, extended debugging time, degraded trust.

**Решение**: Pipeline logging, duration metrics, failure analytics, alerting.

**Уровень уверенности**: **Высокий**

### 7.5. Big Bang Release

**Определение**: Редкие, крупные релизы с множеством изменений.

**Симптомы**:

- Релиз раз в квартал
- 100+ фич в одном релизе
- «Code freeze» за неделю до релиза

**Влияние**: High risk, difficult rollback, customer dissatisfaction.

**Решение**: Continuous delivery, feature flags, small batch sizes.

**Уровень уверенности**: **Высокий**

---

## 8. Синтез: Перекрёстные Паттерны и Корреляции

### 8.1. Мета-паттерны

Анализ выявил несколько мета-паттернов, которые проявляются across domains:

| Мета-паттерн                | Фронтэнд         | Бэкэнд           | БД              | Тесты         | DevOps             |
| --------------------------- | ---------------- | ---------------- | --------------- | ------------- | ------------------ |
| **Over-coupling**           | Props Drilling   | God Controller   | Shared DB       | Test Coupling | Manual Steps       |
| **Lack of Boundaries**      | Div Soup         | Fat Controller   | EAV             | Over-Mocking  | No Rollback        |
| **Missing Automation**      | Manual State     | No Validation    | No EXPLAIN      | Flaky Tests   | Manual Deploy      |
| **Premature Optimization**  | Over-Memoization | Over-Engineering | Index Shotgun   | Over-Testing  | Over-Orchestration |
| **Fear-Driven Development** | Div Soup (safe)  | Error Swallowing | Fear of Unknown | No Tests      | Big Bang Release   |

### 8.2. Корреляции

1. **Props Drilling ↔ God Controller ↔ Shared DB**: Все три антипаттерна являются проявлениями **отсутствия границ ответственности**. Решение в каждом случае — разделение по bounded contexts.

2. **Flaky Tests ↔ Manual Deploy ↔ Infrequent Commits**: Все три создают **непредсказуемость** в процессе доставки. Решение — детерминизм и автоматизация.

3. **N+1 Query ↔ API Chatty Interface ↔ useEffect Overuse**: Все три создают **избыточные операции** (запросы, вызовы, рендеры). Решение — batch/aggregation.

4. **Index Shotgun ↔ Over-Mocking ↔ Over-Memoization**: Все три — **premature optimization**, когда решение применяется без понимания проблемы.

### 8.3. Корневые Причины Across Domains

| Причина                      | Проявления                                                |
| ---------------------------- | --------------------------------------------------------- |
| **Давление сроков**          | Props Drilling, Error Swallowing, No Tests, Manual Deploy |
| **Недостаточная экспертиза** | Callback Hell, EAV, Over-Mocking, Index Shotgun           |
| **Отсутствие стандартов**    | Div Soup, God Controller, Spaghetti Query, Flaky Tests    |
| **Страх изменений**          | Lava Flow (архитектура), Fear of EXPLAIN, No Rollback     |

---

## 9. Критический Обзор и Ограничения

### 9.1. Самокритика

- **Фронтэнд bias**: Большинство источников по фронтэнду посвящены React; антипаттерны Vue/Angular/Svelte менее покрыты.
- **Бэкэнд bias**: Node.js доминирует в источниках; Java/Python/Go антипаттерны менее детализированы.
- **Отсутствие количественных данных**: Большинство описаний качественные; метрики влияния (ms, CPU, memory) ограничены.
- **Контекстуальность**: Некоторые «антипаттерны» могут быть оправданы в определённых контекстах (например, SELECT \* для админ-панелей).

### 9.2. Проверка Надёжности

**Что могло бы фальсифицировать результаты?**

1. **Бенчмарки**: Если бы бенчмарки показали, что N+1 query не влияет на производительность при малых данных, это ограничило бы H3.
2. **A/B тесты**: Если бы A/B тесты показали, что flaky tests не влияют на velocity команд, это ослабило бы H4.
3. **Survey**: Если бы опрос 1000+ разработчиков показал, что большинство не сталкивается с описанными антипаттернами, это потребовало бы пересмотра таксономии.

### 9.3. Конфликтующие Данные

- **Premature Optimization**: Некоторые «антипаттерны» (например, Index Shotgun) могут быть следствием legitimate попытки оптимизации, а не ignorance.
- **Context Matters**: SELECT \* может быть оправдан для ETL-пайплайнов; Over-Mocking — для unit-тестирования legacy кода.

---

## 10. Направления Будущих Исследований

### 10.1. Эмпирическое Исследование Влияния Антипаттернов на Производительность

**Описание**: Бенчмарк-исследование количественного влияния каждого антипаттерна на latency, CPU, memory, и developer velocity.

**Методология**:

- Создание контрольных приложений с и без антипаттернов
- Нагрузочное тестирование (k6, Artillery)
- Измерение developer time на понимание/изменение кода

### 10.2. Автоматизированное Обнаружение Кодовых Антипаттернов

**Описание**: Разработка ESLint/SonarQube правил для автоматического обнаружения описанных антипаттернов.

**Методология**:

- AST-анализ для React антипаттернов
- Static analysis для N+1 query detection
- CI integration для flaky test detection

### 10.3. Cross-Domain Anti-Pattern Correlation Study

**Описание**: Исследование корреляций между антипаттернами разных доменов (например, связаны ли фронтэнд антипаттерны с бэкэнд антипаттернами в одних и тех же командах).

**Методология**:

- Анализ 100+ open-source репозиториев
- Статистический анализ корреляций
- Case studies команд с высоким/низким качеством кода

---

## 11. Заключение

Исследование выявило **25+ кодовых антипаттернов** в пяти доменах разработки. Ключевые выводы:

1. **Фронтэнд**: Props Drilling, Array Index as Key, useEffect Overuse, Missing Memoization — наиболее распространённые React-антипаттерны с прямым влиянием на производительность.
2. **Бэкэнд**: Callback Hell, Unhandled Rejections, Missing Validation, God Controller — критичные для безопасности и надёжности.
3. **Базы Данных**: N+1 Query, EAV, Index Shotgun, Fear of EXPLAIN — основные причины деградации производительности.
4. **Тестирование**: Flaky Tests, Test Coupling, Over-Mocking — снижают доверие к CI и замедляют доставку.
5. **DevOps**: Manual Steps, Infrequent Commits, No Rollback — создают operational risk и увеличивают MTTR.

**Мета-вывод**: Большинство антипаттернов сводятся к четырём корневым причинам: давление сроков, недостаточная экспертиза, отсутствие стандартов и страх изменений.

---

## 12. Список Источников

| #   | Источник                                                         | URL                                                                                                                     |
| --- | ---------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| 1   | ITNEXT (2024). 6 Common React Anti-Patterns                      | [ITNEXT](https://itnext.io/6-common-react-anti-patterns-that-are-hurting-your-code-quality-904b9c32e933)                |
| 2   | Caktus Group (2023). 3 React Anti-Patterns and How to Fix Them   | [Caktus Group](https://www.caktusgroup.com/blog/2023/02/02/3-react-anti-patterns-and-how-fix-them/)                     |
| 3   | DEV Community (2024). React Performance Anti-Patterns            | [DEV](https://dev.to/myogeshchavan97/react-performance-anti-patterns-5-mistakes-that-kill-your-apps-speed-76j)          |
| 4   | Medium (2024). Node.js Anti-Patterns                             | [Medium](https://sunilrana123.medium.com/nodejs-anti-patterns-b23201304833)                                             |
| 5   | AppSignal (2022). Patterns and Anti-Patterns in Node.js          | [AppSignal](https://blog.appsignal.com/2022/02/23/patterns-and-anti-patterns-in-nodejs.html)                            |
| 6   | GitHub (2024). Node.js Best Practices                            | [goldbergyoni/nodebestpractices](https://github.com/goldbergyoni/nodebestpractices)                                     |
| 7   | The New Stack (2024). 5 Worst Anti-Patterns in API Management    | [The New Stack](https://thenewstack.io/the-5-worst-anti-patterns-in-api-management/)                                    |
| 8   | Specmatic (2024). API Design Anti-patterns                       | [Specmatic](https://specmatic.io/appearance/how-to-identify-avoid-api-design-anti-patterns/)                            |
| 9   | PlexObject (2024). API Anti-Patterns: 50+ Mistakes               | [PlexObject](https://weblog.plexobject.com/archives/7439)                                                               |
| 10  | DataCamp (2024). SQL Query Optimization: 15 Techniques           | [DataCamp](https://www.datacamp.com/blog/sql-query-optimization)                                                        |
| 11  | Levitation (2024). Anti-Patterns in Database Design              | [Levitation](https://levitation.in/posts/anti-patterns-in-database-design-lessons-from-real-world-failures)             |
| 12  | Karwin, B. SQL Antipatterns                                      | [Pragmatic Programmers](https://pragprog.com/titles/bksap1/sql-antipatterns-volume-1/)                                  |
| 13  | TXMinds (2024). High-Performance SQL: 12 Proven Techniques       | [TXMinds](https://www.txminds.com/blog/sql-query-optimization-techniques/)                                              |
| 14  | Codepipes. Software Testing Anti-Patterns                        | [Codepipes](https://blog.codepipes.com/testing/software-testing-antipatterns.html)                                      |
| 15  | TestDevLab (2024). Avoiding Test Automation Pitfalls             | [TestDevLab](https://www.testdevlab.com/blog/5-test-automation-anti-patterns-and-how-to-avoid-them)                     |
| 16  | AWS Well-Architected. Anti-Patterns for Continuous Integration   | [AWS](https://docs.aws.amazon.com/wellarchitected/latest/devops-guidance/anti-patterns-for-continuous-integration.html) |
| 17  | EM360Tech (2024). CI/CD Anti-Patterns                            | [EM360Tech](https://em360tech.com/tech-articles/cicd-anti-patterns-whats-slowing-down-your-pipeline/)                   |
| 18  | DZone Refcards. Continuous Delivery Patterns and Anti-Patterns   | [DZone](https://dzone.com/refcardz/continuous-delivery-patterns)                                                        |
| 19  | Red-Gate Simple Talk (2024). DevOps Anti-Patterns                | [Red-Gate](https://www.red-gate.com/simple-talk/devops/devops-anti-patterns-what-they-are-and-how-to-avoid-them/)       |
| 20  | ContinuousDelivery.com (2010). Deployment Pipeline Anti-Patterns | [ContinuousDelivery](https://continuousdelivery.com/2010/09/deployment-pipeline-anti-patterns/)                         |

---

_Отчёт подготовлен: 22 апреля 2026 г._
_Методология: Deep Research Protocol v2.0 — 5-фазный процесс (Calibration → Planning → Evidence Acquisition → Synthesis → Critical Review)_
