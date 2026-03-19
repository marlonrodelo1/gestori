from odoo import models
from odoo.http import request


class ResUsers(models.Model):
    _inherit = 'res.users'

    @classmethod
    def _login(cls, db, login, password, user_agent_env):
        uid = super()._login(db, login, password, user_agent_env)
        result = 'success' if uid else 'failure'
        ip = None
        if request:
            ip = request.httprequest.environ.get('HTTP_X_FORWARDED_FOR') or \
                 request.httprequest.environ.get('REMOTE_ADDR')
        try:
            env = cls.browse(cls._origin.env if hasattr(cls, '_origin') else None)
        except Exception:
            env = None
        # Log usando cursor directo para no fallar si el ORM no está disponible
        try:
            from odoo.api import Environment
            from odoo.modules.registry import Registry
            import odoo
            registry = Registry(db)
            with registry.cursor() as cr:
                env2 = Environment(cr, odoo.SUPERUSER_ID, {})
                partner_id = False
                if uid:
                    user = env2['res.users'].browse(uid)
                    partner_id = user.partner_id.id
                env2['gestori.access.log'].create({
                    'login': login,
                    'partner_id': partner_id,
                    'ip': ip,
                    'result': result,
                })
                cr.commit()
        except Exception:
            pass
        return uid
