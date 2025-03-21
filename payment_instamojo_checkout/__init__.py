# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#################################################################################

from . import models
from . import controllers
from odoo.addons.payment import setup_provider, reset_payment_provider

def pre_init_check(cr):
	from odoo.exceptions import UserError
	from odoo.service import common
	server_serie = common.exp_version().get('server_serie')
	if not server_serie == '18.0':
		raise UserError(f'Module support Odoo series 18.0 but found {server_serie}.')

def post_init_hook(env):
    setup_provider(env, 'instamojo_checkout')


def uninstall_hook(env):
    reset_payment_provider(env, 'instamojo_checkout')