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
    expired = fields.Boolean(string="Expired")
    survey_id = fields.Many2one(comodel_name='live.session.survey', string='Survey')
    describe = fields.Text(string='Describe')
    city = fields.Char(string='City')
    income = fields.Selection(selection=[('1', 'Less than ₹10,000'), ('2', '₹10,000 – ₹50,000'), ('3', '₹50,000 – ₹1,00,000'), ('4', '₹1,00,000+')])
    affiliate_career = fields.Selection(
        selection=[('1', 'Yes, I’m already doing it'), ('2', 'I’ve heard about it but haven’t started'), ('3', 'No, this is my first time')])

    def open_survey(self):
        action = {
            'name': 'Survey',
            'res_model': 'live.session.survey',
            'view_mode': 'form',
            'type': 'ir.actions.act_window',
            'res_id': self.survey_id.id,
            'target': 'new'
        }
        return action


class SlotTime(models.Model):
    _name = 'slot.time'
    _description = 'Slot Timings'

    name = fields.Char()


class LiveSessionSurvey(models.Model):
    _name = 'live.session.survey'
    _description = 'live session survey'

    name = fields.Many2one(comodel_name='lead.funnel', string='Lead')
    rating = fields.Selection(selection=[('1', 'Very Bad'), ('2', 'Bad'), ('3', 'Average'), ('4', 'Good'), ('5', 'Very Good')], string="Rating")
    delivery = fields.Selection(selection=[('1', 'Very Bad'), ('2', 'Bad'), ('3', 'Average'), ('4', 'Good'), ('5', 'Very Good')], string="Delivery")
    friend = fields.Selection(
        selection=[('1', 'Very Bad'), ('2', 'Bad'), ('3', 'Average'), ('4', 'Good'), ('5', 'Very Good')],
        string="Friend")
    platform = fields.Selection(
        selection=[('1', 'Very Bad'), ('2', 'Bad'), ('3', 'Average'), ('4', 'Good'), ('5', 'Very Good')],
        string="Platform")
    starting = fields.Selection(
        selection=[('1', 'Very Bad'), ('2', 'Bad'), ('3', 'Average'), ('4', 'Good'), ('5', 'Very Good')],
        string="Starting")
