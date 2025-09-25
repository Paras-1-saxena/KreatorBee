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

        if self.subscription_id:
            if self.subscription_id.stage_id.name == 'Draft':
                pass
                # self.subscription_id.button_start_date()
            else:
                pending_subscription = self.subscription_id
                pending_subscription.write({
                    'is_to_renew': False,
                    'start_date': pending_subscription.next_invoice_date})
                new_date = self.find_renew_date(
                    pending_subscription.next_invoice_date,
                    pending_subscription.date_started,
                    pending_subscription.plan_id.days_to_end)
                pending_subscription.write(
                    {'close_date': new_date['close_date']})

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

class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'
    

    def _post_process_after_done(self):
				    """
								Full automation:
								- Confirm sale order
								- Create & post invoice
								- Register payment automatically
								"""
				    for tx in self:
								    for order in tx.sale_order_ids:
												    # 1️⃣ Confirm Sale Order
												    if order.state=='draft':
																    order.action_confirm()
												    
												    # 2️⃣ Create Invoice if not exists
												    if not order.invoice_ids:
																    invoice=order._create_invoices()  # creates invoice from SO
																    invoice.action_post()
												    else:
																    # Post any draft invoices
																    for invoice in order.invoice_ids.filtered(lambda i:i.state=='draft'):
																				    invoice.action_post()
												    
												    # 3️⃣ Register Payment automatically
												    for invoice in order.invoice_ids.filtered(lambda i:i.state=='posted'):
																    # check if payment already exists
																    payment=self.env['account.payment'].search(
																				    [('payment_transaction_id','=',tx.id)])
																    if not payment:
																				    payment_vals={
																								    'payment_type':'inbound','partner_type':'customer','partner_id':order.partner_id.id,
																								    'amount':invoice.amount_total,'currency_id':invoice.currency_id.id,
																								    'journal_id':self.env['account.journal'].search([('type','=','bank')],limit=1).id,
																								    'payment_reference':tx.reference,}
																				    payment=self.env['account.payment'].create(payment_vals)
																				    payment.action_post()
																    # if  invoice.invoice_line_ids:
																				#     # Get the receivable lines from the invoice and payment
																				#     invoice_line=invoice.line_ids.filtered(lambda l:l.account_id.internal_type=='receivable')
																				#     payment_line=payment.move_id.line_ids.filtered(lambda l:l.account_id.internal_type=='receivable')
																				#
																				#     (invoice_line+payment_line).reconcile()
				    return True
    
    
    def _create_payment(self, **extra_create_values):
        res = super()._create_payment(**extra_create_values)
        if res and res.state == 'paid' and res.invoice_ids:
            for invoice in res.invoice_ids:
                if invoice.subscription_id:
                    subscription = invoice.subscription_id
                    if subscription.stage_id.name == 'In Progress':
                        pass
                        # pending_subscription = subscription
                        # pending_subscription.write({
                        #     'is_to_renew': False,
                        #     'start_date': pending_subscription.next_invoice_date})
                        # new_date = pending_subscription.find_renew_date(
                        #     pending_subscription.next_invoice_date,
                        #     pending_subscription.date_started,
                        #     pending_subscription.plan_id.days_to_end)
                        # pending_subscription.write(
                        #     {'close_date': new_date['close_date']})
        return res
