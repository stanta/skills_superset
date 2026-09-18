# Sources — Orbitas Odoo Addon Development Skill

Reviewed: **2026-09-12**

Primary sources:

1. Odoo 19 — Coding guidelines  
   https://www.odoo.com/documentation/19.0/contributing/development/coding_guidelines.html

2. Odoo 19 — Security in Odoo  
   https://www.odoo.com/documentation/19.0/developer/reference/backend/security.html

3. Odoo 19 — ORM API  
   https://www.odoo.com/documentation/19.0/developer/reference/backend/orm.html

4. Odoo 19 — Performance  
   https://www.odoo.com/documentation/19.0/developer/reference/backend/performance.html

5. Odoo 19 — Multi-company Guidelines  
   https://www.odoo.com/documentation/19.0/developer/howtos/company.html

6. Odoo 19 — Testing Odoo  
   https://www.odoo.com/documentation/19.0/developer/reference/backend/testing.html

7. Odoo 19 — Command-line interface / test selection  
   https://www.odoo.com/documentation/19.0/developer/reference/cli.html

8. Odoo 19 — Module manifests  
   https://www.odoo.com/documentation/19.0/developer/reference/backend/module.html

9. Odoo 19 — Web controllers  
   https://www.odoo.com/documentation/19.0/developer/reference/backend/http.html

10. Odoo 19 — External JSON-2 API  
    https://www.odoo.com/documentation/19.0/developer/reference/external_api.html

11. Odoo 19 — External RPC API and deprecation notice  
    https://www.odoo.com/documentation/19.0/developer/reference/external_rpc_api.html

12. Odoo 19 — Frontend services  
    https://www.odoo.com/documentation/19.0/developer/reference/frontend/services.html

13. Odoo 19 — Frontend framework overview  
    https://www.odoo.com/documentation/19.0/developer/reference/frontend/framework_overview.html

14. Odoo 19 — JavaScript reference / registries / patching  
    https://www.odoo.com/documentation/19.0/developer/reference/frontend/javascript_reference.html

15. Odoo 19 — Assets  
    https://www.odoo.com/documentation/19.0/developer/reference/frontend/assets.html

16. Odoo 19 — Upgrade a customized database  
    https://www.odoo.com/documentation/19.0/developer/howtos/upgrade_custom_db.html

17. Odoo 19 — Upgrade scripts  
    https://www.odoo.com/documentation/19.0/developer/reference/upgrades/upgrade_scripts.html

18. Odoo 19 — Odoo.sh project/custom-module support  
    https://www.odoo.com/documentation/19.0/administration/odoo_sh/getting_started/create.html

19. Odoo 19 — Licenses  
    https://www.odoo.com/documentation/19.0/legal/licenses.html

Community/OCA quality references:

20. OCA Addons Repo Template  
    https://github.com/OCA/oca-addons-repo-template

21. OCA pylint-odoo  
    https://github.com/OCA/pylint-odoo

22. OCA Maintainer Tools  
    https://github.com/OCA/maintainer-tools

Project-specific design basis:

- Orbitas treats Odoo as the reference ERP connector (Wave 0) before other ERP connectors.
- ERP adapters normalize source-system objects into a common Orbitas domain model rather than leaking Odoo/QBO/1C objects into clearing core.
- Orbitas settlement uses redirect-payment instructions rather than assuming automatic novation; therefore inbound clearing state must not be equated with an Odoo accounting discharge without an explicit accounting workflow.
