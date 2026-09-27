# Git и GitHub: практическая инструкция

Проверено по официальной документации Git и GitHub: 27.09.2026. Документ рассчитан на разработчиков и ИИ-агентов с разрешённым доступом к репозиторию. Локальные правила CONTRIBUTING, защиты веток, CI и инструкция владельца имеют приоритет над примерами. Ни одна команда ниже не означает согласия удалять чужие данные.

## 1. Перед началом

Изучите состояние рабочей директории, назначение remote и правила проекта:

```bash
git rev-parse --show-toplevel
git status --short --branch
git branch -vv
git remote -v
git diff --check
git diff --cached --check
```

Не меняйте и не прячьте чужие незакоммиченные файлы. Если среда уже создала изолированный worktree, используйте его. Для параллельной разработки изучите [using-git-worktrees](../../atomic-skills/using-git-worktrees/SKILL.md).

## 2. Типовой цикл

На **чистой** локальной основной ветке загрузите изменения, создайте тематическую ветку и коммитьте только проверенный diff:

```bash
git fetch origin --prune
git switch main
git pull --ff-only
git switch -c feat/payment-retries
# работа над небольшим изменением
git add -p
git diff --cached --check
git diff --cached
git commit -m "fix: handle payment retry"
git push -u origin HEAD
```

Замените `main` на фактическую основную ветку. Запускайте тесты/линтер до PR и повторно после разрешения конфликтов. Делайте небольшие законченные коммиты, описывающие намерение. Не коммитьте ключи, токены, .env, результаты сборки и большие бинарники. Используйте формат сообщений и правила подписания, принятые в проекте.

**Синхронизация:** `git fetch` обновляет remote-tracking refs, не меняя рабочую ветку. Для общей истории используйте согласованный merge-подход; rebase прежде всего подходит для собственных неопубликованных веток. Переписывание опубликованной ветки требует согласования; при санкционированном обновлении feature-ветки предпочитайте `--force-with-lease`. Не форсируйте защищённую основную ветку.

## 3. Ошибка, конфликт, потеря коммита

Сначала проверьте `git status`, `git log --graph --oneline -20` и `git reflog -30`. Не запускайте наугад `git reset --hard` и `git clean -fdx`. Для снятия файла с индекса с сохранением текста используйте `git restore --staged -- path`; для отмены опубликованного коммита обычно `git revert <sha>`. Если нужно прервать rebase, проверьте, что происходит, затем `git rebase --abort`. Для потерянного коммита найдите SHA через reflog и создайте спасательную ветку `git branch rescue/<case> <sha>`. Ограничения восстановления подробно описаны в [git-history-recovery](../../atomic-skills/git-history-recovery/SKILL.md).

Если в историю попал секрет, **сначала отзовите/ротируйте его** и оцените последствия. Удалить его из последнего файла недостаточно: он может остаться в старых коммитах, форках, артефактах и кэшах. Историю очищайте только по согласованному плану с владельцами репозитория.

## 4. GitHub: Issue → PR → review → merge

Зафиксируйте задачу и критерии приёмки в Issue. Ветка или fork → узкий draft PR → описание причины и изменений, результатов тестов и рисков → релевантные ревьюеры/CODEOWNERS → устранение замечаний → повторные проверки → merge при выполненных требованиях защиты ветки. Проверяйте базовую ветку PR и итоговый merged commit. Автоматические проверки не заменяют содержательное ревью.

Для администраторов: защитите main/release через branch protection или ruleset, рассмотрите обязательные PR, ревью, CODEOWNERS с защитой самого файла, уникальные названия обязательных CI-статусов, запрет force-push/delete и минимум обходных прав. Merge queue включайте там, где она доступна и оправдана; обязательные Actions должны тогда обрабатывать `merge_group`. Доступность настроек зависит от тарифа и типа репозитория.

## 5. GitHub Actions и секреты

Проверяйте код недоверенных PR без секретов и с минимальными правами. В CI задавайте `permissions: { contents: read }` и расширяйте права лишь конкретному job. Не исполняйте PR-код в привилегированном `pull_request_target`. Закрепляйте сторонние Actions на проверенном полном SHA и планово обновляйте; не придумывайте SHA. Для облачного деплоя предпочитайте краткоживущую OIDC-аутентификацию с ограничениями по репозиторию, workflow/ref и окружению. Защитите production environments, проверяйте артефакты и используйте доступные Dependabot, secret scanning/push protection и code scanning.

## 6. Проверка завершения

Перед «готово» проверьте diff и `git status`, реальные результаты тестов, SHA целевой ветки, обязательные checks/reviews и отсутствие секретов. Если инструмент, права или CI недоступны, сообщите точно, что сделано и что осталось.

## Скиллы и первоисточники

- [Git core](../../atomic-skills/git-core-workflows/SKILL.md), [Git recovery](../../atomic-skills/git-history-recovery/SKILL.md).
- [GitHub PR workflows](../../atomic-skills/github-pull-request-workflows/SKILL.md), [GitHub Actions DevSecOps](../../atomic-skills/github-actions-devsecops/SKILL.md).
- [Git manuals](https://git-scm.com/docs), [GitHub flow](https://docs.github.com/en/get-started/using-github/github-flow), [protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches), [Actions security](https://docs.github.com/en/actions/how-tos/secure-your-work).
