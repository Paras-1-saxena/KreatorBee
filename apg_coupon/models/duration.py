# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from datetime import datetime,date
from odoo.exceptions import ValidationError

class duration(models.Model):
	_name = 'duration.duration'
	_description = 'Duration'
	_rec_name = 'name'


	name = fields.Integer(string="Name")
	duration = fields.Selection([
		('minutes', 'Minutes'),
		('hours', 'Hours'), 
		('days', 'Days')],
		string='Duration', default="days")

	# def name_get(self):
	# 	result = []
	# 	for rec in self:
	# 		name = rec.name or '-'
	# 		if rec.duration:
	# 			name += ' [' + rec.duration + ']'
	# 		result.append((rec.id, name))
	# 	return result