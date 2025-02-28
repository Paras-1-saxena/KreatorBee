# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
import re
from datetime import datetime,date
from odoo.exceptions import ValidationError
import math, random
import logging
_logger = logging.getLogger(__name__)

class LoyaltyProgram(models.Model):
	_inherit = 'loyalty.program'
	_description = 'Loyalty Program'

	discount_id = fields.Many2one("discount.discount", "Discount")
	duration_id = fields.Many2one("duration.duration", "Duration")
	duration = fields.Selection(related="duration_id.duration", store=True, string='Duration')

class LoyaltyReward(models.Model):
    _inherit = 'loyalty.reward'
    _description = 'Loyalty Reward'

    discount_id = fields.Many2one(related='program_id.discount_id', store=True)
    duration_id = fields.Many2one(related='program_id.duration_id', store=True,)
    duration = fields.Selection(related='program_id.duration', store=True,)

    @api.onchange('discount_id')
    def onchange_duration(self):
        self.discount = False
        if self.discount_id:
        	self.discount = self.discount_id.name