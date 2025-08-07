from odoo import models, fields, api


class Kb_Sale_Cart(models.Model):
    _name = 'kb.sale.cart'
    _description = 'Record sale Cart'

    name = fields.Many2one('res.users', string='User Name')
    course_ids = fields.Many2many('slide.channel', string='Courses')