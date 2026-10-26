# Meta-skills: plain-search-compatible two-level discovery

## Agent runtime (no scripts and no MCP required)

Only `skills/meta-*/SKILL.md` are visible to first-level skill discovery.
Each is a standard Agent Skill with YAML `name` and `description`.
Read the chosen meta `SKILL.md`, inspect its local `references/members.md`
using ordinary file search, then open the selected atomic skill's full
`SKILL.md`. Repeat for separate subtasks; load 1–3 atomic skills at a time.
A search result excerpt or the one-line catalog entry is not sufficient.

**Resolve relative paths from the directory containing the file that
mentions them**, not from the repository root, except for explicitly
repository-root-relative paths shown in the root README.

| File that contains the path | Correct relative atomic root |
| --- | --- |
| `README.md` or `README.legacy.md` (repository root) | `atomic-skills/` |
| `docs/metaskills.md` (this file) | `../atomic-skills/` |
| `skills/meta-*/SKILL.md` | `../../atomic-skills/` |
| `skills/meta-*/references/members.md` | `../../../atomic-skills/` |
| `skills/meta-specialist-catalog/references/legacy-names.md` | `../../../atomic-skills/` |

For example, a meta instruction at
`../skills/meta-agent-systems/SKILL.md` uses
`../../atomic-skills/agent-evals-lab/SKILL.md`, while a child-catalog
entry inside `../skills/meta-agent-systems/references/members.md` uses
`../../../atomic-skills/agent-evals-lab/SKILL.md`. Both resolve to the
same existing atomic file. A known atomic file can also be opened from
this documentation directory as
`../atomic-skills/agent-evals-lab/SKILL.md`.

For an explicitly named old skill, search the static registry at
`../skills/meta-specialist-catalog/references/legacy-names.md`.
Its entries, like the ordinary child catalogs, are relative to the
registry's own `references/` directory and begin with
`../../../atomic-skills/`.

## Visibility and limits

All original atomic skills and their relative resources are preserved
under the repository-root `atomic-skills/` directory. First-level
discovery must enumerate only repository-root `skills/`. A global
repository `**/SKILL.md` search will also find the atomic files;
the directory convention is not an access-control mechanism.
No agent-time CLI, Python, MCP server or embedding service is needed.

Moving old atomic directories changes hard-coded repository-root paths
from `skills/<original-path>/...` to
`atomic-skills/<original-path>/...`. Existing original frontmatter
names, original skill bodies and relative bundled resources are intact.

## Taxonomy and maintenance

Domain memberships and name registry are static Markdown. Some atomic
skills appear in two meta domains. The unmatched set remains in
`meta-specialist-catalog`. After any catalog change, the CI-only
validator resolves **every** referenced child file from its containing
catalog's directory and verifies the first-level visibility boundary.
This is a filesystem-based semantic taxonomy, not a claim of measured
token savings or perfect routing quality.

## Software simplicity routing

Overengineering, architecture/code bloat, Lean, KISS, YAGNI, AHA,
«оверинжиниринг» and «раздувание кода» route through
[meta-software-architecture](../skills/meta-software-architecture/SKILL.md).
Select by deliverable rather than loading the complete set:

| Deliverable | Atomic skill | Owning meta-skills |
| --- | --- | --- |
| Minimal adequate architecture | [design-minimal-architecture](../atomic-skills/design-minimal-architecture/SKILL.md) | meta-software-architecture, meta-backend-services |
| Behavior-preserving structural simplification | [simplify-code-structure](../atomic-skills/simplify-code-structure/SKILL.md) | meta-software-architecture, meta-backend-services |
| Evidence-based obsolete-code removal | [remove-obsolete-code](../atomic-skills/remove-obsolete-code/SKILL.md) | meta-software-architecture, meta-devops-cloud |
| Independent complexity review | [review-change-complexity](../atomic-skills/review-change-complexity/SKILL.md) | meta-software-architecture, meta-testing-quality |

