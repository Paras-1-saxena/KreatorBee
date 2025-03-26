# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#    See LICENSE file for full copyright and licensing details.
#################################################################################

import logging
import json
import requests
import pprint
from werkzeug import urls
from odoo import api, fields, models, _
from odoo.addons.payment.models.payment_provider import ValidationError, UserError
from odoo.addons.payment_instamojo_checkout.controllers.main import InstamojoCheckoutController
from odoo.addons.payment_instamojo_checkout import const
_logger = logging.getLogger(__name__)


class PaymentProviderInstamojoCheckout(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(selection_add=[('instamojo_checkout', 'Instamojo')], ondelete={'instamojo_checkout': 'set default'})
    instamojo_client_id = fields.Char(groups='base.group_user', string='Instamojo Client Id', required_if_provider='instamojo_checkout')
    instamojo_client_secret = fields.Char(groups='base.group_user', string='Instamojo Client Secret', required_if_provider='instamojo_checkout')

    def _get_default_payment_method_codes(self):
        """ Override of `payment` to return the default payment method codes. """
        default_codes = super()._get_default_payment_method_codes()
        if self.code != 'instamojo_checkout':
            return default_codes
        return const.DEFAULT_PAYMENT_METHOD_CODES
    
    def _get_payment_request_data(self, tx_data):
        reference = tx_data['reference']
        try:
            website = self.env['website'].sudo().get_current_website()
            base_url = website.get_base_url()
        except:
            base_url = self.get_base_url()
        data = {
            'purpose': reference,
            'amount': tx_data['amount'],
            'buyer_name': tx_data['billing_partner_name'],
            'email': tx_data['billing_partner_email'],
            'redirect_url': urls.url_join(base_url, InstamojoCheckoutController._return_url) + '?reference=%s' % reference,
            'send_email': False,
            # 'webhook': 'http://www.example.com/webhook/',
            'allow_repeated_payments': False,
        }
        return data

    def _get_access_token(self):
        api_end = 'https://api.instamojo.com/oauth2/token/' if self.state == 'enabled' else \
                    'https://api.test.instamojo.com/oauth2/token/'
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.instamojo_client_id,
            'client_secret': self.instamojo_client_secret,
        }
        try:
            result = requests.post(api_end,data=data)
            result_content = json.loads(result.content)
            _logger.info(f'\n Access Token Data {pprint.pformat(result_content)} \n')
            if result_content.get('error',False):
                raise UserError(result_content.get('error'))
            else:
                return result_content.get('access_token',False)
        except Exception as e:
            _logger.warning("#WKDEBUG---Instamojo Access Token----Exception-----%r---------" % (e))
            raise UserError(e)

    def _create_instamojo_payment_request(self, data, access_token):
        headers = { "Authorization": "Bearer " + access_token }
        api_end = "https://api.instamojo.com/v2/payment_requests/" if self.state == 'enabled' else \
                    "https://api.test.instamojo.com/v2/payment_requests/"
        try:
            result = requests.post(api_end,data=data,headers=headers)
            result_content = json.loads(result.content)
            _logger.info(f'\n Payment Request Data {pprint.pformat(result_content)} \n')
            if not result_content.get('status'):
                raise UserError(result_content.get('message'))
            else:
                return result_content
        except Exception as e:
            _logger.warning("#WKDEBUG---Instamojo Payment Request----Exception-----%r---------" % (e))
            raise UserError(e)

    def instamojo_checkout_form_generate_values(self, values):
        self.ensure_one()
        if values['currency'].name != 'INR':
            raise ValidationError('%s currency is not supported by instamojo payment gateway. Instamojo processes payments only in Indian Rupees (₹).'% (values['currency'].name))
        elif values.get('amount') > 200000:
            # https://docs.instamojo.com/reference/create-a-payment-request-1
            raise ValidationError('With Instamojo payment gateway you can pay a maximum of ₹2,00,000 in one transaction.')
        if values.get('amount') < 9:
            raise ValidationError('With Instamojo payment gateway you can pay a minimum of ₹9 in one transaction but your cart value is ₹{:.2f}, please choose another payment gateway or buy some more products.'.format(values.get('amount')))
        tx_data = self._get_payment_request_data(values)
        access_token = self._get_access_token()
        payment_request_data = self.sudo()._create_instamojo_payment_request(tx_data, access_token)
        values.update({'longurl': payment_request_data.get('longurl',False)})
        return values

    def _get_payment_status(self, data):
        headers = { "Authorization": "Bearer " + self._get_access_token()}
        payment_id = data.get('payment_id',False)
        if payment_id:
            api_end = "https://api.instamojo.com/v2/payments/" + payment_id if self.state == 'enabled' else \
                        "https://api.test.instamojo.com/v2/payments/" + payment_id
            try:
                result = requests.get(api_end,headers=headers)

                result_content = json.loads(result.content)
                _logger.info(f'\n Instamojo Payment Status {pprint.pformat(result_content)} \n')

                if not result_content.get('status'):
                    raise ValidationError("Instamojo: " + _("Payment Unsuccessfull reason: '%s' ",
                    result_content.get('failure')['reason']))
                    raise UserError(result_content.get('message'))
                else:
                    return result_content
            except Exception as e:
                _logger.warning("#WKDEBUG---Instamojo Payment Status----Exception-----%r---------" % (e))
                raise UserError(e)
        else:
            raise ValidationError(_("Issue in finding instamojo payment id"))    