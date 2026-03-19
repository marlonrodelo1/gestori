## Plan: Odoo 18 DB Manager Hardening Module

Implement a standalone custom module named gestori_security under custom-addons that safely overrides selected web database routes, allowing access only to users in Settings group (`base.group_system`) or requests providing valid master password (`admin_passwd`), and redirecting all unauthorized requests to `/web/login` while preserving Odoo behavior for authorized flows.

**Steps**
1. Confirm routing baseline from core web database controller and reuse exact route signatures to avoid regressions (*blocks step 3*).
2. Create module skeleton in `custom-addons/gestori_security` with manifest/init/controller package files and dependency on `web` (*blocks step 3*).
3. Implement controller inheritance from `odoo.addons.web.controllers.database.Database` using empty `@http.route()` overrides for:
   - `selector` (`/web/database/selector`)
   - `create` (`/web/database/create`)
   - plus an explicit lightweight handler for `/web/database` to ensure requested URL is covered and protected.
4. Add shared access-check helper in controller:
   - If current session user belongs to `base.group_system`, allow.
   - Else, validate submitted `master_pwd` using `odoo.service.db.check_super` (handle AccessDenied safely).
   - Else, redirect to `/web/login`.
   Dependencies: step 3; helper reused by all overridden routes.
5. Keep route stability:
   - Preserve original auth mode (`auth="none"`) and HTTP method/csrf settings.
   - For authorized requests, delegate to `super()` so native behavior remains unchanged.
   - Do not alter unrelated database routes (`/manager`, `/backup`, etc.) to minimize surface area.
6. Add concise production comments in code explaining:
   - why auth remains `none`,
   - why access checks happen before `super()`,
   - why `check_super` exceptions are swallowed and converted to login redirect.
7. Validate behavior manually across scenarios:
   - anonymous to each protected route => redirect to `/web/login`.
   - logged Settings user => route works normally.
   - anonymous with correct `master_pwd` on POST create => works.
   - wrong `master_pwd` => redirect.
8. Provide installation instructions for custom-addons path and module install/upgrade commands.

**Relevant files**
- `addons/web/controllers/database.py` — reference for inherited class, exact method signatures, and route decorators to preserve behavior.
- `odoo/service/db.py` — reference for `check_super` master-password validation behavior.
- `custom-addons/gestori_security/__manifest__.py` — module metadata and dependency declaration.
- `custom-addons/gestori_security/__init__.py` — module init.
- `custom-addons/gestori_security/controllers/__init__.py` — controller package init.
- `custom-addons/gestori_security/controllers/main.py` — route overrides and access control logic.

**Verification**
1. Start Odoo with addons path including `custom-addons` and update app list.
2. Install module and confirm server starts without traceback.
3. Hit `/web/database`, `/web/database/selector`, and `/web/database/create` (POST) as anonymous and confirm redirect to `/web/login`.
4. Test with authenticated Settings user and confirm normal behavior via `super()`.
5. Test POST create with valid/invalid `master_pwd` and confirm allow/redirect accordingly.
6. Sanity check that unmodified routes (e.g. `/web/database/manager`) still work as before.

**Decisions**
- Included scope: harden three requested routes only, with strict redirect policy for unauthorized access.
- Included interpretation of “admin”: any authenticated user in `base.group_system` (confirmed by user).
- Included handling of `/web/database`: add explicit protected endpoint because core controller does not define this base route.
- Excluded: global rewrite of all database manager endpoints, template modifications, or config-level `list_db` hard disable.

**Further Considerations**
1. Optional extension: protect additional database routes (`/manager`, `/drop`, `/backup`, `/restore`) with same helper if you want full DB manager lockdown beyond the three requested endpoints.
