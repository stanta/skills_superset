---
name: analyzing-wishart-graph-compression
description: Анализирует результаты recursive Wishart graph coarsening / compression для SemanticMap/semgraphex: level_XXX, transition_XXX_YYY, hierarchy.json, dynamic_metrics.json, dynamic_vectors.npz, cluster_dynamics.jsonl. Сравнивает изменение параметров графа при сжатии, typed_wl, graphlet, relation_js, lowrank_gw и fgw при одинаковой степени сжатия, проверяет dynamical invariants, scale plateaus, seeds и null baselines.
metadata:
  category: research-analysis
  project: SemanticMap/semgraphex
---
# Анализ результатов Wishart-сжатия семантического графа
## Назначение
Используй skill для исследования того, **как меняются свойства графа при рекурсивном Wishart-coarsening** и какие характеристики сохраняются при уменьшении числа узлов.
Главный принцип:
> Хорошее сжатие не обязано сохранять микроструктуру; оно должно давать существенное уменьшение графа при контролируемом изменении выбранной макродинамики.
Не своди результат к одной цифре. Разделяй:
1. степень сжатия;
2. scalar observables;
3. distributions/vectors;
4. slow spectral subspaces;
5. relation-aware flows;
6. Wishart mode structure;
7. устойчивость к seed, metric и baseline.
Подробности:
- [Metrics and formulas](references/metrics-and-formulas.md)
- [Statistical validation](references/statistical-validation.md)
- [Report template](references/report-template.md)
---
## Когда применять
Применяй, если нужно:
- анализировать `tmp/runs/wishart-*`;
- сравнить (G_0	o G_1	odots);
- понять, какие параметры сохраняются или ломаются;
- сравнить `typed_wl`, `graphlet`, `relation_js`, `lowrank_gw`, `fgw`;
- найти безопасную глубину сжатия;
- обнаружить scale plateau;
- сравнить Wishart с random, degree-matched или Haken coarsening;
- подготовить исследовательский отчёт.
---
# 1. Ожидаемые артефакты
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
Если schema отличается, сначала зафиксируй фактический формат. Не выдумывай отсутствующие данные.
---
# 2. Обязательный integrity check
До интерпретации:
1. Проверь `COMPLETED`.
2. Прочитай `hierarchy.json`.
3. Сверь число уровней и transitions.
4. Для каждого level проверь:
   - shape adjacency;
   - число membership entries;
   - длину stationary_mass;
   - длину betweenness;
   - relation layers.
5. Для transition проверь:
   - `len(fine_to_coarse) == N_s`;
   - coarse IDs допустимы;
   - каждый fine node имеет один coarse parent;
   - `cluster_dynamics.jsonl` согласован с (N_{s+1}).
