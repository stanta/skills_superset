---
name: analyzing-wishart-graph-compression
description: Анализирует результаты recursive Wishart graph coarsening / compression для SemanticMap/semgraphex: сравнивает уровни level_XXX и transition_XXX_YYY, измеряет изменение динамических и структурных параметров при сжатии, сравнивает typed_wl, graphlet, relation_js, lowrank_gw и fgw при одинаковой степени сжатия, проверяет инварианты, устойчивость по seeds и null-baselines. Use for Wishart results, graph compression, coarsening, dynamical invariants, ConceptNet, semmap-wishart, hierarchy.json, dynamic_metrics.json, dynamic_vectors.npz, cluster_dynamics.jsonl.
metadata:
  category: research-analysis
  project: SemanticMap/semgraphex
---

# Анализ результатов Wishart-сжатия семантического графа

## Назначение

Используй этот skill для анализа результатов `semmap-wishart`, когда цель — понять **как изменяются свойства графа при рекурсивном сжатии**, какие характеристики приблизительно сохраняются, какие закономерно меняются, где возникают scale plateaus и какая метрика близости Wishart лучше сохраняет динамику при сопоставимой степени сжатия.

Главный принцип:

> Хорошее сжатие не обязано сохранять микроструктуру. Оно должно давать существенное уменьшение графа при контролируемом изменении выбранных макроскопических и динамических характеристик.

Не своди анализ к одной цифре. Разделяй:
1. структурное уменьшение;
2. скалярные динамические показатели;
3. распределения и векторы;
4. спектральные подпространства;
5. relation-aware потоки;
6. устойчивость результата к метрике и случайности.

Подробные формулы: [references/metrics-and-formulas.md](references/metrics-and-formulas.md).  
Статистическая валидация: [references/statistical-validation.md](references/statistical-validation.md).  
Шаблон отчёта: [references/report-template.md](references/report-template.md).

---

## Когда применять

Применяй skill, если пользователь просит:

- проанализировать `tmp/runs/wishart-*`;
- сравнить уровни `G_0 -> G_1 -> ...`;
- понять, какие параметры сохраняются или разрушаются при coarsening;
- сравнить `typed_wl`, `graphlet`, `relation_js`, `lowrank_gw`, `fgw`;
- найти оптимальную глубину сжатия;
- обнаружить scale plateau;
- сравнить Wishart с random/Haken/degree-matched baseline;
- оценить dynamical invariance;
- подготовить исследовательский отчёт по recursive compression.

---

# 1. Ожидаемый формат эксперимента

Ищи:

```text
run/
  COMPLETED
  hierarchy.json
  input.json

  level_000/
    adjacency.npz
    relations/
    membership.json
    dynamic_metrics.json
    dynamic_vectors.npz

  transition_000_001/
    wishart.json
    candidate_labels.npz
    figure_occurrences.jsonl
    cluster_dynamics.jsonl
    fine_to_coarse.npy

  level_001/
  transition_001_002/
  ...
```

Если структура отличается, сначала зафиксируй фактический schema и адаптируй анализ. Не выдумывай отсутствующие показатели.

---

# 2. Сначала проверь целостность эксперимента

Перед интерпретацией:

1. Убедись, что есть `COMPLETED`.
2. Прочитай `hierarchy.json`.
3. Сверь количество уровней и переходов с реальными каталогами.
4. Для каждого уровня проверь согласованность:
   - размер `adjacency.npz`;
   - количество записей в `membership.json`;
   - размер `stationary_mass`;
   - размер betweenness;
   - наличие relation layers.
5. Для перехода проверь:
   - длина `fine_to_coarse.npy == N_s`;
   - значения отображения лежат в `[0,N_{s+1}-1]`;
   - все исходные узлы входят ровно в один coarse node;
   - число записей `cluster_dynamics.jsonl == N_{s+1}`.
6. Если сравниваются разные метрики, убедись, что исходный `G_0` одинаков:
   - лучше всего — SHA-256 `level_000/adjacency.npz`;
   - дополнительно — одинаковые node IDs / membership;
   - одинаковая подготовка ConceptNet.
7. Сравни конфигурации. Если кроме `wishart.metric` менялись radius, k, significance, candidate_limit, aggregation или sampling-параметры — это уже не чистое сравнение метрик.

Если integrity check не пройден, сначала сообщи проблему и не делай сильных выводов.

---

