# custom_module/controllers/referral.py
from cryptography.fernet import Fernet
import base64
import logging
import werkzeug
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

class ReferralController(http.Controller):
    @http.route('/creator/referral', type='http', auth='public', website=True)
    def nreferral_page(self, **kwargs):
        user_id = request.env.user
        partner_id = user_id.partner_id
        partner_ids = request.env['res.partner'].sudo().search([('user_type', '=', 'customer')])
        course_ids = request.env['slide.channel'].sudo().search([
            ('state', '=', 'published'),
            ('create_uid', '=', user_id.id)
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
        generated_by = user_id.partner_id
        course_id = kwargs.get('payment_course_id')
        partner_id = kwargs.get('payment_partner_id')
        expiry_time = kwargs.get('payment_expiry_time')
        try:
            website = self.env['website'].sudo().get_current_website()
            base_url = website.get_base_url()
        except:
            base_url = request.httprequest.host_url

        payment_redirect_url = base_url+'payment/instamojo/redirect'
        course_ids = request.env['slide.channel'].sudo().search([
            ('state', '=', 'published'),
            ('create_uid', '=', user_id.id)
            ])
        if not partner_id:
            print("Please select Customer")
        if not course_id:
            print("Please select Course")
        partner_id = request.env['res.partner'].sudo().search([('id', '=', partner_id)])
        expireOn = False
        current_time = int(time.time())
        if expiry_time == '5_minutes':
            expireOn = current_time + 300    # 5 minutes
        elif expiry_time == '15_minutes':
            expireOn = current_time + 900   # 15 minutes
        elif expiry_time == '30_minutes':
            expireOn = current_time + 1800   # 30 minutes
        else:
            expireOn = 315360000  # 10 years for unlimited
        
        product_id = request.env['slide.channel'].sudo().search([('id', '=', course_id)]).product_id
        print("Product ID:",product_id)
        order = request.env['sale.order'].sudo().create({
            'partner_id': partner_id.id,
            'partner_invoice_id': partner_id.id,
            'partner_shipping_id': partner_id.id,
            'order_line': [(0, 0, {
                'product_id': product_id.id,
                'name': product_id.name,
                'product_uom_qty': 1,
                'price_unit': product_id.list_price,
                'partner_commission_partner_id':generated_by.id,
            })],
            # 'expiry_time': datetime.datetime.now() + datetime.timedelta(hours=1)
        })
        print("Order ID:",order)
        print("Partner Name:",partner_id.name)
        print("Partner Email:",partner_id.email)
        referral_id = request.env['apg.course.referral'].sudo().create({
            'course_id':course_id,
            'partner_id': generated_by.id,
            'expiry_time': expireOn,
            'order_id': order.id,
            })
        print("Referral  ID:",referral_id)
        partner_name = partner_id.name
        partner_email = partner_id.email
        referral_id.generate_payment_link(order,partner_name,partner_email)
        
        key1 = request.env['ir.config_parameter'].sudo().get_param('apg_course_referral.apg_encryption_key')

        key = key1.encode('utf-8')  # Same as in controller
        cipher_suite = Fernet(key)


        if referral_id.payment_link:
            values = {
                'payment_referral_id': referral_id.id,
                'success': 'Success'  # Ensure 'success' has a valid value
            }

            params = {
                "order_id": order.id,
                "payment_link_id": referral_id.id
            }
            params_json = json.dumps(params)  # Convert dictionary to JSON string
            encrypted_bytes = cipher_suite.encrypt(params_json.encode('utf-8'))  # Encrypt JSON string
            encrypted_token = encrypted_bytes.decode('utf-8')  # Convert bytes to string

            full_url = f"{payment_redirect_url}?token={encrypted_token}"
            print("Generated Encrypted URL:", full_url)  # Debug print
            referral_id.sudo().write({'generated_url': full_url})

            query_string = url_encode(values)
            return request.redirect(f"/creator/referral?{query_string}")
            # return request.redirect("/creator/referral?success=%d" % values)
            # return {'success': True, 'message': 'Payment link generated successfully','referral_id':referral_id, 'course_ids': course_ids}
        return request.redirect("/creator/referral?success=%s" % 'failed')

        # return http.request.render('apg_course_referral.nreferral_link_page', values)


    @http.route('/partner-referral', type='http', auth='public', website=True)
    def partner_referral(self, **kwargs):
        user_id = request.env.user
        partner_id = user_id.partner_id
        course_ids = False
        courses = request.env['my.product.cart'].sudo().search([('partner_id', '=', partner_id.id)]).course_id.ids
        print("product_cart_ids",courses)
        partner_ids = request.env['res.partner'].sudo().search([('user_type', '=', 'customer')])
        if courses:
            course_ids = request.env['slide.channel'].sudo().search([
                ('id', 'in', courses),
                ('state', '=', 'published')
                ])
        if kwargs.get('success') == 'Success':
            payment_referral_id = request.env['apg.course.referral'].sudo().search([('id', '=', kwargs.get('payment_referral_id'))])
            values = {
                'course_ids': course_ids,
                'partner_ids': partner_ids,
                'payment_referral_id': payment_referral_id,

            }
            # Render the data page template
            return http.request.render('apg_course_referral.partner_referral_link_page', values)
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
                    'partner_ids': partner_ids,
                }
                return http.request.render('apg_course_referral.partner_referral_link_page', values)
        values = {
            'product_cart_ids': course_ids,
            'partner_ids': partner_ids,
        }
        # Render the data page template
        return http.request.render('apg_course_referral.partner_referral_link_page', values)

    
    @http.route('/partner/payment/link', type='http', auth='public', website=True)
    def partner_payment_link(self, **kwargs):
        user_id = request.env.user
        generated_by = user_id.partner_id
        course_id = kwargs.get('payment_course_id')
        partner_id = kwargs.get('payment_partner_id')
        expiry_time = kwargs.get('payment_expiry_time')
        try:
            website = self.env['website'].sudo().get_current_website()
            base_url = website.get_base_url()
        except:
            base_url = request.httprequest.host_url
        payment_redirect_url = base_url+'payment/instamojo/redirect'
        if not partner_id:
            print("Please select Customer")
        if not course_id:
            print("Please select Course")
        partner_id = request.env['res.partner'].sudo().search([('id', '=', partner_id)])
        expireOn = False
        if expiry_time == '5_minutes':
            expireOn = 300    # 5 minutes
        elif expiry_time == '15_minutes':
            expireOn = 900   # 15 minutes
        elif expiry_time == '30_minutes':
            expireOn = 1800   # 30 minutes
        else:
            expireOn = 315360000  # 10 years for unlimited
        
        product_id = request.env['slide.channel'].sudo().search([('id', '=', course_id)]).product_id
        print("Product ID:",product_id)
        order = request.env['sale.order'].sudo().create({
            'partner_id': partner_id.id,
            'partner_invoice_id': partner_id.id,
            'partner_shipping_id': partner_id.id,
            'order_line': [(0, 0, {
                'product_id': product_id.id,
                'name': product_id.name,
                'product_uom_qty': 1,
                'price_unit': product_id.list_price,
                'partner_commission_partner_id': generated_by.id,
            })],
            # 'expiry_time': datetime.datetime.now() + datetime.timedelta(hours=1)
        })
        print("Order ID:",order)
        print("Partner Name:",partner_id.name)
        print("Partner Email:",partner_id.email)
        referral_id = request.env['apg.course.referral'].sudo().create({
            'course_id':course_id,
            'partner_id': generated_by.id,
            'expiry_time': expireOn,
            'order_id': order.id,
            })
        print("Referral  ID:",referral_id)
        partner_name = partner_id.name
        partner_email = partner_id.email
        referral_id.generate_payment_link(order,partner_name,partner_email)
        key1 = request.env['ir.config_parameter'].sudo().get_param('apg_course_referral.apg_encryption_key')

        key = key1.encode('utf-8')  # Same as in controller
        cipher_suite = Fernet(key)

        if referral_id.payment_link:
            values = {
                'payment_referral_id': referral_id.id,
                'success': 'Success'  # Ensure 'success' has a valid value
            }

            params = {
                "order_id": order.id,
                "payment_link_id": referral_id.id
            }
            params = {
                "order_id": order.id,
                "payment_link_id": referral_id.id
            }
            params_json = json.dumps(params)  # Convert dictionary to JSON string
            encrypted_bytes = cipher_suite.encrypt(params_json.encode('utf-8'))  # Encrypt JSON string
            encrypted_token = encrypted_bytes.decode('utf-8')  # Convert bytes to string
            full_url = f"{payment_redirect_url}?token={encrypted_token}"
            
            referral_id.sudo().write({'generated_url': full_url})

            query_string = url_encode(values)
            return request.redirect(f"/partner-referral?{query_string}")
            # return request.redirect("/creator/referral?success=%d" % values)
            # return {'success': True, 'message': 'Payment link generated successfully','referral_id':referral_id, 'course_ids': course_ids}
        return request.redirect("/partner-referral?success=%s" % 'failed')

        # return http.request.render('apg_course_referral.nreferral_link_page', values)

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
            encrypt_expiry = [f"{x}{''.join(random.choices(string.ascii_letters + string.digits, k=2))}" for x in str(expiry_time)]
            encrypt_expiry = ''.join(encrypt_expiry)
            course_url = f"{course_url}&course_name={encrypt_expiry}"
            return request.redirect(course_url)
        except Exception as e:
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
        return request.redirect('/partner/product')

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
