# from odoo import api, fields, models, exceptions,_
#
# class ProductMultiSelling(models.Model):
#     _name = 'product.multi.selling'
#     _description = 'Product Batch selling'
#
#     product_id = fields.Many2one(comodel_name='product.product', string='Product')
#     connected_product_ids = fields.Many2many(comodel_name='product.product', string="Connected Products")