# 3. Построй базовую таблицу траектории сжатия

Для каждого уровня (s) собери одну строку:

- metric;
- seed;
- level;
- (N_s);
- adjacency_nnz;
- число relation layers;
- число Wishart clusters на предыдущем переходе;
- noise fraction;
- число accepted figure occurrences;
- cumulative compression fraction;
- compression ratio;
- все scalar dynamic metrics.

Определи:

[
c_s = 1-rac{N_s}{N_0}
]

как долю удалённых степеней свободы и

[
R_s=rac{N_0}{N_s}
]

как коэффициент сжатия.

**Не сравнивай разные методы по номеру level.**  
Сравнивай их при близком (c_s) или (R_s).

---

# 4. Разделяй параметры на четыре класса

## A. Контрольные/почти обязательные инварианты

Проверяй в первую очередь:

- агрегированную stationary mass;
- relation-total weight при `aggregation=sum`;
- external relation flow в пределах ожидаемой перенормировки;
- slow eigenspace;
- leading nontrivial eigenvalues.

Если эти величины резко ломаются на ранних уровнях, coarsening динамически агрессивен.

## B. Динамические показатели сохранности

- normalized-adjacency spectral gap;
- MFPT;
- spreading-threshold proxy;
- percolation-threshold proxy;
- synchronizability proxy;
- congestion-threshold proxy.

Их не называй точными инвариантами без отдельного доказательства. Анализируй как **dynamical observables**.

## C. Scale-dependent структурные характеристики

Ожидаемо могут заметно меняться:

- mean degree;
- second moment of degree;
- clustering;
- betweenness;
- mean/median/p95 shortest-path distance.

Здесь интересен не только размер ошибки, но и **закономерность изменения с масштабом**.

## D. Служебные показатели Wishart

- cluster_count;
- cluster_sizes;
- cluster_peaks;
- noise_count;
- kth_radius;
- accepted occurrences;
- размер фигур;
- вклад каждого figure_type в общее сокращение (N).

Они объясняют, *почему* граф сжимается именно так.

---

# 5. Для каждого scalar Q считай три разных изменения

Не используй только соседний процент.

### Шаговое изменение

[
Delta_s(Q)=rac{Q_{s+1}-Q_s}{|Q_s|+arepsilon}.
]

Показывает локальный скачок после конкретного coarsening.

### Искажение относительно исходного графа

[
D_s(Q)=rac{|Q_s-Q_0|}{|Q_0|+arepsilon}.
]

Это основной показатель сохранности.

### Scale elasticity

Для положительных величин:

[
E_s(Q)=
rac{log Q_{s+1}-log Q_s}
{log N_{s+1}-log N_s}.
]

Если (E_s(Q)) стабилен на нескольких уровнях, это кандидат на scaling law.

Не используй elasticity для нулей, знакопеременных параметров или нестабильных Monte-Carlo оценок.

---

# 6. Stationary mass анализируй через отображение fine -> coarse

Нельзя сравнивать (pi_s) и (pi_{s+1}) по индексам: размерности различны.

Пусть (P_s) — membership matrix из `fine_to_coarse.npy`.

Агрегируй fine stationary distribution:

[
pi_s^{agg}=P_s^Tpi_s.
]

Сравни с фактически вычисленной coarse distribution:

[
pi_{s+1}.
]

Основные ошибки:

[
E_pi^{L1}=|pi_s^{agg}-pi_{s+1}|_1
]

и total variation:

[
E_pi^{TV}=rac12 E_pi^{L1}.
]

Для undirected nonnegative graph + `aggregation=sum` stationary mass должна быть особенно хорошо сохранена. Большая ошибка здесь — прежде всего повод проверить реализацию и веса, а не делать физический вывод.

---

# 7. Slow eigenmodes сравнивай как подпространства

**Никогда не сравнивай eigenvectors покомпонентно.**

Причины:
- знак собственного вектора произволен;
- внутри почти вырожденного спектрального блока базис может вращаться.

Для (r) медленных мод:

1. возьми (U_s);
2. подними coarse modes на fine nodes через membership;
3. ортонормируй;
4. вычисли principal angles;
5. вычисли projection/subspace distance.

Дополнительно сравни eigenvalues по рангу:

[
E_lambda =
rac{|lambda_s-lambda_{s+1}|_2}
{|lambda_s|_2+arepsilon}.
]

