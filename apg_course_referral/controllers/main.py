# custom_module/controllers/referral.py
from cryptography.fernet import Fernet
import base64
import logging
import werkzeug
from werkzeug.urls import url_encode
import requests
import time
from odoo import http, tools, _
from odoo import fields
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.payment.controllers import portal as payment_portal
from odoo.exceptions import UserError, ValidationError
from odoo.http import request, route
import odoo.exceptions
from odoo.exceptions import AccessError
from odoo.service import security
from odoo.tools.translate import _

class ReferralController(http.Controller):
    @http.route('/nreferral', type='http', auth='public', website=True)
    def nreferral_page(self, **kwargs):
        user_id = request.env.user
        partner_id = user_id.partner_id
        course_ids = request.env['slide.channel'].sudo().search([
            ('state', '=', 'published'),
            ('create_uid', '=', user_id.id)
            ])
        if request.httprequest.method == 'POST':
            course_id = kwargs.get('course_id')
            expiry_time = kwargs.get('expiry_time')
            expireOn = False
            if expiry_time == '5_minutes':
                expireOn = 300    # 5 minutes
            elif expiry_time == '15_minutes':
                expireOn = 900   # 15 minutes
            elif expiry_time == '30_minutes':
                expireOn = 1800   # 30 minutes
            else:
                expireOn = 315360000  # 10 years for unlimited
            if course_id:
                course_id = request.env['slide.channel'].sudo().search([('id', '=', course_id)])
                referral_id = request.env['apg.course.referral'].sudo().create({
                    'course_id':course_id.id,
                    'partner_id': partner_id.id,
                    'expiry_time': expireOn,
                    })
                referral_id.generate_referral_link()
                values = {
                    'course_ids': course_ids,
                    'referral_id': referral_id,
                }
                return http.request.render('apg_course_referral.nreferral_link_page', values)

        values = {
            'course_ids': course_ids,
        }
        # Render the data page template
        return http.request.render('apg_course_referral.nreferral_link_page', values)

    @http.route('/partner-referral', type='http', auth='public', website=True)
    def partner_referral(self, **kwargs):
        user_id = request.env.user
        partner_id = user_id.partner_id
        course_ids = False
        courses = request.env['my.product.cart'].sudo().search([('partner_id', '=', partner_id.id)]).course_id.ids
        print("product_cart_ids",courses)
        if courses:
            course_ids = request.env['slide.channel'].sudo().search([
                ('id', 'in', courses),
                ('state', '=', 'published')
                ])
        if request.httprequest.method == 'POST':
            course_id = kwargs.get('course_id')
            expiry_time = kwargs.get('expiry_time')
            expireOn = False
            if expiry_time == '5_minutes':
                expireOn = 300    # 5 minutes
            elif expiry_time == '15_minutes':
                expireOn = 900   # 15 minutes
            elif expiry_time == '30_minutes':
                expireOn = 1800   # 30 minutes
            else:
                expireOn = 315360000  # 10 years for unlimited
            if course_id:
                course_id = request.env['slide.channel'].sudo().search([('id', '=', course_id)])
                referral_id = request.env['apg.course.referral'].sudo().create({
                    'course_id':course_id.id,
                    'partner_id': partner_id.id,
                    'expiry_time': expireOn,
                    })
                referral_id.generate_referral_link()
                values = {
                    'product_cart_ids': course_ids,
                    'referral_id': referral_id,
                }
                return http.request.render('apg_course_referral.partner_referral_link_page', values)
        values = {
            'product_cart_ids': course_ids,
        }
        # Render the data page template
        return http.request.render('apg_course_referral.partner_referral_link_page', values)

    @http.route(['/referral/<string:token>'], type='http', auth='public', website=True)
    def referral(self, token, **kwargs):
        encryption_key = request.env['ir.config_parameter'].sudo().get_param('apg_course_referral.apg_encryption_key').encode('utf-8')  # 32-byte key
        try:
            decrypted_data = self.decrypt_data(token, encryption_key)
            course_id, partner_id, course_url, expiry_time = decrypted_data.split('|')
            request.session['referral_course'] = course_id
            request.session['referral_partner'] = partner_id
            current_time = int(time.time())
            if current_time > int(expiry_time):
                return '''
                    <script>
                        alert("This referral link has expired.");
                        setTimeout(function() {
                            window.location.href = '/404';
                        }, 1000);  // Redirect after 1 seconds
                    </script>
                '''
                # return request.redirect(course_url)
            # Store expiry time in session for frontend validation
            request.session['link_expiry_time'] = expiry_time
            # Store access session
            request.session['course_access'] = {
                'course_id': int(course_id),
                'partner_id': int(partner_id)
            }
            return request.redirect(course_url)
        except Exception as e:
            return "Invalid or expired referral link."

    def decrypt_data(self, encrypted_text, encryption_key):
        cipher_suite = Fernet(encryption_key)
        decrypted_bytes = cipher_suite.decrypt(base64.urlsafe_b64decode(encrypted_text))
        return decrypted_bytes.decode('utf-8')

    @http.route('/delete-session-key', type='json', auth="public")
    def delete_session_key(self):
        if 'link_expiry_time' in request.session:
            print("Link Expiry Time",request.session['link_expiry_time'])
            del request.session['link_expiry_time']  # Delete session key
        if 'course_access' in request.session:
            del request.session['course_access']
        return {"message": "Session key deleted"}

    @http.route('/add-to-cart', type='http', auth="user", methods=['POST'], csrf=False)
    def add_to_cart(self, **kwargs):
        current_user = request.env.user
        partner = current_user.partner_id
        course_id = kwargs.get("courseId")
        expiry_time = kwargs.get('expiry_time')
        expireOn = 315360000  # 10 years for unlimited
        course_id = request.env['slide.channel'].sudo().search([('id', '=', course_id)])
        if course_id:
            referral_id = request.env['apg.course.referral'].sudo().create({
                'course_id':course_id.id,
                'partner_id': partner.id,
                'expiry_time': expireOn,
                })
            referral_id.generate_referral_link()
            my_cart_id = request.env['my.product.cart'].sudo().create({
                'course_id': course_id.id,
                'partner_id': partner.id,
                'referral_id': referral_id.id,
                })
        return request.redirect('/choose-product')

class WebsiteSale(payment_portal.PaymentPortal):
    @route(['/shop/cart'], type='http', auth="public", website=True, sitemap=False)
    def cart(self, access_token=None, revive='', **post):
        response = super().cart(access_token=None, revive='', **post)
        order = request.website.sale_get_order()
        referral_course = False
        referral_partner = False 
        user = request.env.user
        if user and user.id != request.website.user_id.id:
            if request.session.get('referral_course'):
                referral_course = request.session.get('referral_course')
                del request.session['referral_course']  # Clear session value after use
            if request.session.get('referral_partner'):
                referral_partner = request.session.get('referral_partner')
                del request.session['referral_partner']
            if 'link_expiry_time' in request.session:
                del request.session['link_expiry_time']  # Delete session key
            if 'course_access' in request.session:
                del request.session['course_access']
            if order:
                for line in order.order_line:
                    line.partner_commission_partner_id = int(referral_partner)
        return response
