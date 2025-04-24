from odoo import models, fields


class ReferralTracker(models.Model):
    _name = 'referral.tracker'
    
    name = fields.Char(string='MODE')
    course = fields.Char(string='Course Name')
    variant = fields.Char(string='Variant')
