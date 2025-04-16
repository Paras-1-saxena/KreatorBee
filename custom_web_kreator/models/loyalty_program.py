from odoo import api, fields, models, exceptions,_
from odoo.exceptions import UserError, ValidationError

class MyProductCart(models.Model):
    _inherit = 'loyalty.program'

    referral_product_id = fields.Many2one(comodel_name='product.template')

