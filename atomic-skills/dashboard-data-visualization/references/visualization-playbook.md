# Dashboard Visualization Playbook

## Question-to-chart matrix

| Question | Default | Avoid |
|---|---|---|
| What is the current state? | KPI/status card with target and timestamp | Gauge without actionable bands |
| Which categories are larger? | Sorted horizontal bars | Pie with many slices |
| How is a value changing? | Line with direct labels/reference line | Dense bars or smoothed curve hiding volatility |
| What is the distribution? | Histogram, box, quantile plot | Mean-only card |
| Are variables related? | Scatter with trend/uncertainty | Dual-axis line chart |
| How do a few parts compose a whole? | Stacked bar | 3D pie/donut |
| How do many groups compare? | Small multiples on shared scales | Overplotted “spaghetti” line chart |
| What exact records require action? | Sortable/filterable table | Chart requiring tooltip lookup |
| What happened in sequence? | Timeline with bounded lanes | Unbounded event stream on overview |
| Where is process flow concentrated? | Sankey only for true flow magnitude | Decorative node-link graph |

## KPI card contract

A KPI card contains:

- value and unit;
- semantic label;
- target, threshold, or prior-period comparison when meaningful;
- scope and time window;
- freshness/stale indicator;
- error or partial-data state;
- trend only when enough points exist;
- drill-down destination;
- accessible text equivalent.

Do not use green for neutral “up” or red for neutral “down.” Direction is only good or bad relative to metric semantics.

## Honest-axis checklist

- Bars begin at zero.
- Log scales are conspicuously labeled and justified.
- Time axes preserve real intervals.
- Missing periods remain visible rather than connected as fact.
- Forecasts and incomplete buckets are visually distinct.
- Compared panels share domain unless the difference is explicitly signposted.
- Reference lines name the source of a target or threshold.
- Percent rates never exceed logical bounds unless the metric permits it.

## Accessibility contract

For each visualization:

1. Add a concise title that states the question or takeaway.
2. Add a textual summary of important values, trend, scope, and anomalies.
3. Provide a semantic data table or equivalent structured detail where useful.
4. Make focus order predictable and marks keyboard-operable when interactive.
5. Expose selection state and tooltip content to assistive technology.
6. Avoid auto-updating announcements for every realtime point; announce meaningful state changes only.
7. Honor reduced motion and avoid flashing.
8. Keep body/dashboard text at or above the project floor and meet WCAG AA contrast.

## Performance guide

Approximate starting points, subject to measurement:

- Up to about 1,000 marks: SVG.
- About 1,000–50,000 marks: canvas, aggregation, virtualization, or progressive rendering.
- Above about 50,000 marks: WebGL or server/client aggregation.

Treat these as hypotheses. Measure render, interaction, memory, resize, update, and teardown costs on target hardware.

### Streaming visuals

- Batch frequent updates to animation frames or bounded intervals.
- Coalesce superseded values.
- Bound in-memory points and DOM nodes.
- Pause expensive rendering when hidden.
- Preserve a stable y-domain when auto-scaling would cause perceptual jitter.
- Distinguish “latest received” from “latest durable.”

## Review rubric

Score each 0–2:

| Dimension | 0 | 1 | 2 |
|---|---|---|---|
| Question fit | No question | Weak fit | Direct fit |
| Encoding accuracy | Misleading | Acceptable | Perceptually optimal |
| Semantic context | Missing | Partial | Units/window/source/freshness clear |
| Accessibility | Color/hover only | Partial fallback | Keyboard, text, table, contrast complete |
| Data quality | Hidden | Some indicators | Null/partial/late/uncertainty explicit |
| Performance | Demo only | Sampled | Production volume measured |
| Actionability | Decorative | Informative | Clear drill-down/action |

Require no zero and a total appropriate to product risk.

## Sources and provenance

Use only repositories meeting the 5+ stars and/or forks threshold:

- `grafana/grafana` — production dashboard visualization, variables, drill-down, alerting, correlations, and panel patterns: https://github.com/grafana/grafana
- `apache/superset` — broad chart catalog, dashboard filtering, cross-filtering, caching, and drill-to-detail patterns: https://github.com/apache/superset
- `d3/d3` — low-level visual encoding, scales, shapes, interactions, and data transformation: https://github.com/d3/d3
- `vega/vega-lite` — declarative grammar of interactive graphics and systematic encoding: https://github.com/vega/vega-lite
- `observablehq/plot` — concise grammar-oriented exploratory visualization used by the Hermes frontend: https://github.com/observablehq/plot
- `incluud/accessible-astro-dashboard` — accessible shell and navigation patterns: https://github.com/incluud/accessible-astro-dashboard

Role-derived guidance was refactored from `engineering-data-visualization-engineer.md` in `agency-agents`. Validate current library APIs through authoritative documentation before implementation.
