import logging

from odoo import http
from odoo.addons.web.controllers.database import Database
from odoo.http import request
from odoo.service import db

_logger = logging.getLogger(__name__)


class DatabaseSecurity(Database):
    """Harden database manager routes against public access."""

    def _has_database_manager_access(self, master_pwd=None):
        """Allow only Settings users or requests with a valid master password.

        Routes use auth='none', so we keep checks defensive to avoid crashing
        when no database is selected or the request has no authenticated user.
        """
        if request.session.uid:
            try:
                if request.env.user.has_group("base.group_system"):
                    return True
            except Exception:
                _logger.debug("Unable to evaluate user group on auth='none' route", exc_info=True)

        if master_pwd:
            try:
                db.check_super(master_pwd)
                return True
            except Exception:
                _logger.info("Rejected database manager access with invalid master password")

        return False

    def _redirect_unauthorized(self):
        """Centralized redirect for blocked requests."""
        return request.redirect("/web/login")

    @http.route("/web/database", type="http", auth="none")
    def database_root(self, **kw):
        """Protect root alias and route authorized users to database manager UI."""
        if not self._has_database_manager_access(master_pwd=kw.get("master_pwd")):
            return self._redirect_unauthorized()
        return request.redirect("/web/database/manager")

    @http.route("/web/database/selector", type="http", auth="none")
    def selector(self, **kw):
        # Route stays public at framework level (auth='none'), but we enforce
        # authorization before executing core database selector behavior.
        if not self._has_database_manager_access(master_pwd=kw.get("master_pwd")):
            return self._redirect_unauthorized()
        return super().selector(**kw)

    @http.route("/web/database/manager", type="http", auth="none")
    def manager(self, **kw):
        if not self._has_database_manager_access(master_pwd=kw.get("master_pwd")):
            return self._redirect_unauthorized()
        return super().manager(**kw)

    @http.route("/web/database/create", type="http", auth="none", methods=["POST"], csrf=False)
    def create(self, master_pwd, name, lang, password, **post):
        # Validate access before calling core create logic to preserve behavior.
        if not self._has_database_manager_access(master_pwd=master_pwd):
            return self._redirect_unauthorized()
        return super().create(master_pwd, name, lang, password, **post)

    @http.route("/web/database/drop", type="http", auth="none", methods=["POST"], csrf=False)
    def drop(self, master_pwd, name):
        if not self._has_database_manager_access(master_pwd=master_pwd):
            return self._redirect_unauthorized()
        return super().drop(master_pwd, name)

    @http.route("/web/database/backup", type="http", auth="none", methods=["POST"], csrf=False)
    def backup(self, master_pwd, name, backup_format="zip"):
        if not self._has_database_manager_access(master_pwd=master_pwd):
            return self._redirect_unauthorized()
        return super().backup(master_pwd, name, backup_format=backup_format)
