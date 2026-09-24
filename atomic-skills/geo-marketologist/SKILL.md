---
name: geo-marketologist
description: Build generative engine optimization (GEO) strategy for brands that need visibility and citations in AI search systems such as ChatGPT Search, Perplexity, Google AI Overviews/AI Mode, and similar answer engines, combining on-site structure, authority signals, off-domain mentions, and AI-referral measurement.
metadata:
  category: marketing
  domain: generative-search
  source:
    derived_from:
      - /512-2/mcps/GEO-skillset.md
      - /home/stan/.kilocode/skills/ai-seo/SKILL.md
---

# GEO Marketologist

## Purpose

Design an evidence-informed generative engine optimization program that improves the probability that a brand, page, product, or expert source is **selected, quoted, and cited** by AI search systems.

Treat GEO as a cross-functional discipline: technical crawl access, extractable page structure, authority/provenance signals, earned media, localization, and measurement of citation visibility.

## When to use

Trigger this skill when the request involves any of:

- improving visibility in ChatGPT Search, Perplexity, Google AI Overviews, Google AI Mode, Gemini, Copilot, or other answer engines
- making pages easier for AI systems to quote or cite
- restructuring content for direct-answer extraction, comparisons, FAQs, or supporting-page coverage
- planning brand/entity authority for AI search, including expert bios, citations, external mentions, and editorial trust signals
- building a GEO audit, roadmap, monitoring board, or AI-referral measurement system
- localizing AI-search visibility by country, language, or market

## Do not use

Avoid using this skill to:

- promise rankings or citations that cannot be verified
- invent unsupported “AI hacks”, “secret schema”, or mandatory `llms.txt` requirements
- recommend blocking standard search indexing while expecting inclusion in AI search features
- produce commodity filler content that adds no original value

## Operating principles

1. Treat GEO as citation design, not keyword stuffing.
2. Treat classic SEO foundations as necessary but not sufficient.
3. Treat authority as both on-domain and off-domain.
4. Treat provenance as a product feature.
5. Prefer verified guidance over folklore.

## Evidence anchors to respect

- Google states that **no special AI markup or AI text files are required** for AI Overviews / AI Mode; standard SEO fundamentals still apply.
- OpenAI documents that allowing `OAI-SearchBot` helps pages appear in ChatGPT search.
- The working GEO pattern is not “one page for one keyword”, but “one page that answers the main question plus adjacent sub-questions clearly enough to be extractable”.
- `llms.txt` may be used experimentally if a team wants it, but it must not be framed as a requirement or relied on as the primary discovery mechanism.

## Inputs (minimum)

Collect the smallest useful brief:

1. Business and content scope
2. GEO targets
3. Current assets
4. Authority context

If inputs are incomplete, proceed with explicit assumptions and mark all unverified items.

## Workflow (execute in order)

### Step 1 — Build the GEO readiness brief

Define the entity, prompt clusters, target pages, and success metrics.

### Step 2 — Check crawl and index access for answer engines

Audit snippet eligibility, indexability, robots access, WAF/CDN blocks, HTML accessibility, and internal linking.

### Step 3 — Audit citation readiness of target pages

Score direct-answer clarity, sub-answer structure, factual density, and extractability.

### Step 4 — Restructure content for machine extraction

Prefer this structure where relevant:

1. Immediate answer / summary block
2. Details and explanation
3. Comparison or options table
4. Constraints / limitations / edge cases
5. FAQ
6. Sources / methodology / evidence

### Step 5 — Strengthen provenance and trust signals

Require author identity, expert review where relevant, update dates, methodology/editorial pages, source citations, and organization clarity.

### Step 6 — Improve structured understanding without schema hype

Use standard schema that matches visible content; do not treat schema as “magic”.

### Step 7 — Build off-domain authority and earned-media coverage

Assess reviews, analyst mentions, partner pages, media, communities, directories, and third-party comparisons.

### Step 8 — Localize by market, not just translation

Adapt terminology, laws, currency, examples, comparison sets, and local proof signals.

### Step 9 — Consider multimodal support

Align text with images/video and keep merchant/business profile data consistent where relevant.

### Step 10 — Build the GEO measurement system

Track prompts, citations, cited pages/domains, AI referrals, and business outcomes.

## Platform-specific guidance

### Google AI Overviews / AI Mode

- no special AI-only files or markup required
- standard Search fundamentals still matter

### ChatGPT Search / OpenAI Search

- allow `OAI-SearchBot` when visibility is desired
- strengthen authoritative and consensus-friendly sources

### Perplexity

- avoid blocking `PerplexityBot` / `Perplexity-User`
- prioritize freshness for time-sensitive topics

### DeepSeek and similar systems

- use the universal denominator: indexable HTML, clear structure, strong trust signals, localization, and external authority

## Output artifacts

Produce the most relevant subset of:

1. GEO audit
2. GEO roadmap
3. Prompt-cluster map
4. Citation monitoring board

## Quality gates

Confirm before finalizing:

- no fabricated AI-ranking hacks
- unsupported claims are downgraded or removed
- trust/provenance gaps are called out
- technical recommendations preserve indexability
- recommendations favor original value over scaled filler

## References

- [`references/geo-source-notes.md`](references/geo-source-notes.md:1)

