---
name: medical-marketologist
description: Develop compliant acquisition and conversion strategy for medical services and digital health products via websites (trust UX, content/SEO, patient journey CRO, and ads-policy-safe messaging).
metadata:
  category: business-marketing
  domain: healthcare
  source:
    derived_from: healthpilot/TOR_Medical_Promotion_Best_Practices.md
---

# Medical Marketologist (Website Promotion)

Base the workflow on [`healthpilot/TOR_Medical_Promotion_Best_Practices.md`](healthpilot/TOR_Medical_Promotion_Best_Practices.md:1).

## Purpose

Design an evidence-informed, **policy-safe** website promotion system that converts visitors into patients/users for medical services and consultations, without unsafe medical claims.

## Trigger / when to use

Use this skill when needing to:

- audit or design a medical / digital health website funnel (landing → booking)
- improve “medical trust” UX blocks (doctors, credentials, privacy, proof)
- build an SEO/content engine for symptom-led and solution-led demand
- design CRO flows for intake, booking, pricing presentation, and follow-up
- run compliant acquisition experiments under Google Ads / Meta Ads constraints

## Do not use

Avoid using this skill to:

- provide medical diagnosis, treatment advice, or personal health recommendations
- write copy that guarantees outcomes (e.g., “cures”, “reverses”, “100%”, “no risk”)
- propose targeting people by sensitive health attributes for ads or retargeting

## Safety & compliance guardrails

Apply these constraints throughout:

- Exclude personal data and patient-identifiable details.
- Avoid sensitive-attribute targeting and “creepy” personalization.
- Prefer educational framing and “consultation-first” flows over condition-claim hooks.
- Require substantiation for any claim; if substantiation is missing, mark it as **needs substantiation** and rewrite into a non-claim.

Policy entry points (keep up to date):

- Google Ads policies: https://support.google.com/adspolicy
- Meta advertising policies: https://www.facebook.com/policies/ads/

## Inputs (minimum)

Collect:

1. Offer definition
   - service lines (what is being sold)
   - consultation format (chat/video/in-person)
   - regions/markets (e.g., Tier 1 vs Tier 2 in the TOR)

2. Operational constraints
   - available clinicians capacity, response-time SLA, opening hours
   - pricing model (pay-per-visit, bundles, subscription)
   - legal/compliance requirements by market (if known)

3. Current funnel baseline (if available)
   - traffic sources mix
   - conversion steps and drop-offs
   - top landing pages and top queries

If critical inputs are missing, proceed with explicit assumptions and flag them.

## Workflow (execute in modules A–D)

### Module A — Trust & credibility (“medical trust”)

1. Inventory trust elements on the website
   - clinician profiles, credentials, affiliations
   - identity verification, licensing statements (if applicable)
   - social proof handling (reviews/testimonials/case stories)
   - privacy/security communication

2. Audit for trust “friction”
   - unclear provider identity
   - unclear scope of consultation vs emergency care
   - unclear data handling / consent
   - over-claiming outcomes

3. Produce outputs
   - trust block checklist
   - prioritized UX fixes (effort × impact)

Template to copy and fill:

- [`ux-trust-audit-checklist.template.md`](.kilocode/skills/medical-marketologist/assets/templates/ux-trust-audit-checklist.template.md:1)

### Module B — Content strategy & SEO

1. Map demand by intent
   - symptom-led queries (high intent, high compliance risk)
   - solution-led queries (lower risk, broader education)
   - “longevity/wellness optimization” framing where appropriate (see TOR)

2. Design content system
   - education hub / encyclopedia pages
   - comparison pages (services, modalities, programs)
   - lead magnets (risk checks, calculators, symptom-to-education flows)
   - explainer video plan for complex topics

3. Specify measurement
   - organic sessions, qualified leads, booking rate
   - content-to-consultation assist metrics

Template to copy and fill:

- [`content-seo-cluster-map.template.md`](.kilocode/skills/medical-marketologist/assets/templates/content-seo-cluster-map.template.md:1)

### Module C — CRO for health (patient journey)

1. Map the journey from landing to booking
   - first-touch landing → CTA → intake → scheduling → confirmation
   - identify “trust gates” where users need reassurance

2. Design conversion mechanics
   - CTA strategy (book, free triage, educational check)
   - intake pattern selection: chatbot vs form vs call
   - pricing presentation: transparent ranges + what’s included
   - no-show reduction: reminders + value reinforcement

3. Design ethical follow-up
   - use educational retargeting and neutral reminders
   - avoid condition-revealing ad copy

Template to copy and fill:

- [`patient-journey-cro-blueprint.template.md`](.kilocode/skills/medical-marketologist/assets/templates/patient-journey-cro-blueprint.template.md:1)

### Module D — Compliance & ethics in promotion

1. Build “safe claim” rules
   - convert outcome claims into process/value claims
   - insert disclaimers in proximity to the relevant promise
   - never imply a diagnosis or guaranteed result

2. Review every marketing claim and creative
   - detect policy risks
   - rewrite into compliant variants

Template to copy and fill:

- [`compliance-claims-review.template.md`](.kilocode/skills/medical-marketologist/assets/templates/compliance-claims-review.template.md:1)

## Channel patterns (from the TOR)

Use only if compliant for the market and platform:

- Messaging education funnels (WhatsApp/Telegram) for “educational nudge” distribution
- Referral waitlists and non-monetary incentives (exclusive expert content, social spotlight)
- “Expert-as-a-brand” content loops on LinkedIn (authority + trust)
- Local community growth + localized multilingual content

Reference summary:

- [`tor_summary.md`](.kilocode/skills/medical-marketologist/references/tor_summary.md:1)

## Outputs (produce these artifacts)

Generate:

1. Best-practices playbook (Do/Don’t + rationale)
   - Use template: [`medical-website-promo-playbook.template.md`](.kilocode/skills/medical-marketologist/assets/templates/medical-website-promo-playbook.template.md:1)
2. UX/UI swipe-file plan (what to capture, how to tag)
3. Feature wishlist (must-have website features, prioritized)
4. Marketing funnel blueprint (traffic → content → conversion → follow-up)
5. Experiment backlog (A/B tests + guardrails)

## Quality gates (before finalizing)

Confirm:

- Every claim is either substantiated or rewritten as non-claim guidance.
- Disclaimers exist where needed and are not hidden.
- The funnel clearly indicates emergency limitations (e.g., not for emergencies).
- Retargeting guidance remains ethical and non-revealing.

