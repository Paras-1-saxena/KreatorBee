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
    min_quantity = fields.Integer(string="Minimum Quantity")
    discount_per_course = fields.Float(string="Discount Per Course", compute='_compute_discount_per_course',store=True)

    @api.depends('discount_id','min_quantity')
    def _compute_discount_per_course(self):
        for rec in self:
            rec.discount_per_course = 0.0
            if rec.discount_id and rec.min_quantity:
                discount_value = rec.discount_id.name  # use numeric field, not name
                if discount_value <= rec.min_quantity:
                    raise ValidationError(_("Discount amount should be greater than the minimum quantity."))
                rec.discount_per_course = discount_value / rec.min_quantity

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