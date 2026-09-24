---
name: digital-advertizer
description: Run the end-to-end digital advertising lifecycle (strategy → build → launch → optimize → report) across Google Ads (Search/Shopping/Performance Max/YouTube), Google AdSense (publisher monetization), and Yandex Direct, using minimum necessary clarifying questions and producing platform-ready artifacts (keywords/negatives, structures, ads, tracking plan, change log).
metadata:
  category: marketing-performance
  scope:
    platforms:
      - Google Ads
      - Google AdSense
      - Yandex Direct
    regions:
      - Global (EN-first)
      - RU/CIS (Yandex-focused)
  artifacts:
    - campaign_plan.md
    - keyword_map.csv
    - negatives.csv
    - ad_copy_matrix.csv
    - tracking_plan.md
    - change_log.csv
---

# Digital Advertizer (end-to-end)

## Purpose

Execute an end-to-end, operations-first workflow to plan, build, launch, and continuously optimize paid digital advertising.

Produce outputs that are immediately implementable by a marketer (copy/paste into UI) or translatable to ad platform APIs (structured tables + explicit settings and assumptions).

## When to use

Trigger when the request involves any of:

- Building or optimizing PPC / performance marketing campaigns.
- Selecting channels/campaign types (Search, Shopping, Performance Max, YouTube; plus Yandex Direct equivalents).
- Keyword research, negative keywords/minus-words, query mining, or account/campaign/ad group structure.
- Writing compliant ad copy, extensions/assets, and creative variant plans.
- Tracking/measurement setup (UTMs, conversion events, offline conversions, consent-mode constraints).
- Continuous optimization and reporting with change logging.

## Operating principles (treat ads as a production system)

1) Treat auction performance as a combination of economic inputs and quality inputs.
   - Use platform framing of auction ranking to guide operations (bid + quality + context + assets).
   - Reference: Ad Rank definition emphasizes multiple factors including bid, quality, context, and expected impact of assets/ad formats. [Source: Google Ads Help, Ad Rank definition](https://support.google.com/google-ads/answer/1752122?hl=en)

2) Treat measurement quality as a first-class constraint.
   - Avoid optimizing to broken conversion signals.
   - Document modeled vs observed measurement where consent constraints apply. [Source: Google Ads Help, About consent mode](https://support.google.com/google-ads/answer/10000067?hl=en)

3) Treat policy/compliance as reliability engineering.
   - Avoid discontinuous failures (disapprovals, limits, suspensions).
   - Reference: misrepresentation policy aims for ads that are clear and honest; avoid deceptive practices/omissions. [Source: Google Advertising Policies, Misrepresentation](https://support.google.com/adspolicy/answer/6020955?hl=en)

4) Ask only the minimum necessary clarifying questions.
   - If critical inputs are missing, ask narrowly.
   - Otherwise proceed with best-practice defaults and explicitly list assumptions.

## Minimal clarifying questions (ask only if missing)

Ask **only** the smallest set needed to avoid unsafe or non-actionable output.

Critical questions (ask if unknown):

1) Business goal and target KPI: awareness, leads, sales, ROAS/CPA, pipeline revenue.
2) Geo + language: countries/regions; EN-only vs multilingual (include RU/CIS?).
3) Budget constraint: daily/monthly; acceptable CPA/ROAS bounds.
4) Conversion definition: what counts as a conversion; lead qualification rules; offline outcome availability.
5) Restricted category risk: healthcare/finance/politics/adult; any compliance constraints.

Optional questions (skip unless needed):

- Existing account history and what can be changed (new build vs optimize existing).
- Product feed availability (Shopping/PMax), video availability (YouTube), creative production constraints.

## Inputs (ingest and analyze)

Accept inputs in any format; normalize them into a structured brief:

- Product/offer details: value prop, pricing, differentiators, proofs, objections.
- Landing pages: URLs, page copy, form fields, speed/UX notes.
- Creative assets: existing ad copy, images, videos, brand voice.
- Past performance: spend, impressions, CTR, CPC, CVR, CPA, ROAS, AOV/LTV, impression share, search terms, placement reports.
- Audience insights: personas, segments, geo/language, device split, time-of-day patterns.
- Constraints: budget, legal claims, prohibited terms, brand safety, competitor bidding rules.

## Workflow (run in order)

### Step 1 — Build the “Campaign Readiness Brief”

Do:

1) Extract objectives and define success metrics.
2) Define primary KPI + guardrails.
3) Classify funnel intent tiers (high-intent bottom-funnel vs mid vs upper).
4) Identify policy risk areas and prohibited claims.
5) List assumptions explicitly if any inputs are missing.

