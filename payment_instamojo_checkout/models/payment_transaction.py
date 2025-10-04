# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#    See LICENSE file for full copyright and licensing details.
#################################################################################

import logging
from odoo import api, fields, models, _
from odoo.addons.payment.models.payment_provider import ValidationError
_logger = logging.getLogger(__name__)

class PaymentTransactionInstamojoCheckout(models.Model):
    _inherit = 'payment.transaction'

    def _get_specific_rendering_values(self, processing_values):
        res = super()._get_specific_rendering_values(processing_values)
        if self.provider_code != 'instamojo_checkout':
            return res
        record_currency = self.env['res.currency'].browse(processing_values.get('currency_id'))
        processing_values.update({
                    'billing_partner_name':self.partner_name,
                    'billing_partner_email':self.partner_email,
                    'currency':record_currency,
				                'sale': self.sale_order_ids
                    })
        txValues = self.provider_id.instamojo_checkout_form_generate_values(processing_values)
        return txValues

    def _process_notification_data(self, data):
        res = super()._process_notification_data(data)
        if self.provider_code != 'instamojo_checkout':
            return res
        status = data.get('status')
        result = self.write({
            'provider_reference': data.get('id')
        })
        if status :
            self._set_done()
        if status == False:
            self._set_cancel()
        else:
            self._set_pending()
        return result
