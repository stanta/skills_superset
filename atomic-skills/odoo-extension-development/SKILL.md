---
name: orbitas-odoo-addon-development
version: "1.0.0"
description: Best-practice rules for designing, implementing, reviewing, testing and upgrading Odoo addons and ERP connectors, with an Orbitas integration profile.
license: Internal project guidance; upstream source references retain their own licenses.
---

# Orbitas Odoo Addon Development Skill

Use this skill whenever creating, changing, reviewing, testing, packaging or upgrading an Odoo addon, especially the Orbitas Odoo connector.

The skill is intentionally strict. Odoo modules run inside the ERP transaction and security model; a small shortcut in ORM, ACLs, multi-company handling or external synchronization can corrupt accounting data or expose another company's records.

## 1. Baseline and version discipline

Current reviewed baseline: **Odoo 19.x** documentation and conventions.

Before changing code:

1. Detect the target Odoo major version from the repository/manifest/branch.
2. Read documentation for that exact major version.
3. Do not mix examples from Odoo 16/17/18/19/master without verifying compatibility.
4. Keep separate major-version branches when supporting multiple Odoo majors; prefer explicit ports over dense compatibility conditionals.
5. Pin CI/lint/dependency tool versions to reviewed tags or lockfiles.

Odoo 19 is the reference baseline for this skill. Revalidate the skill before adopting Odoo 20/master APIs.

### Hosting constraint

A Python addon requires a deployment model that supports custom server modules, such as **Odoo.sh** or **on-premise**. Odoo Online does not support arbitrary custom Python modules. If the target is Odoo Online, use supported importable-module capabilities or an external integration instead of pretending a normal server addon can be installed.

## 2. Extension-first rule: never fork Odoo for normal customization

Prefer an addon over modifications to Odoo core.

Use extension mechanisms in this order:

1. Python model inheritance (`_inherit`) and narrow method overrides;
2. XML view inheritance;
3. registries/services/components on the frontend;
4. documented controller/API extension points;
5. JS `patch()` only when no stable extension point exists;
6. core fork only under an explicit architecture decision.

Do not copy an entire standard model/view/controller merely to change a small behavior. The more standard code copied, the larger the upgrade surface.

## 3. Standard addon layout

Prefer a predictable module tree:

```text
orbitas_odoo_connector/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── account_move.py
│   ├── res_company.py
│   ├── orbitas_connector.py
│   ├── orbitas_binding.py
│   └── orbitas_outbox.py
├── controllers/
│   ├── __init__.py
│   └── orbitas_odoo_connector.py
├── security/
│   ├── ir.model.access.csv
│   ├── orbitas_odoo_connector_groups.xml
│   └── orbitas_odoo_connector_security.xml
├── data/
│   └── orbitas_odoo_connector_cron.xml
├── views/
│   ├── account_move_views.xml
│   ├── res_company_views.xml
│   └── orbitas_connector_views.xml
├── wizard/
├── static/src/
│   ├── js/
│   ├── scss/
│   └── xml/
├── tests/
│   ├── __init__.py
│   ├── test_security.py
│   ├── test_sync.py
│   ├── test_multicompany.py
│   └── test_idempotency.py
└── migrations/
```

Rules:

- one inherited core model per clearly named file where practical;
- lowercase `[a-z0-9_]` filenames;
- keep security, data, views, tests and frontend assets in their conventional locations;
- never hide business logic in XML or controllers if it belongs in a model/service method.

## 4. Manifest discipline

`__manifest__.py` is part of the public contract of the addon.

- Declare only real dependencies in `depends`.
- Keep data-file load order deterministic: groups/security before dependent views/actions.
- Declare assets through the manifest `assets` key.
- Declare external Python dependencies explicitly in deployment requirements and, when appropriate, `external_dependencies`.
- Never `pip install` dynamically at runtime.
- Set a deliberate license compatible with the code and dependencies used.
- Increment module version when a release changes code/data semantics.
- If following OCA conventions, use a version scheme tied to the Odoo major, e.g. `19.0.x.y.z`.

