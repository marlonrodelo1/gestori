from odoo import models, fields
from odoo.exceptions import UserError


class GenerateDemoWizard(models.TransientModel):
    _name = 'gestori.access.log.demo.wizard'
    _description = 'Generar Datos de Prueba'

    records_count = fields.Integer('Número de registros', default=450)
    months_back = fields.Integer('Meses atrás', default=3)
    confirm = fields.Boolean('Confirmar generación')

    def action_generate(self):
        if not self.confirm:
            raise UserError('Debes confirmar la generación de datos de prueba.')
        from ..hooks import _generate_demo_logs
        _generate_demo_logs(self.env)
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Datos generados',
                'message': f'Se generaron {self.records_count} registros de prueba.',
                'type': 'success',
                'sticky': False,
            }
        }

    def action_clear_all(self):
        self.env['gestori.access.log'].sudo().search([]).unlink()
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Registros eliminados',
                'message': 'Se eliminaron todos los registros de acceso.',
                'type': 'warning',
                'sticky': False,
            }
        }
