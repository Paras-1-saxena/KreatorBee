from odoo import api, fields, models, exceptions,_

class SlideChannel(models.Model):
    _inherit = 'res.partner'

    partner_term_accepted = fields.Boolean(string='Term Accepted ?')
