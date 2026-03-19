from odoo import models
from odoo.http import request


class ResUsers(models.Model):
    _inherit = 'res.users'

    def _check_credentials(self, password, env):
        try:
            result = super()._check_credentials(password, env)
            self._gestori_log_access('success')
            return result
        except Exception:
            self._gestori_log_access('failure')
            raise

    def _gestori_log_access(self, result):
        try:
            ip = None
            if request:
                ip = (
                    request.httprequest.environ.get('HTTP_X_FORWARDED_FOR', '').split(',')[0].strip()
                    or request.httprequest.environ.get('REMOTE_ADDR')
                )
            partner_id = self.partner_id.id if self.ids else False
            login = self.login if self.ids else ''
            self.env['gestori.access.log'].sudo().create({
                'login': login,
                'partner_id': partner_id,
                'ip': ip,
                'result': result,
            })
        except Exception:
            pass