Do not add a dependency merely to access a model that is not actually required by the feature.

## 5. Naming and XML IDs

Follow Odoo naming conventions so future developers can locate extension points quickly.

- Models: singular dot notation, e.g. `orbitas.obligation.binding`.
- `Many2one`: suffix `_id`.
- `One2many` / `Many2many`: suffix `_ids`.
- Compute: `_compute_<field>`.
- Onchange: `_onchange_<field>`.
- Constraint: `_check_<invariant>`.
- Action methods: `action_<verb>`.
- Internal extension hooks: `_prepare_*`, `_get_*`, `_validate_*`, `_sync_*`.
- Prefix module-specific context keys, config keys and CSS classes to avoid collisions.

Use stable XML IDs. Do not rename XML IDs casually after release; if a rename is necessary, migrate it explicitly.

## 6. ORM-first rule

Use the Odoo ORM unless there is a measured reason not to.

- Work with recordsets, not scalar assumptions.
- Methods must support multi-record `self` unless their contract is explicitly singleton.
- Use `self.ensure_one()` only for genuinely singleton actions.
- Use `@api.model_create_multi` when overriding `create()` and preserve batch creation.
- Use Odoo `Command` helpers for x2many updates.
- Use `with_context()` rather than mutating context.
- Use `with_company()` when behavior must be evaluated in a record's company.
- Call `super()` and preserve the standard method contract unless the replacement is deliberate and documented.

Example batch-safe create override:

```python
from odoo import api, models


class OrbitasBinding(models.Model):
    _name = "orbitas.obligation.binding"

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        records._enqueue_initial_sync()
        return records
```

Do not convert a batch method back into one SQL/ORM call per record.

## 7. Raw SQL is exceptional

Raw SQL bypasses ORM behavior and Odoo security.

Use it only when ORM expression is impractical or profiling proves it necessary.

If raw SQL is required:

- parameterize every value; never concatenate user input;
- prefer Odoo's SQL wrapper/utilities for composability;
- flush fields that must be current before SQL reads/writes;
- invalidate the narrowest necessary ORM caches after SQL writes;
- document why ORM was insufficient;
- add tests covering access, consistency and cache behavior.

Never use SQL as a shortcut to bypass `account.move`, reconciliation, access rules, computed fields or business state machines.

## 8. Think extendable

Keep overrides small and composable.

Bad pattern:

```python
def action_sync(self):
    # 150 lines of selection, validation, mapping, network IO, logging...
    ...
```

Preferred shape:

```python
def action_sync(self):
    self._validate_sync_allowed()
    payloads = self._prepare_orbitas_payloads()
    return self._enqueue_payloads(payloads)
```

Expose narrow protected hooks so downstream addons can alter:

- eligibility domains;
- mapping logic;
- payload enrichment;
- policy selection;
- UI labels;
- retry policy.

Avoid hard-coded business assumptions buried inside CRUD overrides.

## 9. Never manually commit the normal Odoo transaction

Do **not** call `cr.commit()` or `cr.rollback()` in normal addon code.

Odoo owns the transaction boundary for RPC calls, tests and scheduled actions. Manual commits create partial state, broken rollbacks and non-reproducible tests.

If a separate cursor/transaction is truly required, it must be an explicit, reviewed design with its own lifecycle and error handling.

## 10. External side effects: use an outbox, not CRUD-time network calls

This is critical for ERP connectors.

Do not make a blockchain/API/webhook side effect part of a normal `create()`, `write()`, compute, constraint or onchange path when rollback cannot undo the remote action.

Preferred pattern:

```text
Odoo business transaction
    |
    +-- update ERP records
    +-- insert durable outbox event
    |
 COMMIT by Odoo
    |
worker/cron/queue
    |
    +-- send to Orbitas
    +-- record remote id / receipt
    +-- retry idempotently on failure
```

Outbox requirements:

- durable status: `pending / processing / done / retry / dead`;
- stable idempotency key;
- bounded retry count with backoff;
- network timeout;
- response hash/remote reference;
- no secret material in logs;
- re-entrant processing after worker crash.

