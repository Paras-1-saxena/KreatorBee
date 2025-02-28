# -*- coding: utf-8 -*-
from odoo import models, fields, api, Command, _
from cryptography.fernet import Fernet
import base64
import time

class CourseReferral(models.Model):
    _name = 'apg.course.referral'
    _description = 'Course Referral'
    _rec_name = 'course_id'

    course_id = fields.Many2one('slide.channel', string="Course")
    expiry_time = fields.Char('Expiry Time')
    website_url = fields.Char(string="Cours Url", related='course_id.website_url')
    partner_id = fields.Many2one('res.partner', string="Partner", ondelete="cascade")
    generated_url = fields.Char(string="URL")
    
    def generate_referral_link(self):
        key1 = self.env['ir.config_parameter'].sudo().get_param('apg_course_referral.apg_encryption_key')
        key = key1.encode('utf-8')  # Same as in controller
        cipher_suite = Fernet(key)
        course_id = str(self.course_id.id)
        partner_id = str(self.partner_id.id)
        course_url = str(self.website_url)
        expiry_time = int(time.time()) + int(self.expiry_time)
        data = f"{course_id}|{partner_id}|{course_url}|{expiry_time}"
        encrypted_bytes = cipher_suite.encrypt(data.encode('utf-8'))
        encrypted_token = base64.urlsafe_b64encode(encrypted_bytes).decode('utf-8')
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        self.generated_url = f"{base_url}/referral/{encrypted_token}"
        # return f"{base_url}/referral/{encrypted_token}"

class MyProductCart(models.Model):
    _inherit = 'my.product.cart'
    _description = 'My Product Cart'

    referral_id = fields.Many2one('apg.course.referral')