# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#    See LICENSE file for full copyright and licensing details.
#################################################################################

import logging
import pprint
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class InstamojoCheckoutController(http.Controller):
    _return_url = '/payment/instamojo/return'

    @http.route([_return_url], type='http', auth='public', csrf=False, save_session=False)
    def instamojo_return(self, **post):
        reference = post.get('reference',False)
        print("\n\n\n=========reference=========",reference)
        if reference:
            tx = request.env['payment.transaction'].sudo().search([('reference', '=', reference)], limit=1)
            print("\n\n\n=========post=========",post)
            data = tx.provider_id._get_payment_status(post)
            data.update({'tx':tx})
            _logger.info('Instamojo: entering form_feedback with post data %s', pprint.pformat(data))
            request.env['payment.transaction'].sudo()._handle_notification_data('instamojo_checkout',data)
        return request.redirect('/payment/status')