Сильное сохранение slow subspace при большом уменьшении (N) — один из главных признаков динамически содержательного coarse-graining.

Источник: Gfeller & De Los Rios формулируют цель spectral coarse graining как сохранение “**the slow modes of the walk**”.

---

# 8. Spectral gap

В текущем `semmap-wishart` spectral gap — разность двух крупнейших eigenvalues **normalized adjacency**, а не обязательно Laplacian (lambda_2).

Анализируй:

[
D_s(gap)
]

и кривую gap versus compression.

Не смешивай этот показатель с synchronizability ratio.

Если gap резко меняется на одном переходе, проверь:
- какие figure types были стянуты;
- не исчез ли bottleneck/community boundary;
- не стал ли граф почти disconnected.

---

# 9. MFPT интерпретируй вместе с hit rate

Текущий MFPT — Monte-Carlo estimate с конечным `mfpt_max_steps`.

Поэтому всегда показывай пару:

[
(MFPT_s, hit_rate_s).
]

Запрещено делать вывод “MFPT улучшился”, если одновременно сильно упал hit rate: среднее может уменьшиться просто потому, что длинные ненайденные траектории были censored.

Если hit rate нестабилен:
- увеличь `mfpt_max_steps`;
- увеличь число пар/траекторий;
- повтори несколько seeds;
- трактуй MFPT как ненадёжный.

---

# 10. Degree moments и thresholds

Текущая реализация считает topological degree, отдельно от weighted strength.

Следи за:

[
langle kangle,qquad langle k^2angle.
]

Именно изменение второго момента часто объясняет изменение threshold proxies.

В текущем коде:

[
T_{spread}approx
rac{langle kangle}{langle k^2angle}
]

и

[
T_{perc}approx
rac{langle kangle}
{langle k^2angle-langle kangle}.
]

Называй их **proxies**, а не универсальными истинными порогами ConceptNet.

При каждом заметном изменении threshold сначала покажи, что произошло с (langle k^2angle/langle kangle).

Barrat–Barthélemy–Vespignani: “**larger heterogeneity levels lead to smaller epidemic thresholds**”.

---

# 11. Synchronizability

Текущий показатель:

[
S=rac{lambda_{max}(L)}{lambda_2(L)}.
]

Для стандартного master-stability контекста меньший ratio обычно означает более благоприятную синхронизируемость.

Но:
- показатель имеет смысл прежде всего для connected undirected coupling graph;
- при (lambda_2approx0) он становится огромным/неопределённым;
- это topology proxy, а не симуляция конкретных осцилляторов.

Не делай вывод о физической синхронизации семантического графа без явно заданной dynamical model.

---

# 12. Congestion и betweenness

Текущий proxy:

[
R_c=rac{N-1}{b^*},
qquad
b^*=max_i b_i.
]

Показывай одновременно:
- (b^*);
- (R_c);
- (N).

Иначе изменение (R_c) трудно интерпретировать.

Если betweenness sampled, считай результат noisy diagnostic и требуй повторов по seed.

Barrat et al.: “**The larger the maximal betweenness ... the smaller the traffic injection rate**”.

---

# 13. Clustering и shortest-path distances

Эти параметры обычно не являются инвариантами.

Смотри:
- monotonicity;
- резкие structural transitions;
- relation с размером фигур;
- plateaus.

Для distances желательно дополнительно пересчитать:
- diameter;
- global efficiency;
- normalized mean distance.

Если исходный граф disconnected, анализируй reachable pairs отдельно.

---

# 14. Relation-aware flow — обязательный SemanticMap-анализ

Для каждого relation (r) и уровня (s) загрузи `relations/*.npz`.

Считай:

[
W_r(s)=sum_{ij}A^{(r)}_{ij},
]

[
W_r^{loop}(s)=mathrm{tr}(A^{(r)}),
]

[
W_r^{off}(s)=W_r(s)-W_r^{loop}(s).
]

Для `aggregation=sum` общий (W_r) должен быть почти conserved.

Рост

[
I_r(s)=rac{W_r^{loop}(s)}{W_r(s)}
]

показывает, какая доля relation (r) стала внутренней структурой суперузлов.

Это один из наиболее содержательных параметров для ConceptNet: он показывает, **какие семантические отношения “схлопываются” раньше других**.

Строй relation × level heatmap для (I_r(s)).

---

# 15. Анализ внешнего интерфейса фигур

Из `cluster_dynamics.jsonl` для каждого нового coarse node анализируй:

