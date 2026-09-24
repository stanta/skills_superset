---
name: dashboard-data-visualization
description: This skill should be used when selecting, designing, implementing, or reviewing charts, KPI cards, tables, heatmaps, timelines, and visual encodings for dashboards. Apply it to match chart type to question and data shape, enforce perceptual honesty, accessible and color-safe presentation, uncertainty disclosure, responsive behavior, and rendering performance at production volume; do not use it as the primary skill for overall dashboard information architecture or AI-agent runtime semantics.
---

# Dashboard Data Visualization

## Purpose

Turn dashboard questions into truthful, quickly readable, accessible, and performant visual encodings. Treat perception and semantic correctness as prerequisites to styling or library choice.

Load `references/visualization-playbook.md` for chart-selection matrices, review rubrics, implementation guidance, and source provenance.

## Boundary

- Own chart type, encoding, axes, scale, color, labels, comparison, uncertainty, tooltips, data-table alternatives, responsive adaptation, and renderer choice.
- Defer dashboard audience, hierarchy, filters, actions, and page-state architecture to `dashboard-product-architecture`.
- Defer run/tool/evaluation semantics to `ai-agent-control-plane-dashboard`.
- Defer data transport and cache reconciliation to `dashboard-realtime-consistency`.
- Defer end-to-end release verification to `dashboard-quality-gates`.

## Workflow

### 1. State the question and expected reading

Write one sentence for each visual: “This visual lets <audience> determine <decision> from <measure> over <scope/time>.” Reject a chart with no specific reading.

Classify the task:

- current value or status;
- comparison or ranking;
- trend over time;
- distribution;
- relationship/correlation;
- composition;
- flow or sequence;
- schedule or lifecycle;
- anomaly or threshold detection.

### 2. Profile data before selecting an encoding

Inspect:

- categorical, ordinal, quantitative, temporal, and geographic fields;
- row count, cardinality, missingness, outliers, skew, and update rate;
- unit, grain, aggregation, timezone, and correction behavior;
- whether exact values, patterns, or both matter;
- expected desktop, narrow, print, export, and assistive-technology contexts.

### 3. Choose the most accurate encoding

Prefer:

- KPI/status card for one current value with target, context, freshness, and drill-down;
- sorted horizontal bars for categorical comparison;
- line or area with justified baseline for continuous time trends;
- histogram, box plot, or quantile bands for distributions;
- scatter plot for relationships;
- stacked bar for limited part-to-whole comparison;
- small multiples for many comparable groups;
- table for lookup, exact values, heterogeneous fields, and dense evidence;
- timeline/Gantt only when sequence or interval is the decision object.

Avoid pie/donut beyond a few unmistakable categories, gauges without meaningful thresholds, decorative maps, 3D, dual axes, and charts that merely restate a single number.

### 4. Enforce perceptual honesty

- Start bar axes at zero.
- Label non-zero line-chart baselines and justify the choice.
- Do not use area, volume, angle, or hue as the primary quantitative channel when position/length is available.
- Keep comparable panels on comparable scales.
- Show sample size, units, aggregation, and time window.
- Display uncertainty, late data, recovery, and partial coverage when material.
- Avoid averages that conceal multimodal distributions or tail risk.
- Never imply causation from correlation.

### 5. Use color as redundant semantics

- Match palette type to data: categorical, sequential, or diverging.
- Keep categorical hues limited and stable across surfaces.
- Pair status color with text, icon, shape, pattern, or position.
- Test contrast, deuteranopia, protanopia, grayscale, dark mode, and high-contrast mode.
- Reserve saturated colors for selection, exceptions, and high-priority action.

### 6. Design interaction and drill-down

- Make hover optional rather than necessary.
- Provide keyboard focus and equivalent detail for interactive marks.
- Keep tooltips concise: label, value, unit, timestamp, comparison, and data-quality note.
- Preserve current filters/time range in links.
- Expose reset and selection state.
- Use brushing/cross-filtering only when it clarifies a defined analytical task.
- Provide direct labels where legends force costly visual lookup.

### 7. Select renderer by real workload

Use SVG for modest mark counts and rich accessibility; canvas for thousands to tens of thousands of marks; WebGL or aggregation for larger sets. Validate with production cardinality, update rate, device class, and interaction patterns.

Apply aggregation or downsampling that preserves the claimed pattern. Document any loss of precision. Bound retained realtime points and transcript/event marks.

### 8. Define responsive and fallback behavior

For every visual specify:

- minimum useful width and height;
- label truncation/wrapping rules;
- stacking or conversion at narrow widths;
- touch and keyboard behavior;
- reduced-motion behavior;
- print/export rendering;
- textual summary and accessible table fallback;
- loading, empty, partial, stale, and error states.

### 9. Deliver a visual specification

Provide:

1. Question and audience.
2. Data contract and transformations.
3. Chart choice and rejected alternatives.
4. Encoding map and scale/axis rules.
5. Color and accessibility specification.
6. Interaction and drill-down behavior.
7. Responsive and fallback behavior.
8. Volume/performance budget.
9. Tests and acceptance criteria.

## Non-negotiables

- Let the question choose the chart.
- Never hide units, denominator, time range, timezone, or data quality.
- Never encode status or category by color alone.
- Keep a table or text alternative available where exact values matter.
- Test at real volume and with long labels, nulls, negative values, and extreme outliers.
- Prefer a simple accurate visual over a novel ambiguous one.

## Review gate

A visual is ready only when a fresh reader can state its intended takeaway quickly, the same meaning survives grayscale and keyboard use, the axis cannot exaggerate the result, and the production-size dataset remains responsive.
