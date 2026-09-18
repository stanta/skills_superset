# Sources — 1С:Предприятие extension-development skill

Актуализировано: 2026-09-18.

## Source priority

При конфликте источников используй приоритет:

1. официальная документация платформы 1С:Предприятие / 1С:ИТС;
2. официальная Система стандартов и методик разработки конфигураций;
3. официальная документация 1C:EDT;
4. официальные материалы БСП;
5. проверенные open-source инструменты 1С-сообщества — только как tooling recommendation, не как определение семантики платформы.

## Official 1C sources

1. **Расширения — платформа 1С:Предприятие**  
   https://v8.1c.ru/platforma/rasshireniya/  
   Основание для extension-first, заимствованных объектов и автоматической проверки применимости.

2. **Расширения конфигураций. Как адаптировать прикладные решения при внедрении**  
   https://its.1c.ru/db/pubextensions  
   Префикс, назначение, область действия, формы, модули, `&Перед`, `&После`, `&Вместо`, взаимодействие расширений, safe mode.

3. **Проект расширения конфигурации — 1C:EDT**  
   https://its.1c.ru/db/content/edtdoc/src/topics/t000538.html  
   Один extension project = одно расширение, базовый проект конфигурации.

4. **1C:EDT — официальный сайт**  
   https://edt.1c.ru/  
   Текущий релиз и release candidate.

5. **1C:EDT 2026.1**  
   https://edt.1c.ru/docs/new/versiya-2026-1/  
   Stable-line изменения, поддержка платформ и проверки «1С:Стандарты разработки V8».

6. **1C:EDT 2026.2 RC**  
   https://edt.1c.ru/blog/vyshel-reliz-kandidat-1c-edt-2026-2-0/  
   RC, минимальные требования к 8.3.27, Java/Eclipse baseline.

7. **Общие требования к конфигурации — стандарт 467**  
   https://its.1c.ru/db/content/v8std/src/200/100/i8100467.htm

8. **Стандартные роли — стандарт 488**  
   https://its.1c.ru/db/content/v8std/src/700/i8100488.htm  
   Включает отдельные требования к ролям расширений.

9. **Настройка ролей и прав доступа — стандарт 689**  
   https://its.1c.ru/db/content/v8std/src/700/i8100689.htm

10. **Проверка прав доступа — стандарт 737**  
    https://its.1c.ru/db/content/v8std/src/700/i8100737.htm  
    `ПравоДоступа` vs `РольДоступна`.

11. **Безопасность прикладного программного интерфейса сервера — стандарт 678**  
    https://its.1c.ru/db/content/v8std/src/600/i8100678.htm

12. **Ограничение на выполнение внешнего кода — стандарт 669**  
    https://its.1c.ru/db/content/v8std/src/600/i8100669.htm  
    Safe mode, privileged boundaries, HTTPS verification.

13. **Транзакции: правила использования — стандарт 783**  
    https://its.1c.ru/db/content/v8std/src/300/300/i8100783.htm  
    Парность транзакций, обработка исключений, запрет вызова внешних ресурсов внутри транзакции.

14. **Минимизация количества серверных вызовов и трафика — стандарт 487**  
    https://its.1c.ru/db/content/v8std/src/500/i8100487.htm

15. **Минимизация кода, выполняемого на клиенте — стандарт 629**  
    https://its.1c.ru/db/content/v8std/src/500/i8100629.htm

16. **Таймауты при работе с внешними ресурсами — стандарт 748**  
    https://its.1c.ru/db/content/v8std/src/500/i8100748.htm

17. **Общие требования к регламентным заданиям — стандарт 540**  
    https://its.1c.ru/db/content/v8std/src/200/500/i8100540.htm

18. **Запуск регламентных заданий — стандарт 539**  
    https://its.1c.ru/db/content/v8std/src/200/500/i8100539.htm

19. **Ограничения на регламентные задания в режиме сервиса — стандарт 760**  
    https://its.1c.ru/db/content/v8std/src/200/500/i8100760.htm

20. **Перехват исключений в коде — стандарт 499**  
    https://its.1c.ru/db/content/v8std/src/400/200/i8100499.htm

21. **Использование Журнала регистрации — стандарт 498**  
    https://its.1c.ru/db/content/v8std/src/400/200/i8100498.htm

22. **Правила создания общих модулей — стандарт 469**  
    https://its.1c.ru/db/content/v8std/src/200/100/i8100469.htm

23. **Обработчики обновления информационной базы (БСП) — стандарт 690**  
    https://its.1c.ru/db/content/v8std/src/900/i8100690.htm  
    Versioned/idempotent update handlers, deferred processing.

24. **HTTP-сервисы (REST) — Технологии интеграции 1С:Предприятия 8.3**  
    https://its.1c.ru/db/content/intgr83/src/24.html

25. **JSON — Технологии интеграции 1С:Предприятия 8.3**  
    https://its.1c.ru/db/intgr83/content/6/hdoc

26. **Язык запросов — оптимизация запросов**  
    https://its.1c.ru/db/pubqlang/content/138/hdoc

## Community tooling (optional, secondary)

27. **YAxUnit**  
    https://github.com/bia-technologies/yaxunit  
    Open-source unit/integration testing extension for 1C.

28. **Vanessa Automation**  
    https://github.com/Pr-Mex/vanessa-automation  
    Open-source BDD/scenario testing for 1C.

29. **BSL Language Server**  
    https://github.com/1c-syntax/bsl-language-server  
    Additional static analysis/LSP tooling. Use as a complement to 1C:EDT checks, not a substitute for platform-aware validation.

## Project-specific basis for Orbitas profile

Orbitas ERP connectors normalize heterogeneous ERP data into one domain model; ERP-specific objects must not leak into the clearing core. The connector profile also preserves the project invariant that a redirect settlement instruction is not itself proof that an invoice is paid. Those project constraints were carried over from the Orbitas BRD/PRD/TRD work and the previously created Odoo connector skill.
