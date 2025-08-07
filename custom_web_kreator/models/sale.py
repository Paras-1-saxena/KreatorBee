from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _action_confirm(self):
        user = self.env.user
        sale_cart = self.env['kb.sale.cart'].sudo().search([('name', '=', user.id)], limit=1)
        sale_cart.sudo().write({'course_ids': False})
        return super()._action_confirm()