A failed Orbitas API call must not corrupt or block core accounting transactions unless the business requirement explicitly demands synchronous rejection.

## 11. Security model: ACL + record rules + field restrictions

Every new persistent model must have an explicit security design.

Use layers:

1. `ir.model.access` for model-level CRUD;
2. record rules for row-level access;
3. field `groups` for sensitive fields;
4. model-level validation for business invariants.

Remember:

- ACL grants are additive;
- record rules are evaluated after ACLs;
- record rules are default-allow when no applicable rule restricts the record;
- global and group rules compose differently, so careless rules can either lock everyone out or broaden access unexpectedly.

UI invisibility is **not** security.

## 12. `sudo()` is a scalpel, not an error suppressor

Never use `sudo()` merely because an access error is inconvenient.

`sudo()` can cross record-rule and multi-company boundaries.

If elevation is required:

- keep the elevated recordset as small as possible;
- explicitly validate the current user's authority first;
- read/write only the necessary fields;
- document why normal ACL/rules are insufficient;
- add tests proving no cross-company or cross-user data leak.

Never return a broad `sudo()` recordset to code that assumes normal permissions.

## 13. Public methods and controller inputs are untrusted

A public model method can be called over RPC. Parameters and record IDs supplied to it are not trustworthy merely because the UI normally sends valid values.

- validate state transitions server-side;
- validate ownership/company/role;
- never trust client-computed monetary values;
- keep sensitive helpers protected (`_method`) when they are not intended as RPC surface;
- use ORM operations that enforce ACL/rules rather than hand-rolling authorization.

## 14. Multi-company correctness is mandatory

For company-scoped integration data:

- add `company_id`;
- default required company fields to `env.company` where appropriate;
- enable `_check_company_auto = True` on shareable models that link company-bound records;
- use `check_company=True` on relational fields where Odoo's consistency check applies;
- use `with_company(record.company_id)` when computing or creating company-sensitive data;
- use `company_dependent=True` only for values that truly vary by company;
- add global multi-company record rules based on `company_ids` for company-isolated records.

Every Orbitas connector configuration, credential reference, binding and outbox record must be scoped to the correct Odoo company.

Test with at least two companies and users with different company access.

## 15. Accounting data is protected business state

When extending Accounting:

- treat posted journal entries/invoices/bills as accounting facts, not convenient mutable rows;
- use supported accounting business methods for posting, payment and reconciliation;
- never update derived accounting fields (`amount_residual`, `payment_state`, etc.) directly;
- do not silently unpost/repost documents;
- preserve currency, company, partner and due-date semantics;
- treat refunds/credit notes and partial payments explicitly;
- do not infer legal settlement merely from a connector status.

For an integration that is primarily observational, keep Orbitas synchronization state in dedicated technical models instead of adding many persistence fields to `account.move`.

## 16. Computed fields, onchange and constraints

Computed fields:

- must work in batch;
- declare complete dependencies;
- avoid network calls and other side effects;
- store only when search/reporting/performance justifies the write amplification.

Onchange:

- is a UI assistance mechanism;
- must not be the only enforcement of a business invariant;
- may not run for imports, RPC integrations or background jobs.

Constraints:

- should validate durable invariants;
- must be deterministic and reasonably cheap;
- must not perform irreversible external side effects.

## 17. Performance rules

Profile before micro-optimizing, but avoid known anti-patterns from the start.

Mandatory practices:

- batch `create()` and `write()` operations;
- browse recordsets together so prefetch works;
- avoid `search()` / `search_count()` / remote calls inside record loops;
- use `_read_group` or precomputed mappings for aggregate counts;
- use dict/set lookup instead of nested scans when datasets grow;
- add database indexes only for demonstrated, selective query patterns;
- avoid unbounded searches and unbounded cron batches;
- use Odoo profiler/query-count tests for hot paths.

An integration that handles thousands of invoices must not become O(n²) because of per-invoice partner/config lookups.

