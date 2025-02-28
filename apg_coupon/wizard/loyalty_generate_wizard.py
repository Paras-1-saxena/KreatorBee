# -*- encoding: utf-8 -*-
from odoo import models, fields, api,_
from datetime import date, datetime, timedelta
from odoo.exceptions import UserError
import base64

class LoyaltyGenerateWizard(models.TransientModel):
    _inherit = 'loyalty.generate.wizard'
    _description = 'Generate Coupons'
   
    # program_id = fields.Many2one('loyalty.program', required=True, default=lambda self: self.env.context.get('active_id', False) or self.env.context.get('default_program_id', False))
    discount_id = fields.Many2one(related='program_id.discount_id', store=True)
    duration_id = fields.Many2one(related='program_id.duration_id', store=True,)
    duration = fields.Selection(related='program_id.duration', store=True,)

    @api.onchange('duration_id', 'duration')
    def onchange_duration(self):
        today = datetime.now()
        days = 0
        expiry_date = False
        self.valid_until = False
        if self.duration_id:
            if self.duration == 'minutes':
                pass
            elif self.duration == 'hours':
                pass
            else:
                self.duration == 'days'
                days = self.duration_id.name
                expiry_date = today + timedelta(days=days)
        self.valid_until = expiry_date