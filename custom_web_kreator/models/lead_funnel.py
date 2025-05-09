from odoo import models, fields


class LeadFunnel(models.Model):
    _name = 'lead.funnel'
    _description = 'Get Leads from the social adds'

    name = fields.Char(string='Lead Id')
    user_name = fields.Char(string='User Name')
    email = fields.Char(string='Email')
    mobile = fields.Char(string='Mobile')
    course_interested = fields.Char(string='Course')
    slot_date = fields.Date(string='Slot Date')
    slot_time = fields.Many2one(comodel_name='slot.time', string='Slot Time')
    visited = fields.Boolean(string="Visited")
    finished = fields.Boolean(string="Finished")
    survey_id = fields.Many2one(comodel_name='live.session.survey', sring='Survey')


class SlotTime(models.Model):
    _name = 'slot.time'
    _description = 'Slot Timings'

    name = fields.Char()


class LiveSessionSurvey(models.Model):
    _name = 'live.session.survey'
    _description = 'live session survey'

    name = fields.One2many(comodel_name='lead.funnel', inverse_name='survey_id', string='Lead')
    rating = fields.Selection(selection=[('1', 'Very Bad'), ('2', 'Bad'), ('3', 'Average'), ('4', 'Good'), ('5', 'Very Good')], string="Rating")
    notes = fields.Text(string="Notes")
