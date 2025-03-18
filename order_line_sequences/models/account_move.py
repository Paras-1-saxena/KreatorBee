from odoo import models,fields,api

class AccountMove(models.Model):
    _inherit = 'account.move'

    # sequence1 = fields.Char(string='Sequence Number  ')

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    invoice_sequence_number = fields.Char(string='#  ',compute="_compute_invoice_line_sequence")

    @api.depends('invoice_sequence_number')
    def _compute_invoice_line_sequence(self):
        number = 1
        for record in self.move_id.invoice_line_ids:
            record.invoice_sequence_number = number
            number += 1
