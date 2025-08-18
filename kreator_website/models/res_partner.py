from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def update_phone_no(self, **kwargs):
        for partner, phno in kwargs.items():
            if partner and phno:
                partner_obj = self.sudo().browse(partner)
                partner_obj.write({'phone': phno, 'mobile': phno})