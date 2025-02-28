from odoo import api, fields, models, exceptions,_
from odoo.exceptions import UserError, ValidationError

class MyProductCart(models.Model):
    _name = 'my.product.cart'
    _description = 'My Product Cart'

    course_id = fields.Many2one('slide.channel')
    name = fields.Char(related="course_id.name")
    product_id = fields.Many2one('product.product', related="course_id.product_id", store=True)
    regular_price = fields.Float(string="Regular Price", related="course_id.regular_price", store=True)
    sales_price = fields.Float(string="Sales Price", related="course_id.sales_price", store=True)
    partner_commission = fields.Float(string="Partner Sales Commission", related="course_id.partner_commission",
                                      store=True)
    user_id = fields.Many2one('res.users', related="course_id.create_uid", store=True)
    partner_id = fields.Many2one('res.partner')
