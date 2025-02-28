# -*- coding: utf-8 -*-
from odoo import models, fields, api, Command, _
from datetime import datetime, date
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
import json
import logging
_logger = logging.getLogger(__name__)



class PartnerCommission(models.Model):
    _name = 'partner.commission'
    _description = 'Partner Commission Configuration'
    _rec_name = 'name'

    name = fields.Char(string="Commission Plan")
    rate = fields.Float(string="Rate", required=True)
    line_ids = fields.One2many('partner.commission.line', 'commission_id', string="Commission Lines")
    

class PartnerCommissionLine(models.Model):
    _name = 'partner.commission.line'
    _description = 'Partner Commission Line'

    target = fields.Char(string="Target", required=True)
    rate = fields.Float(string="Rate", required=True)
    commission_id = fields.Many2one('partner.commission', string="Partner Commission", ondelete="cascade")

class DirectCommission(models.Model):
    _name = 'direct.commission'
    _description = 'Direct Commission Configuration'
    _rec_name = 'name'

    name = fields.Char(string="Commission Plan")
    rate = fields.Float(string="Rate", required=True)
    line_ids = fields.One2many('direct.commission.line', 'commission_id', string="Commission Lines")

class DirectCommissionLine(models.Model):
    _name = 'direct.commission.line'
    _description = 'Direct Commission Line'

    target = fields.Char(string="Target", required=True)
    rate = fields.Float(string="Rate", required=True)
    commission_id = fields.Many2one('direct.commission', string="Direct Commission", ondelete="cascade")

class Coursestandard(models.Model):
    _name = 'course.standard'
    _description = 'Course standard'

    # name = fields.Char(string="Name", required=True)  # Example field for course name
    description = fields.Text(string="Description", required=True)  # Text field for additional course details
    # google_drive_links = fields.Many2many(
    #     comodel_name='ir.attachment',  # This model manages file attachments
    #     relation='course_standard_attachment_rel',  # Relation table name
    #     column1='course_standard_id',  # Relation column for `course.standard`
    #     column2='attachment_id',  # Relation column for `ir.attachment`
    #     string="Google Drive Links"
    # )


class TermsAndConditions(models.Model):
    _name = 'terms.conditions'
    _description = 'Terms and Conditions'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # name = fields.Char(string="Title", required=True)
    content = fields.Text(string="Terms and Conditions", required=True)