## 18. Scheduled jobs and retries

Cron/worker code must be:

- bounded per run;
- idempotent;
- resumable;
- safe under repeated execution;
- safe if the previous process died after the remote side accepted a request but before local status was updated.

Process a deterministic batch, mark outcomes, and leave the next batch for the next run. Do not hold one database transaction open while sending thousands of external requests.

For high-throughput connectors, use a reviewed job/queue mechanism or a durable outbox processor rather than one giant scheduled action.

## 19. Views: inherit narrowly

- Inherit standard views; do not duplicate them wholesale.
- Use stable anchors/XPath expressions; avoid brittle selectors based on incidental DOM position.
- Keep view changes minimal.
- Use `groups` for visibility convenience, but enforce the same permission server-side.
- Put fields near the standard data they conceptually extend.
- Do not overload core forms with connector diagnostics; use a smart button or dedicated technical view for deep status.

## 20. Frontend/Owl discipline

For Odoo 19 web extensions:

- prefer Owl components and registries;
- use Odoo services through `useService`;
- use the `orm` service for model operations;
- use `rpc` for custom controller routes, not as a replacement for model ORM calls;
- package side-effectful long-lived behavior as a service where appropriate;
- declare JS/XML/SCSS assets in manifest bundles;
- prefer registry extension over monkey-patching;
- use `patch()` only when necessary and apply patches deterministically at module load time.

Do not copy old frontend examples blindly: controller/JS APIs evolve between Odoo majors.

## 21. HTTP controllers and webhooks

Keep controllers thin. They should authenticate/validate the request and call model/service logic that can be tested independently.

Rules:

- choose the narrowest appropriate route authentication;
- never expose company accounting data on `public` routes;
- keep CSRF protection for browser/session flows;
- disable CSRF for machine-to-machine webhook endpoints only when required, and replace it with strong request authentication;
- validate webhook signature, timestamp/expiry and replay nonce/idempotency key;
- rate-limit or otherwise bound externally reachable endpoints at the deployment layer;
- never log bearer tokens, API keys, signatures or raw sensitive payloads;
- return bounded error details, not Python tracebacks or secrets.

For Odoo 19 custom JSON controllers, verify route type and decorator semantics against Odoo 19 docs; do not copy legacy `type='json'` examples from older versions without checking the renamed/current API.

## 22. External API strategy

For new **external clients** of Odoo 19, prefer the current **External JSON-2 API** rather than building new dependencies on the legacy `/xmlrpc`, `/xmlrpc/2` or `/jsonrpc` external services, which Odoo has scheduled for removal in a future release.

This does not mean every addon needs an external Odoo API: code running inside the addon should call ORM directly.

Keep external API adapters behind an internal interface so transport/API evolution does not leak into business logic.

## 23. Secrets and configuration

Never commit credentials in Python, XML, demo data or JS assets.

Prefer deployment secret injection/secret manager integration for production secrets. If a value must be stored in Odoo configuration:

- restrict who can read/change it;
- never render it back to unauthorized users;
- do not put it in chatter or logs;
- separate secret values from non-secret connector settings;
- make credential rotation possible without reinstalling the addon.

## 24. Idempotency and bindings

Every ERP-to-Orbitas object needs a stable binding independent from transient request attempts.

Recommended identity dimensions:

```text
odoo_instance_id
+ company_id
+ source_model
+ source_record_id
= stable source identity
```

Store a dedicated binding with, as needed:

- source identity;
- source revision/write timestamp or payload hash;
- Orbitas remote/on-chain identifier;
- last synchronized state;
- last successful sync time;
- last error classification.

Use a database uniqueness constraint on the stable source identity.

Retries must not create duplicate Orbitas obligations. A duplicated webhook must not apply a settlement twice.

## 25. Orbitas integration boundary

For Orbitas, the Odoo addon is an **adapter**, not the clearing core and not blockchain settlement authority.

Target flow:

```text
Odoo accounting objects
        |
        v
Odoo adapter / eligibility / mapping
        |
        v
Normalized Orbitas obligation DTO
        |
        v
Durable outbox
        |
        v
Orbitas API / chain / indexer
```

