# Store, product and delivery optimization

Separate mandatory submission requirements from experiments and engineering recommendations. Optimization must not introduce misleading claims, unnecessary tracking or inaccessible flows.

## Metadata and creative assets

Use current field specifications rather than an old template. The inspected Apple documentation specifies a name/subtitle of up to 30 characters, description up to 4,000 characters and promotional text up to 170 characters. Metadata mutability differs by field and app status. Screenshot/device requirements must be read for the actual supported families. [S11](sources.md#s11), [S12](sources.md#s12)

The keyword field has a documented unit discrepancy: the detailed field reference says **100 bytes**, while the product-page guide says **100 characters**. Prefer a conservative UTF-8 byte check, especially for non-Latin locales, and verify current App Store Connect behavior. Do not silently describe the two limits as equivalent.

Recommended asset workflow:

1. Define the main user need and the actual first-value experience; derive truthful positioning from shipped behavior.
2. Build a locale/device asset matrix. Capture real release-candidate UI with synthetic content; validate dimensions, localization and legibility against current specifications.
3. Make the first visible assets communicate the main benefit. Keep claims and terminology consistent with the app, subscriptions and available features.
4. Check clipping, text density, language expansion, contrast and content readability on a small display. Validate accessibility claims against actual tested support rather than marketing intent.
5. Maintain source assets and metadata in version control where appropriate, but exclude personal data and secrets. Revalidate after UI, pricing or privacy changes.

Localize search intent and screenshots, not only individual words. Avoid irrelevant terms, unauthorized trademarks, competitor names and duplicated keyword terms. Promotional text is not a keyword-ranking field. [S12](sources.md#s12)

## Controlled acquisition experiments

Use Product Page Optimization only where its current platform/asset eligibility supports the hypothesis. Define a primary outcome, guardrail, observation window and stopping rule before launch. Change a small, coherent treatment rather than rewriting every asset simultaneously. Interpret uncertainty and audience mix; a short-lived uplift is not a universal causal result. [S13](sources.md#s13)

Consider Custom Product Pages for clearly different campaign/audience intents. Preserve consistency between the campaign promise, product page and in-app destination; verify the current link/deep-link and review requirements. [S14](sources.md#s14)

Recommended measurement contract:

`storefront exposure -> product-page view -> download -> first meaningful value -> retained use -> paid conversion (when relevant)`

Do not merge store conversion, onboarding completion and retention into one metric. Record denominator, attribution window, source, version and locale. Use minimal event attributes and consent-aware collection; store-level aggregate tools may suffice for some questions. Never log raw user content merely to gain broader analytics.

Do not buy or manipulate reviews, incentivize positive ratings or suppress feedback through deceptive flows. Evaluate review requests in the context of the current Apple policy and platform API.

## Runtime quality as conversion protection

These are recommended engineering checks, not universal Apple performance thresholds:

- Measure cold/warm start and the time to the app's first meaningful usable screen on representative real devices.
- Trace main-thread stalls, hangs, memory growth, scrolling and energy-intensive background work; optimize measured bottlenecks rather than speculative rewrites.
- Compare download/install footprint and dependency cost. Remove unused assets/SDKs where safe; retain evidence that feature behavior and declarations still agree.
- Exercise poor connectivity, interruption, authentication recovery and purchase recovery. A polished product page cannot compensate for a broken first session.
- Test VoiceOver, text scaling, contrast, reduced motion, focus/navigation and relevant input methods. Keep platform- and device-specific evidence separate.

Set budgets from the actual product and baseline. Preserve privacy-safe release labels and symbolication so regressions can be diagnosed without collecting sensitive payloads.

## Pipeline and review efficiency

Automate repeatable checks: metadata lengths, UTF-8 keyword size, internal links, asset matrix coverage, dependency/toolchain identity and candidate evidence completeness. Cache deterministic inputs while keeping signing secrets isolated. Reuse an immutable tested artifact when supported.

Reduce review friction with accurate notes, working synthetic access, stable services and a concise explanation of unusual functionality. Do not trade away safety, privacy or correctness to shorten review preparation. Track elapsed time by stage to find the bottleneck rather than assuming App Review is always the cause.

## Completion criteria

A proposed optimization has a baseline, hypothesis, scope, success measure, guardrail and reversible implementation. Report what was measured versus merely proposed; do not promise ranking, approval, conversion uplift or revenue.
