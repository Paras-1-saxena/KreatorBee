from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.translate import _

from werkzeug import urls


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    def action_open_unblocked_third_party_domains(self):
        self.website_id._force()
        return {
            'name': _("Add external websites"),
            'view_mode': 'form',
            'res_model': 'website.custom_unblocked_third_party_domains',
            'type': 'ir.actions.act_window',
            'views': [[False, "form"]],
            'target': 'new',
        }