Output:

- A short “Readiness Brief” section in `campaign_plan.md`.

### Step 2 — Select platforms and campaign types

Decide channel mix by intent, assets, and measurement maturity.

Minimum decision set:

- If the goal is high-intent capture and landing pages are strong → prioritize Search.
- If there is a product feed and purchase goals → include Shopping / Performance Max.
- If there is strong video and reach goals → include YouTube.
- If RU/CIS market is primary/important → include Yandex Direct as a parallel system.

Document the reason for each channel and the KPI it optimizes.

### Step 3 — Create the measurement + tracking plan

Do:

1) Define conversion events (primary + secondary).
2) Define attribution assumptions and limitations.
3) Define UTM taxonomy.
4) Define offline conversion loop if applicable.

Evidence anchors:

- Respect identifier retention constraints in offline conversion operations.
  - Quote: “We only keep the GCLID for 90 days.” [Source: Google Ads Help, Fix discrepancies and errors in offline conversion imports](https://support.google.com/google-ads/answer/13321563?hl=en)
- Treat consent constraints and modeled conversions as part of readiness. [Source: Google Ads Help, About consent mode](https://support.google.com/google-ads/answer/10000067?hl=en)

Output:

- `tracking_plan.md` (events, UTMs, QA checklist, attribution notes).

### Step 4 — Keyword research and intent mapping (Search + Yandex)

Do:

1) Build a keyword universe grouped by intent:
   - Brand
   - Competitor
   - Category / generic
   - Problem/solution
   - “Alternatives” and “vs” queries
2) Create an initial negatives/minus-words list.
3) Define query mining cadence and “promotion rules” (what becomes a keyword, what becomes a negative).

Yandex-specific anchors:

- Use minus-words as a first-class control; use platform-supported workflows and operators to refine exclusions. [Source: Yandex Direct Help, Negative keywords](https://yandex.com/support/direct/en/keywords/negative-keywords)

Output:

- `keyword_map.csv` (columns: theme, intent, keyword, match_type, landing_page, notes)
- `negatives.csv` (columns: scope, negative_term, rationale, added_date)

### Step 5 — Audience targeting and exclusions

Do:

1) Define geo/language targeting and exclusions.
2) Define device strategy (mobile vs desktop) based on funnel stage and UX.
3) Define remarketing / customer match usage only if allowed and safe.
4) Define brand safety and placement exclusions where applicable.

Policy anchors:

- Avoid sensitive-health targeting; treat policy updates as hard constraints. [Source: Google Advertising Policies Help, Personalized advertising update (May 2025)](https://support.google.com/adspolicy/answer/16258024?hl=en)

### Step 6 — Design account structure (campaigns → groups → ads)

Do:

1) Choose a structure that matches business boundaries:
   - Separate by goal (leads vs sales) and by major geo/language.
   - Separate brand vs non-brand.
2) Keep each ad group/theme aligned to one intent cluster and one landing page narrative.
   - Reference: themed ad group organization guidance. [Source: Google Ads Help, Organize your account with ad groups](https://support.google.com/google-ads/answer/6372655?hl=en)

Output:

- A table in `campaign_plan.md` describing campaigns and ad groups, settings, budgets, KPIs.

### Step 7 — Write ad copy + extensions/assets (compliant + on-brand)

Do:

1) Produce an “ad copy matrix”:
   - Multiple headlines/descriptions per intent cluster.
   - At least one variant focusing on: value, proof, risk reversal, urgency (if allowed), differentiation.
2) Produce extensions/assets plan:
   - Sitelinks, callouts, structured snippets, images where relevant.
3) Apply compliance gates:
   - Remove deceptive, unverifiable, or misleading claims.

Evidence anchors:

- Treat RSA asset flexibility as performance lever and avoid over-pinning.
  - Quote: “It’s recommended to have one responsive search ad per ad group with at least ‘Good’ or ‘Excellent’ Ad Strength.” [Source: Google Ads Help, About responsive search ads](https://support.google.com/google-ads/answer/7684791?hl=en)
  - Quote: “Pinning reduces the overall number of headlines or descriptions that can be shown. Therefore, the less you pin, the more combinations you can create.” [Source: Google Ads Help, Ad strength for responsive search ads](https://support.google.com/google-ads/answer/9921843?hl=en)

Output:

- `ad_copy_matrix.csv` (campaign, ad_group, headline_1..N, description_1..N, pinned_assets, compliance_notes)

### Step 8 — Configure budgets, bidding, and safeguards

Do:

1) Set budgets by goal priority and marginal ROI expectations.
2) Choose bidding strategy consistent with conversion maturity.
3) Configure geo/device/daypart settings if justified by data; otherwise avoid premature micro-optimizations.
4) Configure spend safeguards:
   - Daily spend caps where possible.
   - Alerts for spend spikes and conversion drops.

