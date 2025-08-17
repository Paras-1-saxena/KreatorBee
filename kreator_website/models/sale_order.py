from odoo import models, fields, api, _


class SalesOrder(models.Model):
    _inherit = 'sale.order'

    def generate_sale_for_users(self, partner_products=[]):
        subscription = self.env['product.template'].search([('id', '=', 107)]).product_variant_ids
        for partner, products in partner_products:
            contact = self.env['res.partner'].sudo().search([('id', '=', partner)])
            product_variants = self.env['product.template'].sudo().search([('id', 'in', products)]).product_variant_ids
            order_line = [(0, 0, {'product_id': product.id, 'product_uom_qty': 1}) for product in product_variants]
            order_line.append((0, 0, {'product_id': subscription.id, 'product_uom_qty': 1}))
            order = self.create({
                'partner_id': contact.id,
                'partner_invoice_id': contact.id,
                'partner_shipping_id': contact.id,
                'order_line': order_line,
            })
            order.action_confirm()
            self._cr.commit()