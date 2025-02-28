# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from datetime import datetime,date
from odoo.exceptions import ValidationError

class discount(models.Model):
	_name = 'discount.discount'
	_description = 'Discount'
	_rec_name = 'name'


	name = fields.Float(string="Name")

	