from cryptography.fernet import Fernet
from odoo import api, registry, SUPERUSER_ID, tools

def set_encryption_key(env):
    print("\n\n\n>>>>>once time 0<<<<<<<<<<<<",env['ir.config_parameter'].sudo().get_param('apg_course_referral.apg_encryption_key'))
    # env = api.Environment(cr, SUPERUSER_ID, {})
    if not env['ir.config_parameter'].sudo().get_param('apg_course_referral.apg_encryption_key'):
        print("\n\n\n>>>>>once time 1<<<<<<<<<<<<")
        key = Fernet.generate_key().decode('utf-8')  # Generate and decode key
        env['ir.config_parameter'].sudo().set_param('apg_course_referral.apg_encryption_key', key)

def uninstall_encryption_key(env):
    print("\n\n\n>>>>>unlink-0<<<<<<<<<<<<")
    # env = api.Environment(cr, SUPERUSER_ID, {})
    key_param = 'apg_course_referral.apg_encryption_key'
    param = env['ir.config_parameter'].sudo().search([('key', '=', key_param)], limit=1)
    if param:
        print("\n\n\n>>>>>unlink-1<<<<<<<<<<<<",param)
        param.sudo().unlink()

from . import models
from . import controllers