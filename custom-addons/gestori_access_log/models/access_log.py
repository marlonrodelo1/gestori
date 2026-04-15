from odoo import models, fields


class GestoriAccessLog(models.Model):
    _name = 'gestori.access.log'
    _description = 'Registro de Accesos'
    _order = 'date desc'
    _rec_name = 'login'

    date = fields.Datetime('Fecha y Hora', readonly=True, index=True)
    login = fields.Char('Login', readonly=True)
    partner_id = fields.Many2one('res.partner', 'Usuario', readonly=True)
    ip = fields.Char('Dirección IP', readonly=True)
    result = fields.Selection([
        ('success', 'Exitoso'),
        ('failure', 'Fallido'),
    ], string='Resultado', readonly=True)
