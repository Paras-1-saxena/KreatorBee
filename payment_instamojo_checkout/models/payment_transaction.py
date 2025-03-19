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
                    'currency':record_currency
                    })
        txValues = self.provider_id.instamojo_checkout_form_generate_values(processing_values)
        return txValues

    def _get_tx_from_notification_data(self, provider_code, notification_data):
        tx = super()._get_tx_from_notification_data(provider_code, notification_data)
        if provider_code != 'instamojo_checkout' or len(tx) == 1:
            return tx
        reference = notification_data['payment_request']['purpose']
        if not reference:
            raise ValidationError("Instamojo Payment: " + _("Received data with missing reference."))

        tx = self.search([('reference', '=', reference), ('provider_code', '=', 'instamojo_checkout')])
        if not tx:
            raise ValidationError(
                "Instamojo Payment: " + _("No transaction found matching reference %s.", reference)
            )
        return tx

    def _process_notification_data(self, data):
        res = super()._process_notification_data(data)
        if self.provider_code != 'instamojo_checkout':
            return res
        status = data['payment_request']['payment']['status']
        result = self.write({
            'provider_reference': data['payment_request']['payment']['payment_id'],
        })
        if status == 'Credit':
            self._set_done()
        if status == 'Failed':
            self._set_cancel()
        else:
            self._set_pending()
        return result
