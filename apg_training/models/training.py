# -*- coding: utf-8 -*-
from odoo import models, fields, api, Command,exceptions, _
import time
from odoo.exceptions import UserError, ValidationError

class CourseTraining(models.Model):
    _name = 'apg.course.training'
    _description = 'Course Training'
    _rec_name = 'name'

    name = fields.Char('Training Name', required=True)
    image = fields.Binary('Training Image')
    line_ids = fields.One2many('apg.course.training.lines', 'training_id', string="Training Lines")

class CourseTrainingLines(models.Model):
    _name = 'apg.course.training.lines'
    _description = 'Course Training Line'

    training_id = fields.Many2one('apg.course.training', string="Training", ondelete="cascade")
    name = fields.Char('Line Name', required=True)
    image = fields.Binary('Image')
    youtube_url = fields.Char('YouTube URL')