### Step 9 — Launch checklist (QA + governance)

Do:

1) Validate tracking end-to-end.
2) Validate policy compliance of ads and landing pages.
3) Confirm negative keyword coverage for obvious mismatches.
4) Document initial settings as baseline.

Output:

- “Launch QA checklist” section in `campaign_plan.md`.
- Initialize `change_log.csv` with baseline snapshot.

### Step 10 — Monitoring, diagnosis, and optimization loop

Run a fixed cadence:

Daily:

- Check spend pacing and major metric breaks (CTR/CVR/CPC/CPA/ROAS).
- Check query drift and add negatives/minus-words.
- Check lead quality signals if lead-gen.

Weekly:

- Reallocate budget by marginal returns.
- Refresh creative and rotate variants.
- Promote search terms to keywords and exclude irrelevancies.

Monthly:

- Structural changes (consolidate or split only with a hypothesis).
- Measurement audits (event definitions, offline import completeness, consent modeling changes).

Evidence anchors (lead quality and invalid traffic):

- Implement lead-quality controls such as server-side validation; treat data integrity as operational mitigation. [Source: Google Ads Help, Managing invalid traffic](https://support.google.com/google-ads/answer/11182074?hl=en)

### Step 11 — Experimentation and learning

Do:

1) Define one hypothesis per experiment (bidding vs targeting vs creative vs landing page).
2) Record expected direction, metric, and minimum detectable effect.
3) Use platform experiment tools where available.

Evidence anchor:

- Use published experiment methodology notes as a reminder to respect statistical uncertainty. [Source: Google Ads Help, Statistical methodology behind experiments](https://support.google.com/google-ads/answer/9232676?hl=en)

### Step 12 — Reporting, forecasting, and change logging

Do:

1) Produce a weekly report with:
   - What changed (from change log)
   - What happened (metrics)
   - Why it likely happened (diagnosis)
   - What to do next (actions + expected impact)
2) Maintain a change log as an audit trail.
   - Reference: Google change history stores changes for the past 2 years; use it as an external control log where possible. [Source: Google Ads Help, About change history](https://support.google.com/google-ads/answer/19888?hl=en)

Output:

- `campaign_plan.md` (rolling doc)
- `change_log.csv` (date, entity, change, reason, expected impact, owner)

## AdSense sub-skill (publisher monetization)

If the input involves AdSense publishing, run a parallel workflow:

1) Verify AdSense program policy compatibility.
2) Optimize placement for UX and accidental-click prevention.
   - Reference: Ad placement policies warn about placing UI elements (links/buttons/players/menus) near ads. [Source: Google AdSense Help, Ad placement policies](https://support.google.com/adsense/answer/1346295?hl=en)
3) If unusual/invalid traffic is detected, act immediately.
   - Quote: “If you find traffic to be unusual, invalid or low performing, stop acquiring the traffic immediately and remove the ad code from pages that are impacted.” [Source: Google AdSense Help, Site optimization best practices](https://support.google.com/adsense/answer/2661562?hl=en)

## RU/CIS notes (Yandex Direct)

1) Treat selection logic as bid + predicted CTR/quality.
   - Quote: “Select the best ad by CTR, quality coefficient, and bid per click.” [Source: Yandex Direct Help, Campaign parameters](https://yandex.com/support/direct/en/campaigns/campaign-settings)
2) Treat Metrica goals and Conversion Center feeds as the measurement spine.
   - Reference: conversion center sends data to Metrica for conversions/goals and optimization. [Source: Yandex Direct Help, Conversion center](https://yandex.com/support/direct/statistics/conversions.html)
3) Use autotargeting for fast launch only with disciplined exclusions.
   - Reference: educational material notes ability to run search ads without keywords via autotargeting. [Source: Yandex Advertising Education, Create an ad group](https://yandex.com/adv/edu/direct/direct-start/create-an-ad-group)

## Output format requirements

Always produce:

1) `campaign_plan.md` with:
   - Objectives + KPIs
   - Channel and campaign-type selection
   - Account structure
   - Budget and bidding plan
   - Safeguards
   - Launch checklist
   - Optimization cadence
2) `keyword_map.csv`, `negatives.csv`
3) `ad_copy_matrix.csv`
4) `tracking_plan.md`
5) `change_log.csv` (initialized)

Use templates in [output templates](references/output-templates.md).

