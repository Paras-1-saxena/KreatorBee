# custom_module/controllers/referral.py
from cryptography.fernet import Fernet
import base64
import logging
import werkzeug
from reportlab.lib.pagesizes import elevenSeventeen
from werkzeug.urls import url_encode
import requests
import time
import json
import urllib.parse
from werkzeug import urls
from odoo import http, tools, _
from odoo import fields
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.payment.controllers import portal as payment_portal
from odoo.exceptions import UserError, ValidationError
from datetime import date, datetime, timedelta
from odoo.http import request, route
import odoo.exceptions
from odoo.exceptions import AccessError
from odoo.service import security 
from odoo.tools.translate import _
import random
import string
from markupsafe import Markup

_logger = logging.getLogger(__name__)

class ReferralController(http.Controller):
    @http.route('/creator/referral', type='http', auth='public', website=True)
    def nreferral_page(self, **kwargs):
        user_id = request.env.user
        partner_id = user_id.partner_id
        partner_ids = request.env['res.partner'].sudo().search([('user_type', '=', 'customer')])
        course_ids = request.env['slide.channel'].sudo().search([
            ('state', '=', 'published'),
            ('create_uid', '=', user_id.id),
            ('not_display', '=', False)
            ])
        if kwargs.get('success') == 'Success':
            payment_referral_id = request.env['apg.course.referral'].sudo().search([('id', '=', kwargs.get('payment_referral_id'))])
            values = {
                'course_ids': course_ids,
                'partner_ids': partner_ids,
                'payment_referral_id': payment_referral_id,

            }
            # Render the data page template
            return http.request.render('apg_course_referral.nreferral_link_page', values)
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
                    'partner_ids': partner_ids, 
                }
                return http.request.render('apg_course_referral.nreferral_link_page', values)

        values = {
            'course_ids': course_ids,
            'partner_ids': partner_ids, 
        }
        # Render the data page template
        return http.request.render('apg_course_referral.nreferral_link_page', values)

    @http.route('/creator/payment/link', type='http', auth='public', website=True)
    def creator_payment_link(self, **kwargs):
        user_id = request.env.user
        partner_id = user_id.partner_id
        course_ids = request.env['slide.channel'].sudo().search([
            ('state', '=', 'published'),
            ('create_uid', '=', user_id.id),
            ('not_display', '=', False)
        ])
        if kwargs.get('success') == 'Success':
            payment_referral_id = request.env['apg.course.referral'].sudo().search(
                [('id', '=', kwargs.get('payment_referral_id'))])
            values = {
                'course_ids': course_ids,
                'payment_referral_id': payment_referral_id,

            }
            # Render the data page template
            return http.request.render('apg_course_referral.nreferral_link_page', values)
        if request.httprequest.method == 'POST':
            course_id = kwargs.get('payment_course_id')
            expiry_time = kwargs.get('payment_expiry_time')
            expireOn = False
            if expiry_time == '5_minutes':
                expireOn = 300  # 5 minutes
            elif expiry_time == '15_minutes':
                expireOn = 900  # 15 minutes
            elif expiry_time == '30_minutes':
                expireOn = 1800  # 30 minutes
            else:
                expireOn = 315360000  # 10 years for unlimited
            if course_id:
                course_id = request.env['slide.channel'].sudo().search([('id', '=', course_id)])
                referral_id = request.env['apg.course.referral'].sudo().create({
                    'course_id': course_id.id,
                    'partner_id': partner_id.id,
                    'stage_id': int(kwargs.get('stage_id')) if kwargs.get('stage_id') else False,
                    'expiry_time': expireOn,
                })
                referral_id.generate_payment_link()
                values = {
                    'course_ids': course_ids,
                    'payment_referral_id': referral_id,
                }
                return http.request.render('apg_course_referral.nreferral_link_page', values)
        values = {
            'course_ids': course_ids,
        }
        tutorial_video = Markup("""
                                    <iframe src="https://player.vimeo.com/video/1073824076?badge=0&amp;autopause=0&amp;player_id=0&amp;app_id=58479"
                                     frameborder="0" allow="autoplay; fullscreen; picture-in-picture; clipboard-write; encrypted-media"
                                      style="width:60vw;;height:40vh;" title="Sales+Product"></iframe>
                                    """)
        values.update({'tutorial_video': tutorial_video})
        # Render the data page template
        return http.request.render('apg_course_referral.nreferral_link_page', values)

        # return http.request.render('apg_course_referral.nreferral_link_page', values)

    @http.route('/check/upgrade', type='http', auth='public', website=True, csrf=False)
    def checkUpgrade(self, **kwargs):
        course_id = request.env['slide.channel'].sudo().search([('id', '=', int(kwargs.get('course_id')))]) if kwargs.get('course_id') else False
        if course_id and course_id.is_upgradable:
            upgrade_options = {}
            for stage in course_id.upgrade_stage_ids:
                if request.env.user.partner_id.user_type == 'creator' or not [False for prd in stage.product_ids.ids if prd not in request.env.user.partner_id.slide_channel_ids.product_id.ids] or (request.env.user.id in course_id.user_ids.ids):
                    upgrade_options.update({stage.id: stage.name})
            if upgrade_options:
                return request.make_response(
                    data=json.dumps({'response': "yes", 'upgrade_options': upgrade_options}),
                    headers=[('Content-Type', 'application/json')],
                    status=200
                )
            else:
                return request.make_response(
                    data=json.dumps({'response': "No"}),
                    headers=[('Content-Type', 'application/json')],
                    status=200
                )
        else:
            return request.make_response(
                data=json.dumps({'response': "No"}),
                headers=[('Content-Type', 'application/json')],
                status=200
            )

    @http.route('/partner-referral', type='http', auth='public', website=True)
    def partner_referral(self, **kwargs):
        user_id = request.env.user
        partner_id = user_id.partner_id
        is_active_subscription = False
        partner = request.env.user.partner_id  # Get related partner

        subscription = partner.subscription_product_line_ids.subscription_id.filtered(
            lambda sub: sub.stage_id.name == 'In Progress')
        expire_on = False
        if subscription and subscription.next_invoice_date >= datetime.today().date():
            is_active_subscription = True
        expire_on = request.env['subscription.package'].sudo().search([
            ('partner_id', '=', partner_id.id),
            ('stage_id.name', 'in', ['In Progress', 'Draft'])
        ], order='id desc', limit=1).next_invoice_date
        end_days = -1
        # if (datetime.today().date() - timedelta(days=2)) < partner.create_date.date() and not partner.early_sign_in:
        #     return request.redirect('/partner/income')
        if subscription:
            end_days = (subscription.next_invoice_date - datetime.today().date()).days
        # if not request.env.user.partner_id.early_sign_in and (
        #         premium_course.id not in request.env.user.partner_id.slide_channel_ids.ids):
        #     return request.redirect('/partner-welcome')
        if not is_active_subscription:
            request.env['apg.course.referral'].sudo().search([('partner_id', '=', partner_id.id)]).unlink()
            return request.redirect('/partner-welcome')
        # course_ids = False
        course_ids = request.env['product.template'].sudo().search([('bom_ids', '!=', False)])
        partner_ids = request.env['res.partner'].sudo().search([('user_type', '=', 'customer')])
        # Get only confirmed sale order lines (exclude draft/quotation)
        confirmed_orders = request.env.user.partner_id.sale_order_ids.filtered(lambda so: so.state in ['sale', 'done'])
        
        course_count = len(confirmed_orders.order_line.filtered(lambda line: line.product_id.bom_ids).product_id)
        # if courses:
        #     course_ids = request.env['slide.channel'].sudo().search([
        #         ('id', 'in', courses),
        #         ('state', '=', 'published'),
        #         ('not_display', '=', False)
        #         ])
        if kwargs.get('success') == 'Success':
            payment_referral_id = request.env['apg.course.referral'].sudo().search([('id', '=', kwargs.get('payment_referral_id'))])
            values = {
                'product_cart_ids': course_ids,
                'partner_ids': partner_ids,
                'payment_referral_id': payment_referral_id,
                'course_count': course_count,
                'end_days': end_days,
                'expire_on': expire_on
            }
            # Render the data page template
            return http.request.render('apg_course_referral.partner_referral_link_page', values)
        if request.httprequest.method == 'POST':
            course_id = request.httprequest.form.getlist('course_id')
            expiry_time = kwargs.get('expiry_time')
            # expireOn = False
            # if expiry_time == '5_minutes':
            #     expireOn = 300    # 5 minutes
            # elif expiry_time == '15_minutes':
            #     expireOn = 900   # 15 minutes
            # elif expiry_time == '30_minutes':
            #     expireOn = 1800   # 30 minutes
            # else:
            expireOn = 315360000  # 10 years for unlimited
            if course_id:
                course_id = request.env['product.template'].sudo().search([('id', 'in', course_id)])
                referral_id = request.env['apg.course.referral'].sudo().create({
                    'course_id':[(4, c.id) for c in course_id],
                    'partner_id': partner_id.id,
                    'stage_id': int(kwargs.get('stage_id')) if kwargs.get('stage_id') else False,
                    'expiry_time': expireOn,
                    })
                referral_id.generate_referral_link()
                values = {
                    'product_cart_ids': course_ids,
                    'referral_id': referral_id,
                    'partner_ids': partner_ids,
                    'course_count': course_count,
                    'end_days': end_days,
                    'expire_on': expire_on
                }
                return http.request.render('apg_course_referral.partner_referral_link_page', values)
        values = {
            'product_cart_ids': course_ids,
            'partner_ids': partner_ids,
            'course_count': course_count,
            'end_days': end_days,
            'expire_on': expire_on
        }
        tutorial_video = Markup("""
                    <iframe src="https://player.vimeo.com/video/1073824076?badge=0&amp;autopause=0&amp;player_id=0&amp;app_id=58479"
                     frameborder="0" allow="autoplay; fullscreen; picture-in-picture; clipboard-write; encrypted-media"
                      style="width:60vw;;height:40vh;" title="Sales+Product"></iframe>
                    """)
        values.update({'tutorial_video': tutorial_video})        # Render the data page template
        return http.request.render('apg_course_referral.partner_referral_link_page', values)

    
    @http.route('/partner/payment/link', type='http', auth='public', website=True)
    def partner_payment_link(self, **kwargs):
        user_id = request.env.user
        partner_id = user_id.partner_id
        course_ids = False
        courses = request.env['my.product.cart'].sudo().search([('partner_id', '=', partner_id.id)]).course_id.ids
        print("product_cart_ids", courses)
        # partner_ids = request.env['res.partner'].sudo().search([('user_type', '=', 'customer')])
        if courses:
            course_ids = request.env['slide.channel'].sudo().search([
                ('id', 'in', courses),
                ('state', '=', 'published')
                , ('not_display', '=', False)
            ])
        if kwargs.get('success') == 'Success':
            payment_referral_id = request.env['apg.course.referral'].sudo().search(
                [('id', '=', kwargs.get('payment_referral_id'))])
            values = {
                'product_cart_ids': course_ids,
                'payment_referral_id': payment_referral_id,
            }
            # Render the data page template
            return http.request.render('apg_course_referral.partner_referral_link_page', values)
        if request.httprequest.method == 'POST':
            course_id = kwargs.get('payment_course_id')
            expiry_time = kwargs.get('payment_expiry_time')
            expireOn = False
            if expiry_time == '5_minutes':
                expireOn = 300  # 5 minutes
            elif expiry_time == '15_minutes':
                expireOn = 900  # 15 minutes
            elif expiry_time == '30_minutes':
                expireOn = 1800  # 30 minutes
            else:
                expireOn = 315360000  # 10 years for unlimited
            if course_id:
                course_id = request.env['slide.channel'].sudo().search([('id', '=', course_id)])
                referral_id = request.env['apg.course.referral'].sudo().create({
                    'course_id': course_id.id,
                    'partner_id': partner_id.id,
                    'stage_id': int(kwargs.get('stage_id')) if kwargs.get('stage_id') else False,
                    'expiry_time': expireOn,
                })
                referral_id.generate_payment_link()
                values = {
                    'product_cart_ids': course_ids,
                    'payment_referral_id': referral_id,
                }
                return http.request.render('apg_course_referral.partner_referral_link_page', values)
        values = {
            'product_cart_ids': course_ids,
        }
        tutorial_video = Markup("""
                            <iframe src="https://player.vimeo.com/video/1073824076?badge=0&amp;autopause=0&amp;player_id=0&amp;app_id=58479"
                             frameborder="0" allow="autoplay; fullscreen; picture-in-picture; clipboard-write; encrypted-media"
                              style="width:60vw;;height:40vh;" title="Sales+Product"></iframe>
                            """)
        values.update({'tutorial_video': tutorial_video})
        # Render the data page template
        return http.request.render('apg_course_referral.partner_referral_link_page', values)

        # return http.request.render('apg_course_referral.nreferral_link_page', values)

    @http.route(['/referral/<string:token>'], type='http', auth='public', website=True)
    def referral(self, token, **kwargs):
        encryption_key = request.env['ir.config_parameter'].sudo().get_param('apg_course_referral.apg_encryption_key').encode('utf-8')  # 32-byte key
        try:
            decrypted_data = self.decrypt_data(token, encryption_key)
            course_id, partner_id, course_url, expiry_time, stage_id = decrypted_data.split('|')
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
                'course_id': course_id,
                'partner_id': int(partner_id)
            }
            encrypt_expiry = [f"{x}{''.join(random.choices(string.ascii_letters + string.digits, k=2))}" for x in str(expiry_time)]
            encrypt_expiry = ''.join(encrypt_expiry)
            # if stage_id != 'False':
            #     stage_id = request.env['slide.channel.upgrade.stage'].browse(int(stage_id))
            #     course_url = f"{request.env['ir.config_parameter'].sudo().get_param('web.base.url')}/landing/page/{stage_id.landing_page_record_id.lading_id}?course_id={int(course_id)}&course_name={encrypt_expiry}"
            # else:
            course_url = f"/product/referral/page?courses={course_id}&course_name={encrypt_expiry}"
            return request.redirect(course_url)
        except Exception as e:
            return "Invalid or expired referral link."

    @http.route(['/payment/<string:token>'], type='http', auth='public', website=True)
    def payment_redirect(self, token, **kwargs):
        link_tracker_obj = request.env['referral.tracker']
        encryption_key = request.env['ir.config_parameter'].sudo().get_param(
            'apg_course_referral.apg_encryption_key').encode('utf-8')  # 32-byte key
        try:
            decrypted_data = self.decrypt_data(token, encryption_key)
            course_id, partner_id, course_url, expiry_time, stage_id = decrypted_data.split('|')
            request.session['referral_course'] = course_id
            request.session['referral_partner'] = partner_id
            current_time = int(time.time())
            channel_id = request.env['slide.channel'].sudo().search([('id', '=', course_id)], limit=1)
            if current_time > int(expiry_time):
                return '''
                        <script>
                            alert("This Payment link has expired.");
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
            mode = kwargs.get('mode')
            tracker_value = {}
            if stage_id != 'False':
                stage_id = request.env['slide.channel.upgrade.stage'].browse(int(stage_id))
                tracker_value.update({'variant': stage_id.name})
                # course_url = f"{request.env['ir.config_parameter'].sudo().get_param('web.base.url')}/shop/cart/update/?course_id={int(course_id)}"
                action = odoo.addons.elearning_upgradable_courses.controllers.main.WebsiteSaleCustom.cart_update(self=False, product_id=channel_id.product_id.id, **{'option': stage_id.name})
            else:
                action = odoo.addons.elearning_upgradable_courses.controllers.main.WebsiteSaleCustom.cart_update(self=False, product_id=channel_id.product_id.id)
            if mode:
                tracker_value.update({'name': mode, 'course': channel_id.name})
                link_tracker_obj.sudo().create(tracker_value)
            return action
        except Exception as e:
            _logger.info(f"{'*'*50} {e}")
            return "Invalid or expired referral link."

    @http.route('/payment/instamojo/redirect', type='http', auth='public', website=True)
    def instamojo_redirect(self, token=None, **kwargs):
        """Redirects customer to the actual Instamojo payment page after checking expiry"""
        if not token:
            return "Error: Missing token"
        key1 = request.env['ir.config_parameter'].sudo().get_param('apg_course_referral.apg_encryption_key')
        if not key1:
            return "Error: Encryption key not found"
        try:
            key = key1.encode('utf-8')
            cipher_suite = Fernet(key)

            # Decode and decrypt the token
            encrypted_bytes = token.encode('utf-8')  # Convert to bytes
            decrypted_bytes = cipher_suite.decrypt(encrypted_bytes)  # Decrypt
            decrypted_text = decrypted_bytes.decode('utf-8')  # Convert to string

            # Convert JSON string back to dictionary
            params = json.loads(decrypted_text)
            order_id = params.get("order_id")
            payment_link_id = params.get("payment_link_id")

            if not payment_link_id:
                return request.redirect("/404")  # Redirect to an error page

            order = request.env['apg.course.referral'].sudo().browse(int(payment_link_id))

            # Check if payment link has expired
            
            current_time = int(time.time())  # Get current timestamp
            expiry_time = int(order.expiry_time)  # Ensure expiry_time is stored as a timestamp


            # if current_time > expiry_time:
            #     return request.redirect("/404")

            # Redirect to Instamojo payment page
            return f"""
                <html>
                <head>
                    <meta http-equiv="refresh" content="0;url={order.payment_link}">
                </head>
                <body>
                    <p>Redirecting to <a href="{order.payment_link}">payment page</a>...</p>
                </body>
                </html>
                """
        except Exception as e:
            return f"Decryption Error: {str(e)}"
    
        # return request.redirect('https://www.instamojo.com/@paras9/f11375dc96f74e1db2e8d69da167e1d3')
        # return request.redirect(order.payment_link)

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
                'course_id': [(4, course_id.id)],
                'partner_id': partner.id,
                'expiry_time': expireOn,
                })
            referral_id.generate_referral_link()
            my_cart_id = request.env['my.product.cart'].sudo().create({
                'course_id': course_id.id,
                'partner_id': partner.id,
                'referral_id': referral_id.id,
                })
        return request.redirect('/partner/product')

class WebsiteSale(payment_portal.PaymentPortal):
    @route(['/shop/cart'], type='http', auth="public", website=True, sitemap=False)
    def cart(self, access_token=None, revive='', **post):
        response = super().cart(access_token=None, revive='', **post)
        order = request.website.sale_get_order()
        referral_course = False
        referral_partner = False 
        user = request.env.user
        # if user and user.id != request.website.user_id.id:
        #     if request.session.get('referral_course'):
        #         referral_course = request.session.get('referral_course')
        #         del request.session['referral_course']  # Clear session value after use
        #     if request.session.get('referral_partner'):
        #         referral_partner = request.session.get('referral_partner')
        #         # del request.session['referral_partner']
        #     if 'link_expiry_time' in request.session:
        #         del request.session['link_expiry_time']  # Delete session key
        #     if 'course_access' in request.session:
        #         del request.session['course_access']
        #     if order:
        #         for line in order.order_line:
        #             line.partner_commission_partner_id = int(referral_partner)
        return response
