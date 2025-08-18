from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def update_phone_no(self, partner_info = []):
        for partner, phno in partner_info:
            if partner and phno:
                partner_obj = self.sudo().browse(partner)
                partner_obj.sudo().write({'phone': phno, 'mobile': phno})