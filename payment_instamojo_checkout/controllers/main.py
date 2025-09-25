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
            tx._post_process_after_done()
            data.update({'tx':tx})
            _logger.info('Instamojo: entering form_feedback with post data %s', pprint.pformat(data))
            tx.sudo()._handle_notification_data('instamojo_checkout',data)
        return request.redirect('/payment/status')
