from odoo import models,fields,api,_

class AccountMove(models.Model):
    _inherit='account.move'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            defaults = self.default_get(['name', 'journal_id'])
            journal_id = self.env['account.journal'].browse(vals.get('journal_id', defaults.get('journal_id')))
            if vals.get('journal_id', defaults.get('journal_id')):
                if journal_id.sequence_id:
                    vals['name'] = journal_id.sequence_id.next_by_id()

            return super(AccountMove, self).create(vals_list)


    @api.depends('company_id', 'invoice_filter_type_domain')
    def _compute_suitable_journal_ids(self):
        for m in self:
            journal_type = m.invoice_filter_type_domain or []
            company_id = m.company_id.id or self.env.company.id
            domain = [('company_id', '=', company_id)]
            m.suitable_journal_ids = self.env['account.journal'].search(domain)



    @api.model_create_multi
    def create(self, vals_list):
        # OVERRIDE
        moves = super(AccountMove, self).create(vals_list)
        if moves is not None:
            for move in moves:
                if move.reversed_entry_id:
                    continue
                purchases = move.line_ids.purchase_line_id.order_id
                if not purchases:
                    continue
                refs = [purchase._get_html_link() for purchase in purchases]
                message = _("This vendor bill has been created from: %s") % ','.join(refs)
                move.message_post(body=message)
            return moves



class AccountJournal(models.Model):
    _inherit='account.journal'


    sequence_id = fields.Many2one(
        'ir.sequence', 'Reference Sequence',
        check_company=True, copy=False)
    sequence_code = fields.Char('Sequence Prefix', required=False)