- external_flow;
- external_flow_by_relation;
- stationary_mass;
- exit_probabilities;
- figure_type;
- original_concepts / concept_concat.

Для cluster (C) полезно вычислить leakage:

[
ell_C=
rac{F_{out}(C)}
{F_{out}(C)+F_{internal}(C)}.
]

Низкая leakage означает более автономную фигуру.

Сравни распределения leakage по figure_type.

---

# 16. Wishart clusters не равны автоматически “хорошим фигурам сжатия”

Для каждого `figure_type` посчитай:

- occurrences;
- median number of nodes;
- total nodes removed;
- median kth_radius;
- within-type variation;
- external-flow profile;
- relation profile;
- dynamic distortion после contraction.

Ищи типы, которые:
1. часто повторяются;
2. дают заметное сжатие;
3. имеют стабильный внешний интерфейс;
4. дают малую dynamical distortion.

Именно они — лучшие кандидаты на устойчивые compression figures.

---

# 17. Сравнение разных Wishart metrics

Сравнивай:

- typed_wl;
- graphlet;
- relation_js;
- lowrank_gw;
- fgw.

Главное правило:

[
oxed{	ext{compare at matched compression, not matched level}}
]

Например, если typed-WL достиг (c=0.50) на level 2, а FGW на level 4 — сравни эти точки.

Если точных совпадений нет:
- интерполируй metric-vs-compression curve;
- либо используй ближайшую точку и явно укажи разницу в compression.

Строй Pareto plot:

[
x=c_s,qquad y=D_s(Q).
]

Лучший метод для данного (Q) даёт большее сжатие при меньшем искажении.

Не объявляй одну метрику абсолютным победителем, если trade-offs различаются по параметрам.

---

# 18. Обязательно анализируй случайность

Источники random variation:

- sampling candidate centers;
- graphlet sampling;
- MFPT Monte Carlo;
- sampled betweenness;
- clustering samples;
- sampled distances;
- transport solver initialization/approximations.

Для исследовательского вывода используй несколько seeds.

Минимум отчёта:
- median;
- IQR или bootstrap 95% CI;
- число repeats.

Один seed — exploratory result, не устойчивый вывод.

---

# 19. Null baselines

Wishart должен сравниваться хотя бы с одним control coarsening при том же (N_s).

Рекомендуемые baselines:

1. random disjoint contraction с тем же распределением размеров блоков;
2. degree-matched contraction;
3. relation-shuffled graph;
4. существующий Haken-coarsening semgraphex.

Для каждого baseline сравни:

[
D_s^{Wishart}(Q)
quad 	ext{vs} quad
D_s^{baseline}(Q)
]

при одинаковой compression fraction.

Если Wishart не лучше random contraction, нельзя утверждать, что найденные modes функционально значимы.

---

# 20. Поиск scale plateau

Scale plateau — диапазон уровней/компрессии, где:

- (N) заметно уменьшается;
- выбранные dynamical distortions остаются малы;
- step changes не имеют крупных скачков;
- slow eigenspace остаётся близким;
- результаты воспроизводятся по seeds.

Не определяй plateau “на глаз”.

Задай набор observables (Q_j) и operational tolerances (t_j), затем требуй:

[
D_s(Q_j)le t_j
]

для всех обязательных (Q_j) на последовательном диапазоне compression.

Tolerances должны быть:
- заранее объявлены;
- проверены sensitivity analysis;
- не выбираться после просмотра результата.

---

# 21. Опциональный composite preservation score

Сначала всегда показывай отдельные показатели.

Только затем можно вычислить:

[
D_{dyn}(s)=
rac{sum_j w_j,D_s(Q_j)/t_j}
{sum_j w_j}.
]

Где:
- (w_j) — заранее заданная важность;
- (t_j) — допустимая шкала изменения.

Не подбирай (w_j) для получения желаемого победителя.

Также показывай worst-case:

[
D_{max}(s)=max_j D_s(Q_j)/t_j.
]

---

# 22. Что считать сильным результатом

Сильное свидетельство в пользу полезного Wishart-coarsening:

- существенное (N_0/N_s);
- низкая stationary-mass aggregation error;
- устойчивый slow eigenspace;
- умеренные изменения spectral/dynamic observables;
- Wishart превосходит matched random baseline;
- результат воспроизводится по seeds;
- несколько разных similarity metrics дают сходную качественную картину;
- relation-aware структуры не разрушаются сразу;
- существует интервал scale plateau.