The normalized DTO must not expose Odoo recordsets or Odoo-specific behavior to the Orbitas core.

The adapter owns Odoo-specific interpretation; the Orbitas domain model owns cross-ERP semantics.

### Recommended invoice-source snapshot

For invoice-backed obligations, capture enough source evidence to reproduce the mapping, for example:

- Odoo instance identifier;
- company identity;
- source model and record ID;
- invoice/bill number and source reference;
- counterparty identity;
- move type;
- currency;
- original amount;
- residual amount;
- invoice date and due date;
- accounting/document state;
- payment state where relevant;
- source `write_date` / revision marker.

Exact eligibility rules belong in the product/TRD and must be implemented as explicit adapter policy, not guessed from a single field.

## 26. Orbitas: inbound settlement instructions

A remote Orbitas clearing result must not silently rewrite Odoo accounting.

Separate:

1. **Orbitas instruction observed**;
2. **user/company consent confirmed**;
3. **real payment/settlement evidence received**;
4. **Odoo accounting action executed**;
5. **reconciliation confirmed**.

Until an explicit accounting workflow proves otherwise, store remote settlement state in connector models and surface it to users rather than forcing `account.move` into a paid/reconciled state.

This preserves the project's redirect-payment semantics: a settlement instruction is not automatically equivalent to novation or proof that the invoice was discharged.

## 27. Logging and observability

Use Python `logging`; never `print()` in production addon code.

Logs should include stable technical correlation fields such as:

- connector/backend ID;
- company ID;
- binding/outbox ID;
- source model/id;
- correlation/request ID;
- remote reference.

Do not log:

- credentials;
- access tokens;
- private keys;
- full invoice documents;
- unnecessary PII.

Expose operational health separately from logs: last successful sync, pending count, retry count, oldest pending event and last remote error category.

## 28. Testing pyramid

Every behavior change requires tests appropriate to its risk.

### Model tests

Use `TransactionCase` for:

- mapping and eligibility;
- state transitions;
- idempotency;
- multi-record behavior;
- computed values;
- error paths.

### Security tests

Use real test users/groups and verify:

- ACLs;
- record rules;
- field restrictions;
- no cross-company access;
- no accidental `sudo()` widening.

### HTTP / UI tests

Use `HttpCase` for controller/browser behavior when needed. Use Odoo frontend unit/tour tests for meaningful Owl/UI logic.

### Integration failure tests

Simulate:

- timeout;
- remote 4xx/5xx;
- duplicate request;
- accepted-remote/local-crash ambiguity;
- retry exhaustion;
- stale source revision;
- webhook replay.

### Accounting scenarios

For an accounting connector, cover at least the applicable scenarios:

- draft vs posted;
- customer invoice vs vendor bill;
- credit note/refund;
- partial payment;
- full payment;
- canceled/reversed document;
- multiple currencies;
- multiple companies;
- source record edited after export.

Use test tags deliberately (`standard`, `at_install`, `post_install`, custom tags) and make CI select them explicitly.

## 29. Upgrade and migration discipline

An Odoo-major upgrade is a migration project, not a search/replace exercise.

For a target major:

1. make the addon install cleanly on an empty target-version database;
2. remove warnings/deprecations and update frontend/view APIs;
3. run standard/custom tests;
4. test on an upgraded copy of a real database;
5. use migration scripts for data/schema/XML-ID changes;
6. rehearse the production upgrade.

Use Odoo migration layout:

```text
<module>/migrations/<version>/pre-*.py
<module>/migrations/<version>/post-*.py
<module>/migrations/<version>/end-*.py
```

When renaming models, fields or XML IDs, use upgrade/migration utilities so data is preserved. Do not "migrate" by dropping old fields/tables and recreating them unless deliberate data loss is approved.

Be careful with `noupdate` records: module update will not automatically refresh them as normal data.

## 30. Linting and CI

Use a pinned pre-commit/CI stack. At minimum include:

