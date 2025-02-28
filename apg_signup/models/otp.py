# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
import re
from datetime import datetime,date
from odoo.exceptions import ValidationError
import math, random
import logging
_logger = logging.getLogger(__name__)

class MobOtp(models.Model):
	_name = 'otp.otp'
	_description = 'Moble OTP'

	otp = fields.Char(string='OTP')
	mobile = fields.Char(string='OTP')
	partner_id = fields.Many2one('res.partner')
	is_verify = fields.Boolean(string="OTP Verified")