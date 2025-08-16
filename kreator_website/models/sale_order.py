from odoo import models, fields, api, _


class SalesOrder(models.Model):
    _inherit = 'sale.order'

    def generate_sale_for_users(self, product_ids=[]):
        products = self.env['product.template'].search([('id', 'in', product_ids)]).product_variant_ids
        order_line = [(0, 0, {'product_id': product.id, 'product_uom_qty': 1}) for product in products]
        so_partners = self.env['sale.order'].sudo().search([]).partner_id.ids
        for contact in self.env['res.partner'].sudo().search([('user_type', '=', 'partner'), ('id', 'not in', so_partners)]):
            order = self.create({
                'partner_id': contact.id,
                'partner_invoice_id': contact.id,
                'partner_shipping_id': contact.id,
                'order_line': order_line,
            })
            order.action_confirm()
            self._cr.commit()