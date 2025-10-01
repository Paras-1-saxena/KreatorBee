# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#    See LICENSE file for full copyright and licensing details.
#################################################################################

import logging
import pprint
from odoo import http,fields
from odoo.http import request
_logger = logging.getLogger(__name__)
import time

class InstamojoCheckoutController(http.Controller):
    _return_url = '/payment/instamojo/return'

    @http.route([_return_url], type='http', auth='public', csrf=False, save_session=False)
    def instamojo_return(self, **post):
        _logger.info('Instamojo: Post %s', pprint.pformat(post))
        reference = post.get('reference',False)
        if reference:
            tx = request.env['payment.transaction'].sudo().search([('reference', '=', reference)], limit=1)
            time.sleep(2)
            data = tx.provider_id._get_payment_status(post)
            # tx._post_process_after_done()
            data.update({'tx':tx})
            _logger.info('Instamojo: entering form_feedback with post data %s', pprint.pformat(data))
            tx.sudo()._handle_notification_data('instamojo_checkout',data)
        return request.redirect('/payment/status')
        
        
        
    @http.route('/payment/instamojo/webhook',type='http',csrf=False,auth='public',methods=['POST'])
    def webhook_new_url(self,**post):
        
        payment_id=post.get('payment_id')
        amount=post.get('amount')
        purpose=post.get('purpose')  # typically your Odoo order reference
        status=post.get('status')  # "Credit" = payment successful
        _logger.info('Instamojo: wwebhook data %s',pprint.pformat(post))
        # Find the sale order
        order=request.env['sale.order'].sudo().search([('payment_request_id','=',payment_id)],limit=1)
        _logger.info('Instamojo: wwebhook url and order id %s',pprint.pformat(order))
        
        if order and status=="Credit":
				        # Confirm sale order
				        if order.state in ['draft','sent']:
								        order.action_confirm()
								        order._update_partner_onlines()
				        
				        
								        
				        if not order.invoice_ids:
								        invoice=order._create_invoices()  # creates invoice from SO
								        invoice.action_post()
				        else:
								        # Post any draft invoices
								        for invoice in order.invoice_ids.filtered(lambda i:i.state=='draft'):
												        invoice.action_post()
				        
				        # Post payment
				        journal=request.env['account.journal'].sudo().search([('type','=','bank')],limit=1)
				        payment_vals={
								        'payment_type':'inbound','partner_type':'customer','partner_id':order.partner_id.id,'amount':amount,
								        'currency_id': order.pricelist_id.currency_id.id,'payment_date':fields.Date.today(),
								        'journal_id':  journal.id,'ref':f"Instamojo {payment_id}",}
				        payment=request.env['account.payment'].sudo().create(payment_vals)
				        payment.action_post()
        return "Ok"
        
        