6. При сравнении metrics проверь одинаковый (G_0), лучше SHA-256 `level_000/adjacency.npz`.
7. Проверь, что кроме `wishart.metric` не менялись существенно radius, k, significance, candidate_limit, aggregation и sampling controls.
Если integrity нарушен, сначала сообщи это и не делай сильных сравнительных выводов.
---
# 3. Построй master-table
Одна строка = один metric × seed × level.
Собери:
- metric;
- seed;
- level;
- (N_s);
- adjacency_nnz;
- compression fraction;
- compression ratio;
- Wishart cluster count;
- noise fraction;
- accepted figure occurrences;
- scalar dynamic metrics;
- caveats.
Используй:
[
c_s=1-rac{N_s}{N_0}
]
и
[
R_s=rac{N_0}{N_s}.
]
**Главное правило: сравнивай разные методы при одинаковом (c_s), а не при одинаковом level.**
---
# 4. Раздели показатели на классы
| Класс | Показатели | Как трактовать |
|---|---|---|
| Контрольные инварианты | stationary mass aggregation, relation total weight при sum | Большая ошибка часто означает bug/несогласованность |
| Спектральная сохранность | slow eigenspace, slow eigenvalues, spectral gap | Главные признаки сохранения крупномасштабной динамики |
| Dynamical observables | MFPT, spreading/percolation proxies, synchronizability, congestion | Сравнивать с оговорками модели и sampling |
| Scale-dependent topology | degree moments, clustering, betweenness, path lengths | Могут закономерно меняться |
| Wishart diagnostics | modes, peaks, noise, kth radius, occurrence sizes | Объясняют механизм coarsening |
| Semantic flow | relation internalization, external flow by relation | Показывают, какие связи становятся внутриблочными |
---
# 5. Для каждого scalar Q считай минимум два вида ошибки
### Шаговое изменение
[
Delta_s(Q)=
rac{Q_{s+1}-Q_s}{|Q_s|+arepsilon}.
]
Ищи резкие переходы.
### Искажение относительно исходного графа
[
D_s(Q)=
rac{|Q_s-Q_0|}{|Q_0|+arepsilon}.
]
Используй это как главный scalar preservation score.
Опционально для положительных устойчивых величин считай log-elasticity по (N). Формулы — в metrics reference.
---
# 6. Stationary mass: сравнивай через fine-to-coarse map
Нельзя сравнивать (pi_s) и (pi_{s+1}) по индексам.
Построй membership matrix (P_s) из `fine_to_coarse.npy` и вычисли:
[
widehatpi_{s+1}=P_s^Tpi_s.
]
Сравни с coarse stationary mass через:
- L1 error;
- total variation.
Для undirected nonnegative + `aggregation=sum` большая ошибка — сначала проверка реализации, потом научная интерпретация.
---
# 7. Slow modes: сравнивай подпространства, не raw eigenvectors
Raw eigenvectors нельзя сопоставлять покомпонентно:
- знак произволен;
- внутри близких eigenvalues базис может вращаться.
Используй:
- principal angles;
- projection/subspace distance;
- relative slow-eigenvalue error.
Сильное сохранение slow subspace при заметном уменьшении (N) — один из основных позитивных результатов.
Источник Gfeller & De Los Rios: coarse graining “**preserves the slow modes of the walk**”.
---
# 8. Spectral gap
В текущем `semmap-wishart` gap относится к **normalized adjacency**, не смешивай его с Laplacian (lambda_2).
Строй:
- gap vs compression;
- baseline distortion of gap;
- step jumps.
При скачке проверь, какие figure types стягивались и не исчез ли bottleneck.
---
# 9. MFPT всегда анализируй с hit rate
Текущий MFPT — Monte-Carlo estimate с finite step cap.
Всегда показывай:
[
(MFPT_s, hit_rate_s).
]
Если MFPT уменьшается, но hit rate тоже падает, это может быть censoring artifact.
При нестабильном hit rate:
- увеличь max steps;
- увеличь sampling;
- повтори seeds;
- ослабь вывод.
---
# 10. Degree moments объясняют threshold drift
Показывай вместе:
- (langle kangle);
- (langle k^2angle);
- (kappa=langle k^2angle/langle kangle);
- spreading proxy;
- percolation proxy.
Текущие formulas — proxies, не универсальные физические пороги ConceptNet.
Barrat et al.: “**larger heterogeneity levels lead to smaller epidemic thresholds**”.
---
# 11. Synchronizability и congestion трактуй осторожно
Synchronizability proxy использует Laplacian eigenratio. Он имеет смысл прежде всего для connected undirected coupling graph и стандартного master-stability контекста.
Congestion proxy анализируй вместе с:
- (N);
- max betweenness;
- path lengths.
Barrat et al.: “**The larger the maximal betweenness ... the smaller the traffic injection rate**”.
Если betweenness sampled, требуй repeats.
---
# 12. Relation-aware analysis обязателен
Для каждого relation (r) загрузи `relations/*.npz`.
Считай:
- total relation weight;
- diagonal/self-loop weight;
- off-diagonal weight;
- internalization fraction.
При `aggregation=sum` total relation weight должен быть почти conserved.
Ключевой вопрос:
> Какие ConceptNet relations становятся внутренними для суперузлов раньше других?
Строй relation × compression heatmap.
---
# 13. Анализируй внешний интерфейс фигур
Из `cluster_dynamics.jsonl` используй:
- external_flow;
- external_flow_by_relation;
- stationary_mass;
- exit_probabilities;
- figure_type;
- original_concepts;
- concept_concat.
Для figure type оцени:
- occurrence count;
- median size;
- nodes removed;
- kth-radius distribution;
- leakage/external-flow distribution;
- relation profile;
- associated dynamic distortion.
Wishart mode — только **candidate compression type**, а не автоматически “хорошая фигура”.
---
# 14. Cross-metric comparison
Сравни:
- typed_wl;
- graphlet;
- relation_js;
- lowrank_gw;
- fgw.
Правило:
[
oxed{	ext{matched compression, not matched level}}
]
Если одинакового (c) нет:
- используй ближайшую observed point;
- либо интерполируй между соседними compression points;
- не extrapolate без caveat.
Строй Pareto plots:
[
x=c,qquad y=D(Q).
]
Не объявляй один global winner без заранее заданной функции полезности.
---
# 15. Повторяй seeds
Источники randomness:
- candidate subsampling;
- graphlet sampling;
- MFPT;
- betweenness;
- clustering;
- sampled distances;
- approximate transport.
Один seed = exploratory evidence.
Для серии repeats показывай:
- median;
- IQR;
- 95% bootstrap CI, если repeats достаточно.
Подробный протокол — statistical-validation reference.
---
# 16. Null baselines обязательны для сильного вывода
Минимум:
1. random disjoint contraction с теми же block sizes;
2. degree-matched contraction.
Желательно:
3. relation-label shuffle;
4. Haken coarsening из semgraphex.
Сравни при одинаковой compression fraction.
Если Wishart не лучше matched random contraction по выбранным observables, нельзя утверждать, что найденные modes функционально значимы.
---
# 17. Scale plateau
Plateau — диапазон compression, где:
- (N) продолжает уменьшаться;
- обязательные distortions остаются ниже заранее заданных tolerances;
- slow eigenspace стабилен;
- нет крупных step jumps;
- результат воспроизводится по seeds.
Не находи plateau “на глаз”.
Задай tolerances **до** выбора желаемого результата.
---
# 18. Composite score — только вторично
Сначала показывай отдельные observables.
Затем допустим weighted normalized distortion и worst-case distortion.
Не подбирай weights постфактум.
Если разные metrics дают trade-offs, показывай Pareto frontier вместо одного рейтинга.
---
# 19. Сильный позитивный результат
Сильное свидетельство полезного Wishart-coarsening требует сочетания:
- заметного compression ratio;
- малой stationary-mass aggregation error;
- устойчивого slow eigenspace;
- умеренного drift выбранных dynamics metrics;
- лучшего результата, чем matched random baseline;
- повторяемости по seeds;
- частичной устойчивости к choice of similarity metric;
- relation-aware структуры, не уничтожаемой сразу;
- при наличии — scale plateau.
---
# 20. Отрицательные результаты также обязательны
Явно сообщай, если:
- modes есть, но slow dynamics рушится;
- result seed-sensitive;
- different metrics дают несовместимые картины;
- thresholds скачут из-за потери degree heterogeneity;
- stationary mass не сохраняется там, где должна;
- relations быстро уходят в self-loops;
- Wishart не лучше random baseline;
- plateau отсутствует.
Не маскируй это как “нужно больше оптимизации”.
---
# 21. Обязательные визуализации
Минимум:
1. (N_s/N_0) vs level.
2. compression fraction vs level.
3. scalar observables vs compression.
4. baseline distortions vs compression.
5. stationary-mass TV vs compression.
6. slow-eigenspace distance vs compression.
7. slow eigenvalue trajectories.
8. degree moments + threshold proxies.
9. MFPT + hit rate.
10. max betweenness + congestion.
11. relation internalization heatmap.
12. Wishart modes/noise/occurrences.
13. cross-metric Pareto curves.
14. seed uncertainty bands.
15. null/baseline comparison.
---
# 22. Non-negotiable interpretation rules
Никогда не:
- называй Wishart cluster семантическим примитивом только из-за density;
- сравнивай raw eigenvectors;
- сравнивай methods только по level;
- называй threshold proxies точными физическими thresholds;
- интерпретируй MFPT без hit rate;
- делай publication-level вывод по одному seed;
- смешивай degree и weighted strength;
- считай ConceptNet weight эмпирической transition probability;
- игнорируй caveats в `dynamic_metrics.json`;
- утверждай multifractality только из recursive hierarchy;
- скрывай null result.
---
# 23. Формат результата агента
Всегда выдай:
1. **Integrity/comparability**.
2. **Compression trajectory**.
3. **Parameter-by-parameter changes**.
4. **Preserved quantities** с численной ошибкой.
5. **Broken quantities** и first breaking scale.
6. **Wishart mode analysis**.
7. **Relation-aware flow analysis**.
8. **Cross-metric comparison at matched compression**.
9. **Seed robustness**.
10. **Null/baseline comparison**.
11. **Scale plateau** или явное отсутствие.
12. **Semantic follow-up** по concept_concat отдельно от topology-only вывода.
13. **Sources + short quotes**.
14. **Limitations and falsification conditions**.
Используй [report template](references/report-template.md).
---
# 24. Evidence basis
Используй источники как методологическую опору, а не как доказательство конкретного результата.
- Wishart, 1969, *Numerical Classification Method for deriving Natural Classes*.  
  https://doi.org/10.1038/221097a0  
  “**clusters should correspond to data modes**”.