The corresponding member catalogs and exact-name registry contain all four
canonical paths. `meta-agent-systems` links to the architecture route for
AI-generated and multiagent bloat without adding a third membership. General
architecture design, antipattern audits and code review retain their existing
scope and hand off only when focused simplification work is requested.

### Ponytail-inspired methods (2026-10-26)

The methods extend existing skills; there is no new always-on persona, hook,
agent host requirement or first-level skill. Open the selected child first,
then only the reference needed for the current decision:

| Task | Canonical procedure |
| --- | --- |
| Choose the first complete sufficient solution | `design-minimal-architecture` or `simplify-code-structure`, using the shared [solution ladder](../atomic-skills/design-minimal-architecture/references/solution-ladder.md) |
| Review simplicity without trading away correctness | `review-change-complexity`, starting with its risk-first triage and connected consumers |
| Record or inventory temporary compromises | `remove-obsolete-code`, using the [shortcut ledger](../atomic-skills/remove-obsolete-code/references/shortcut-ledger.md); an inventory does not authorize deletion |
| Measure whether a coding skill helps | [agent-evals-lab](../atomic-skills/agent-evals-lab/SKILL.md), using the [comparison protocol](../atomic-skills/agent-evals-lab/references/skill-comparison.md) and [case specifications](../atomic-skills/agent-evals-lab/references/simplicity-cases.json) |

Comparative trials route through `meta-agent-systems` or `meta-testing-quality`.
[agent-skill-development](../atomic-skills/agent-skill-development/SKILL.md) links
to the same protocol rather than duplicating it. Atomic names and memberships
are unchanged, so the existing exact-name registry remains authoritative.
Case specifications and structural validation are not executed model trials;
report unrun evaluations instead of inheriting Ponytail's performance numbers.

## Apple Pay routing example

Apple Pay requests route through `meta-finance-payments` or `meta-mobile-desktop`. Their static catalogs select [apple-pay-integration](../atomic-skills/apple-pay-integration/SKILL.md); the exact-name registry lists both owners. Read its eligibility gate before web/native setup, then only the relevant processor and verification references. This is one portable atomic skill with two domain memberships, not a project-specific payment recipe or a new first-level meta-skill.

## Google Play release routing

Google Play publishing and release automation route through `meta-mobile-desktop` and `meta-devops-cloud` to [google-play-publishing](../atomic-skills/google-play-publishing/SKILL.md). Both member catalogs and the exact-name registry contain the canonical atomic path. The skill is not tied to a product, framework, publisher account or country; it selects only applicable policy modules. Its source snapshot is dated and must be refreshed before a submission. The [practical guide](guides/google-play-publishing.md) is for human readers. Maintainer structural tests do not constitute behavioral evaluation or Play approval.

## Apple App Store publishing route

The project-neutral [apple-app-store-publishing](../atomic-skills/apple-app-store-publishing/SKILL.md) atomic skill belongs to meta-mobile-desktop and meta-devops-cloud. Their child catalogs and the exact-name registry include it. Meta-security-compliance and meta-marketing-growth provide cross-domain routing without additional membership. Read the skill's references selectively; no runtime script or proprietary agent host is required.

## Google Pay integration routing

For Google Pay, GooglePay, GPay or «интеграция Google Pay», start with
[meta-finance-payments](../skills/meta-finance-payments/SKILL.md), or
[meta-mobile-desktop](../skills/meta-mobile-desktop/SKILL.md) for an Android,
Flutter, React Native or WebView entry point. Both catalogs route to
[google-pay-integration](../atomic-skills/google-pay-integration/SKILL.md).

The atomic skill contains a provider-neutral decision workflow, platform
instructions, secure server payment lifecycle, recurring/deferred/reload
payments, test/production gates, optimization, a dated primary-source ledger,
configuration and plan templates, and agent evaluation cases. Load only the
references needed for the selected surface and charge model. Google Pay is
not a shortcut around store billing rules, a Wallet pass API or an India UPI
integration. Project-specific settings belong in the consuming project's
plan, never in this shared skill.