- Python formatting/linting;
- **pylint-odoo** with the correct target Odoo version;
- XML validation;
- translation/PO validation when translations exist;
- JS/SCSS lint/format where frontend code exists;
- addon install on a clean database;
- module tests;
- upgrade/update test for migration-bearing releases.

The OCA addon repository template is a useful reference implementation for Odoo-specific pre-commit and CI conventions. Reuse ideas, not unreviewed moving branches; pin tags/commits.

Treat linter warnings about deprecated Odoo APIs as migration signals, not cosmetic noise.

## 31. Translation rules

All user-facing strings must be translatable.

- use Odoo translation helpers correctly;
- do not pre-format/f-string a translatable string before passing it to translation machinery;
- do not translate technical identifiers;
- keep error messages meaningful but do not expose secrets or internal stack details.

## 32. Dependency and licensing hygiene

Before adding an Odoo/OCA/third-party module dependency:

- verify its target Odoo version;
- verify maintenance status;
- inspect license compatibility;
- inspect transitive Python/system dependencies;
- determine whether it works on the deployment platform (especially Odoo.sh restrictions);
- pin/reproduce dependency versions in deployment.

Do not copy proprietary Odoo Enterprise/App Store source into a differently licensed module.

## 33. Mandatory review gate

A PR changing an Odoo addon is not ready until reviewers can answer **yes** to all applicable items:

- no unnecessary core fork/copy;
- exact target Odoo major is known;
- manifest dependencies are minimal and correct;
- every new model has ACL/rule design;
- multi-company behavior is explicit;
- no broad/unjustified `sudo()`;
- no manual transaction commit/rollback;
- no raw SQL without justification/cache handling;
- no irreversible external side effect inside normal CRUD/compute/constraint;
- external operations are idempotent and timeout-bounded;
- batch ORM behavior is preserved;
- no N+1 query pattern on expected bulk paths;
- controller/public method inputs are validated;
- accounting fields/states are not mutated by shortcut;
- frontend uses extension points before patches;
- upgrade/migration impact is addressed;
- security, idempotency and failure-path tests exist;
- logs contain no secrets/PII spill;
- documentation/configuration instructions are updated.

## 34. Red-flag anti-patterns

Reject or explicitly redesign code containing patterns such as:

```python
for move in moves:
    self.env["some.model"].search([...])   # N+1
```

```python
self.env.cr.commit()                       # partial ERP transaction
```

```python
self.sudo().search([])                     # unexplained security bypass
```

```python
requests.post(url, json=payload)            # inside account.move.write()
```

```python
self.env.cr.execute(
    "UPDATE account_move SET payment_state='paid' ..."
)                                           # bypasses accounting/ORM
```

```python
@api.onchange("...")
def _onchange_x(self):
    ...                                     # only place a business invariant exists
```

```javascript
patch(CoreThing.prototype, {...})            // when registry/service extension exists
```

```text
API key in XML / JS / repository / log
```

These are architecture warnings, not style nits.

## 35. Definition of done for the Orbitas Odoo connector

A connector increment is done only when:

- addon installs on a clean supported Odoo database;
- update (`-u`) succeeds on a populated test database;
- two-company security tests pass;
- source-to-Orbitas mapping is deterministic;
- repeated export is idempotent;
- network failures do not corrupt Odoo transactions;
- outbox retry and dead-letter behavior are tested;
- no duplicate remote obligation is created after crash/retry;
- inbound events are replay-safe;
- accounting state is changed only through an explicit supported workflow;
- bulk invoice sync is profiled or query-count bounded;
- lint + Odoo tests + frontend tests (if any) are green;
- migration notes exist for persistent schema/meaning changes.

## 36. Reference basis

This skill is synthesized from current Odoo 19 developer documentation for coding guidelines, ORM, security, performance, multi-company behavior, testing, web frontend/services/assets, HTTP/external APIs and custom-database upgrades; plus current OCA addon repository/pylint-odoo conventions.

For source links and the review date, see `SOURCES.md`.
