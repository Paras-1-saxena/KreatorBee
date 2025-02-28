from odoo import models,fields, _

class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'

    def action_create_payments(self):
        if self.is_register_payment_on_draft:
            self.payment_difference_handling = 'open'
        payments = self._create_payments()

        # Automatically send receipt email for each payment
        template_id = self.env.ref('account.mail_template_data_payment_receipt')
        for payment in payments:
            if template_id:
                # Send email for each payment
                template_id.send_mail(payment.id, force_send=True)

        if self._context.get('dont_redirect_to_payments'):
            return True

        action = {
            'name': _('Payments'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.payment',
            'context': {'create': False},
        }
        if len(payments) == 1:
            action.update({
                'view_mode': 'form',
                'res_id': payments.id,
            })
        else:
            action.update({
                'view_mode': 'list,form',
                'domain': [('id', 'in', payments.ids)],
            })
        return action

class AccountJournal(models.Model):
    _inherit = 'account.journal'

    bank_reference = fields.Selection(
            [('rbl', 'RBL'), ('icici', 'ICICI')],
            string='Bank Reference',
            help="Select the bank reference for this journal"
        )