---

# 23. Что считать отрицательным или фальсифицирующим результатом

Не скрывай:

- modes есть, но contraction разрушает slow dynamics;
- фигуры зависят только от одного seed;
- разные similarity metrics дают несовместимые результаты;
- thresholds скачут из-за коллапса degree heterogeneity;
- stationary mass не сохраняется даже там, где должна;
- relation structure быстро превращается в self-loops;
- Wishart не превосходит random baseline;
- plateau отсутствует.

Это ценные результаты, а не “ошибка эксперимента”.

---

# 24. Обязательные визуализации

Минимальный набор:

1. (N_s/N_0) vs level.
2. Все scalar observables vs compression fraction.
3. Baseline distortion (D_s(Q)) vs compression.
4. stationary-mass TV error vs compression.
5. slow-eigenspace distance vs compression.
6. slow eigenvalue trajectories.
7. degree moments + spreading/percolation proxies.
8. MFPT вместе с hit rate.
9. max betweenness + congestion threshold.
10. relation internalization heatmap.
11. Wishart cluster count/noise/occurrences.
12. cross-metric Pareto plots.
13. seed uncertainty bands.
14. baseline comparison.

---

# 25. Обязательные правила интерпретации

Никогда не:

- называй Wishart cluster семантическим примитивом только из-за плотности;
- сравнивай eigenvectors напрямую;
- сравнивай разные metrics только по level index;
- называй proxies точными физическими thresholds;
- интерпретируй MFPT без hit rate;
- делай вывод по одному seed;
- смешивай topological degree и weighted strength;
- считай ConceptNet weight эмпирической transition probability;
- скрывай caveats из `dynamic_metrics.json`;
- утверждай multifractality только по наличию рекурсивной иерархии.

---

# 26. Формат итогового ответа агента

Всегда выдай:

1. **Integrity / comparability** — можно ли доверять сравнению.
2. **Compression trajectory** — насколько граф уменьшился.
3. **Parameter-by-parameter changes** — что изменилось и почему.
4. **Preserved quantities** — только с численной ошибкой.
5. **Broken quantities** — где и на каком масштабе.
6. **Wishart-specific analysis** — modes, noise, figure types.
7. **Cross-metric comparison** — на matched compression.
8. **Seed robustness**.
9. **Null/baseline comparison**, если доступен.
10. **Scale plateau**, если он статистически поддерживается.
11. **Semantic follow-up** по `concept_concat`, но отдельно от topology-only вывода.
12. **Sources and short quotes**.
13. **Limitations / falsification conditions**.

---

# 27. Evidence basis

Используй эти работы как методологическую опору, а не как доказательство результата конкретного эксперимента:

- Wishart, 1969, *Numerical Classification Method for deriving Natural Classes*.  
  https://doi.org/10.1038/221097a0  
  Короткая цитата: “**clusters should correspond to data modes**”.

- Gfeller & De Los Rios, 2007, *Spectral Coarse Graining of Complex Networks*.  
  https://doi.org/10.1103/PhysRevLett.99.038701  
  Короткая цитата: “**preserves the slow modes of the walk**”.

- Barrat, Barthélemy & Vespignani, 2008, *Dynamical Processes on Complex Networks*.  
  https://doi.org/10.1017/CBO9780511791383  
  Короткая цитата: “**the larger the degree ... the larger the probability of being visited**”.

- Shervashidze et al., 2011, *Weisfeiler-Lehman Graph Kernels*.  
  https://www.jmlr.org/papers/v12/shervashidze11a.html  
  Короткая цитата: “**runtime scales only linearly in the number of edges**”.

- Shervashidze et al., 2009, *Efficient Graphlet Kernels for Large Graph Comparison*.  
  https://proceedings.mlr.press/v5/shervashidze09a.html  
  Короткая цитата: “**Exhaustive enumeration of all graphlets being prohibitively expensive**”.

- Vayer et al., 2019, *Optimal Transport for structured data with application on graphs*.  
  https://proceedings.mlr.press/v97/titouan19a.html

- Scetbon, Peyré & Cuturi, 2022, *Linear-Time Gromov Wasserstein Distances using Low Rank Couplings and Costs*.  
  https://proceedings.mlr.press/v162/scetbon22b.html  
  Короткая цитата: “**linear time O(n) GW approximation**”.
