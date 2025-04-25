from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    coupon_type = fields.Selection(selection=[('company', 'Company'), ('creator', 'Creator'), ('partner', 'Partner')], string='Coupon Type')
