from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    specific_commission = fields.Float(string='Specific Partner Commission')
