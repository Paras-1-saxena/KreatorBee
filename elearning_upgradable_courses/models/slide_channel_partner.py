from odoo import api, fields, models, exceptions,_

class SlideChannel(models.Model):
    _inherit = 'slide.channel.partner'

    upgrade_stage_ids = fields.Many2one(comodel_name='slide.channel.upgrade.stage', string='Course Option', domain="[('channel_id', '=', channel_id)]")