- Gfeller & De Los Rios, 2007, *Spectral Coarse Graining of Complex Networks*.  
  https://doi.org/10.1103/PhysRevLett.99.038701  
  “**preserves the slow modes of the walk**”.
- Barrat, Barthélemy & Vespignani, 2008, *Dynamical Processes on Complex Networks*.  
  https://doi.org/10.1017/CBO9780511791383  
  “**the larger the degree ... the larger the probability of being visited**”.
- Shervashidze et al., 2011, *Weisfeiler-Lehman Graph Kernels*.  
  https://www.jmlr.org/papers/v12/shervashidze11a.html  
  “**runtime scales only linearly in the number of edges**”.
- Shervashidze et al., 2009, *Efficient Graphlet Kernels for Large Graph Comparison*.  
  https://proceedings.mlr.press/v5/shervashidze09a.html  
  “**Exhaustive enumeration of all graphlets being prohibitively expensive**”.
- Vayer et al., 2019, *Optimal Transport for structured data with application on graphs*.  
  https://proceedings.mlr.press/v97/titouan19a.html
- Scetbon, Peyré & Cuturi, 2022, *Linear-Time Gromov Wasserstein Distances using Low Rank Couplings and Costs*.  
  https://proceedings.mlr.press/v162/scetbon22b.html  
  “**linear time O(n) GW approximation**”.
