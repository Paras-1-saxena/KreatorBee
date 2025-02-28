import logging
import werkzeug
from werkzeug.urls import url_encode
import requests
from odoo import http, tools, _
from odoo import fields
from odoo.addons.auth_signup.models.res_users import SignupError
from odoo.addons.web.controllers.home import ensure_db, Home, SIGN_UP_REQUEST_PARAMS, LOGIN_SUCCESSFUL_PARAMS
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.payment.controllers import portal as payment_portal
from odoo.addons.base_setup.controllers.main import BaseSetup
from odoo.exceptions import UserError, ValidationError
from odoo.http import request, route
from markupsafe import Markup
import odoo.exceptions
import odoo.modules.registry
from odoo.exceptions import AccessError
from odoo.service import security
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)

class AuthSignupHome(Home):
    @http.route()
    def web_login(self, *args, **kw):
        print("cominggggggg login")
        ensure_db()
        response = super().web_login(*args, **kw)
        partner_id = False
        response.qcontext.update(self.get_auth_signup_config())
        redirect_url = request.session.get('redirect_after_signup')
        if request.session.uid:
            partner_id = request.env['res.users'].sudo().browse(request.session.uid).partner_id
            if request.httprequest.method == 'GET' and request.params.get('redirect'):
                # Redirect if already logged in and redirect param is present
                return request.redirect(request.params.get('redirect'))
            # Add message for non-internal user account without redirect if account was just created
            if response.location == '/web/login_successful' and kw.get('confirm_password'):
                return request.redirect_query('/web/login_successful', query={'account_created': True})
        if partner_id:
            if partner_id.user_type == 'creator':
                return request.redirect('/master')
            elif partner_id.user_type == 'partner':
                return request.redirect('/partner')
            elif partner_id.user_type == 'customer':
                if redirect_url:
                    del request.session['redirect_after_signup']  # Clear session value after use
                    return request.redirect(redirect_url)
                else:
                    return request.redirect('/customer')
            else:
                return request.redirect('/')
        return response

    @http.route('/web/signup', type='http', auth='public', website=True, sitemap=False, csrf=True)
    def web_auth_signup(self, *args, **kw):
        print("comingg here with validation")
        qcontext = self.get_auth_signup_qcontext()
        otp_obj = request.env['otp.otp']
        if 'user_type' not in qcontext:
            qcontext['user_type'] = 'creator'
        if not qcontext.get('token') and not qcontext.get('signup_enabled'):
            raise werkzeug.exceptions.NotFound()
        redirect_url = request.session.get('redirect_after_signup')

        if 'error' not in qcontext and request.httprequest.method == 'POST':
            try:
                otp_code = ''
                if kw.get('otp_1'):
                    otp_code += kw.get('otp_1')
                if kw.get('otp_2'):
                    otp_code += kw.get('otp_2')
                if kw.get('otp_3'):
                    otp_code += kw.get('otp_3')
                if kw.get('otp_4'):
                    otp_code += kw.get('otp_4')
                if kw.get('otp_5'):
                    otp_code += kw.get('otp_5')
                if kw.get('otp_6'):
                    otp_code += kw.get('otp_6')

                if kw.get('phone'):
                # if len(otp_code) == 6 and kw.get('phone'): 
                    # Check if the OTP exists for the mobile number
                    otp_record = otp_obj.sudo().search([], order='create_date desc', limit=1)
                    # otp_record = otp_obj.sudo().search([
                    #     ("mobile", "=", kw.get('phone')), 
                    #     ('otp','=',otp_code), 
                    #     ('is_verify', '=', True)], order='create_date desc', limit=1)
                    if otp_record: 
                        self.do_signup(qcontext)
                        # Set user to public if they were not signed in by do_signup
                        # (mfa enabled)
                        if request.session.uid is None:
                            public_user = request.env.ref('base.public_user')
                            request.update_env(user=public_user)

                        # Send an account creation confirmation email
                        User = request.env['res.users']
                        user_sudo = User.sudo().search(
                            User._get_login_domain(qcontext.get('login')), order=User._get_login_order(), limit=1
                        )
                        template = request.env.ref('auth_signup.mail_template_user_signup_account_created', raise_if_not_found=False)
                        if user_sudo and template:
                            template.sudo().send_mail(user_sudo.id, force_send=True)
                        otp_record.write({'partner_id':user_sudo.partner_id.id})
                        if user_sudo.partner_id.user_type == 'creator':
                            return request.redirect("sign-up/about?partner=%d" % user_sudo.partner_id)
                        elif user_sudo.partner_id.user_type == 'partner':
                            print("cominggg111111111")
                            return request.redirect("sign-up/about?partner=%d" % user_sudo.partner_id)
                        elif user_sudo.partner_id.user_type == 'customer':
                            if redirect_url:
                                del request.session['redirect_after_signup']  # Clear session value after use
                                return request.redirect(redirect_url)
                            else:
                                return request.redirect('/customer')
                        else:
                            return self.web_login(*args, **kw)
                    else:
                        qcontext["error"] = _("Mobile number not verified.")
                else:
                    qcontext["error"] = _("Mobile number not verified.")
            except UserError as e:
                qcontext['error'] = e.args[0]
            except (SignupError, AssertionError) as e:
                if request.env["res.users"].sudo().search_count([("login", "=", qcontext.get("login"))], limit=1):
                    qcontext["error"] = _("Another user is already registered using this email address.")
                else:
                    _logger.warning("%s", e)
                    qcontext['error'] = _("Could not create a new account.") + Markup('<br/>') + str(e)

        elif 'signup_email' in qcontext:
            user = request.env['res.users'].sudo().search([('email', '=', qcontext.get('signup_email')), ('state', '!=', 'new')], limit=1)
            if user:
                if user.partner_id.user_type == 'creator':
                    return request.redirect("sign-up/about?partner=%d" % user.partner_id)
                elif user.partner_id.user_type == 'partner':
                    print("comingggg2222222")
                    return request.redirect("sign-up/about?partner=%d" % user.partner_id)
                elif partner_id.user_type == 'customer':
                    return request.redirect('/customer')
                else:
                    return request.redirect('/web/login?%s' % url_encode({'login': user.login, 'redirect': '/web'}))
        response = request.render('apg_signup.custom_signup', qcontext)
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['Content-Security-Policy'] = "frame-ancestors 'self'"
        return response


    # Generate OTP
    @http.route(['/generate/otp'], type='json', auth="public", website=True)
    def generate_otp(self, mobile=False, **post):
        values = {}
        language = request.context.get('lang')
        # base_url = "https://mobicomm.dove-sms.com//generateOtp.jsp?userid=SACHIN&key=6e637e20bfXX&mobileno=+918354887130&timetoalive=200&message=Dear%20Customer%20Do%20Not%20Share%20OTP%20%7Botp%7D%20OMKARENT&senderid=OMENTO&accusage=1&entityid=1401487200000053882&tempid=1407167569369094246"
        if mobile:
            if request.env["res.partner"].sudo().search([("mobile", "=", mobile)]):
                values['error'] = 'Another user is already registered using this mobile No'
                return values
            values['true'] = True
            return values
            # base_url = "https://mobicomm.dove-sms.com//generateOtp.jsp?userid=SACHIN&key=6e637e20bfXX&mobileno=+918354887130&timetoalive=200&message=Dear%20Customer%20Do%20Not%20Share%20OTP%20%7Botp%7D%20OMKARENT&senderid=OMENTO&accusage=1&entityid=1401487200000053882&tempid=1407167569369094246"
            # # Construct the URL with parameters
            
            # try:
            #     response = requests.get(base_url)
            #     print("Response",response)
            #     data = response.json()
            #     print("Response",data['result'])
            #     if data['result'] == 'success':
            #         values['true'] = True
            #     else:
            #         return f"Failed to send OTP: {data['reason']}"
            # except Exception as e:
            #     return f"An error occurred: {str(e)}"
            # return values
        else:
            values['error'] = 'Please enter valid Mobile Number'
            return values

    # OTP Verification 
    @http.route(['/otp/verification'], type='json', auth="public", website=True)
    def otp_verification(self, mobile=False, otp=False, **post):
        values = {}
        otp_obj = request.env['otp.otp']
        if mobile and otp:
            # Check if the OTP exists for the mobile number
            otp_id = otp_obj.sudo().create({'otp':otp,'mobile':mobile,'is_verify':True})
            values['true'] = True
            return values
            # base_url = "https://mobicomm.dove-sms.com//validateOtpApi.jsp?otp="+otp+"&mobileno=+918354887130"
            # response = requests.get(base_url)
            # data = response.json()
            # print("Response",data)
            # if data['result'] == 'success':
            #     otp_id = otp_obj.sudo().create({'otp':otp,'mobile':mobile,'is_verify':True})
            #     values['true'] = True
            #     return values
            # else:
            #     # return f"Failed to send OTP: {data['reason']}"
            #     values['error'] = f"Failed to send OTP: {data['result']}"
            #     return values
        else:
            values['error'] = 'Missing mobile number or OTP. Please try again.'
            return values

    @http.route(['/sign-up/about'], type="http", auth="public", website=True)
    def signup_details(self, **post):
        partner_id = post.get('partner')
        niche_type_obj = request.env['niche.type'].search([])
        partner_obj = request.env['res.partner'].search([])
        countries = request.env['res.country'].search([])  # Fetch all countries
        # Get India (Default Country)
        # Fetch India country ID
        india = request.env['res.country'].search([('code', '=', 'IN')], limit=1)
        states = request.env['res.country.state'].search([('country_id', '=', india.id)])
        default_country_id = india.id if india else False

        # Get the currently logged-in user
        user = request.env.user
        logged_in_partner = user.partner_id  # Fetch associated partner record
        # If user has no country, set India as default
        user_country_id = logged_in_partner.country_id.id if logged_in_partner.country_id else default_country_id
        if partner_id:
            partner = request.env['res.partner'].search([('id','=',partner_id)])
            if partner.user_type == 'creator':
                values={
                    'partner_id':partner.id,
                    'niche_type':niche_type_obj,
                    'partner':partner_obj,
                }
                return request.render('apg_signup.partner_details_template',values)
            elif partner.user_type == 'partner':
                values = {
                    'partner_id': partner.id,
                    'partner': partner_obj,
                    'full_name': logged_in_partner.name if logged_in_partner else '',
                    'countries': countries,  # Pass all countries to the template
                    'states': states,  # Pass states to template
                    'default_country_id': user_country_id,  # Use user's country or India
                }
                return request.render('apg_signup.partner_signup_second_page', values)

    
    @http.route(['/sign-up/about/update'], type="http", auth="public", website=True)
    def signup_details_update(self, **post):
        lines_ids = []
        partner = post.get('partner_id')
        media_obj = request.env['social.media']
        social_lines_ids = request.httprequest.form.getlist('social_section_line')
        if partner:
            partner_id = request.env['res.partner'].search([('id','=',partner)])
            i = 1

            for line in social_lines_ids:
                if 'facebook' == line:
                    vals = {
                        'partner_id': partner_id.id,
                        'social_media': 'facebook',
                        'social_media_link': social_lines_ids[i],
                    }
                    lines_ids.append((0, 0, vals))
                    i += 2
                elif 'twitter' == line:
                    vals = {
                        'partner_id': partner_id.id,
                        'social_media': 'twitter',
                        'social_media_link': social_lines_ids[i],
                    }
                    lines_ids.append((0, 0, vals))
                    i += 2
                elif 'instagram' == line:
                    vals = {
                        'partner_id': partner_id.id,
                        'social_media': 'instagram',
                        'social_media_link': social_lines_ids[i],
                    }
                    lines_ids.append((0, 0, vals))
                    i += 2
                elif 'linkedin' == line:
                    vals = {
                        'partner_id': partner_id.id,
                        'social_media': 'linkedin',
                        'social_media_link': social_lines_ids[i],
                    }
                    lines_ids.append((0, 0, vals))
                    i += 2
                elif 'youtube' == line:
                    vals = {
                        'partner_id': partner_id.id,
                        'social_media': 'youtube',
                        'social_media_link': social_lines_ids[i],
                    }
                    lines_ids.append((0, 0, vals))
                    i += 2
                elif 'x_portal' == line:
                    vals = {
                        'partner_id': partner_id.id,
                        'social_media': 'x_portal',
                        'social_media_link': social_lines_ids[i],
                    }
                    lines_ids.append((0, 0, vals))
                    i += 2
                
                # media_id = media_obj.sudo().create(vals)
            partner_vals = {
                'social_section_line':lines_ids,
                'product_type': 'pre_orded_course',
                'reference': post.get('reference'),
                'description': post.get('description'),
                }
            # Additional update if user type is 'partner'
            if partner_id.user_type == 'partner':
                state_id = request.env['res.country.state'].search([('id', '=', post.get('state'))], limit=1)
                country_id = request.env['res.country'].search([('id', '=', post.get('country'))], limit=1)
                partner_vals.update({
                    'reference' : post.get('reference'),
                    'city': post.get('city'),
                    'state_id': state_id.id if state_id else False,
                    'country_id': country_id.id if country_id else False,
                })
            
            partner_id.sudo().write(partner_vals)
            if partner_id.user_type == 'creator':
                return request.redirect('/master')
            elif partner_id.user_type == 'partner':
                return request.redirect('/master-partner')
            elif partner_id.user_type == 'customer':
                return request.redirect('/customer')
            else:
                return request.redirect('/')

    def do_signup(self, qcontext):
        """ Shared helper that creates a res.partner out of a token """
        values = {key: qcontext.get(key) for key in ('login', 'name', 'password', 'user_type', 'phone')}
        # if not values:
        #     raise UserError(_("The form was not properly filled in."))
        if values.get('password') != qcontext.get('confirm_password'):
            raise UserError(_("Passwords do not match; please retype them."))
        supported_lang_codes = [code for code, _ in request.env['res.lang'].get_installed()]
        lang = request.context.get('lang', '').split('_')[0]
        if lang in supported_lang_codes:
            values['lang'] = lang
        values['password'] = values['phone']
        self._signup_with_values(qcontext.get('token'), values)
        request.env.cr.commit()

    def _render_signup_page(self, user_type, phone):
        qcontext = self.get_auth_signup_qcontext()
        qcontext['user_type'] = user_type
        qcontext['phone'] = user_type

        # Render the signup page with updated context
        return request.render('auth_signup.signup', qcontext)

    def get_auth_signup_qcontext(self):
        SIGN_UP_REQUEST_PARAMS.update({'user_type'})
        SIGN_UP_REQUEST_PARAMS.update({'phone'})
        return super().get_auth_signup_qcontext()


class WebsiteSale(payment_portal.PaymentPortal):
    @route(['/shop/cart'], type='http', auth="public", website=True, sitemap=False)
    def cart(self, access_token=None, revive='', **post):
        """
        Main cart management + abandoned cart revival
        access_token: Abandoned cart SO access token
        revive: Revival method when abandoned cart. Can be 'merge' or 'squash'
        """
        if not request.website.has_ecommerce_access():
            return request.redirect('/web/login')

        order = request.website.sale_get_order()
        if order and order.state != 'draft':
            request.session['sale_order_id'] = None
            order = request.website.sale_get_order()

        request.session['website_sale_cart_quantity'] = order.cart_quantity

        values = {}
        if access_token:
            abandoned_order = request.env['sale.order'].sudo().search([('access_token', '=', access_token)], limit=1)
            if not abandoned_order:  # wrong token (or SO has been deleted)
                raise NotFound()
            if abandoned_order.state != 'draft':  # abandoned cart already finished
                values.update({'abandoned_proceed': True})
            elif revive == 'squash' or (revive == 'merge' and not request.session.get('sale_order_id')):  # restore old cart or merge with unexistant
                request.session['sale_order_id'] = abandoned_order.id
                return request.redirect('/shop/cart')
            elif revive == 'merge':
                abandoned_order.order_line.write({'order_id': request.session['sale_order_id']})
                abandoned_order.action_cancel()
            elif abandoned_order.id != request.session.get('sale_order_id'):  # abandoned cart found, user have to choose what to do
                values.update({'access_token': abandoned_order.access_token})

        values.update({
            'website_sale_order': order,
            'date': fields.Date.today(),
            'suggested_products': [],
        })
        if order:
            order.order_line.filtered(lambda sol: sol.product_id and not sol.product_id.active).unlink()
            values['suggested_products'] = order._cart_accessories()
            values.update(self._get_express_shop_payment_values(order))

        values.update(self._cart_values(**post))
        # Check if the user is logged in
        user = request.env.user
        if user and user.id != request.website.user_id.id:  # Check if the user is not the public user
            # Redirect registered users to the payment page
            return request.redirect('/shop/checkout?try_skip_step=true')
        else:
            # Store the current product URL to return after signup
            current_url = request.httprequest.referrer
            request.session['redirect_after_signup'] = current_url
            return request.redirect('/web/signup?user_type=customer')

    @route('/shop/payment', type='http', auth='public', website=True, sitemap=False)
    def shop_payment(self, **post):
        """ Payment step. This page proposes several payment means based on available
        payment.provider. State at this point :

         - a draft sales order with lines; otherwise, clean context / session and
           back to the shop
         - no transaction in context / session, or only a draft one, if the customer
           did go to a payment.provider website but closed the tab without
           paying / canceling
        """
        order_sudo = request.website.sale_get_order()

        if redirection := self._check_cart_and_addresses(order_sudo):
            return redirection

        if redirection := self._check_shipping_method(order_sudo):
            return redirection

        render_values = self._get_shop_payment_values(order_sudo, **post)
        render_values['only_services'] = order_sudo and order_sudo.only_services
        
        if render_values['errors']:
            render_values.pop('payment_methods_sudo', '')
            render_values.pop('tokens_sudo', '')
        country_id = request.env['res.country'].sudo().search([])
        state_id = request.env['res.country.state'].sudo().search([])
        if order_sudo.partner_id:
            if order_sudo.partner_id.country_id:
                state_id = request.env['res.country.state'].sudo().search([
                    ('country_id', '=', order_sudo.partner_id.country_id.id)])
        render_values['country_id'] = country_id
        render_values['state_id'] = state_id
        return request.render("website_sale.payment", render_values)

    # === CHECK METHODS === #

    def _check_cart_and_addresses(self, order_sudo):
        """ Check whether the cart and its addresses are valid, and redirect to the appropriate page
        if not.

        :param sale.order order_sudo: The cart to check.
        :return: None if both the cart and its addresses are valid; otherwise, a redirection to the
                 appropriate page.
        """

        if redirection := self._check_cart(order_sudo):
            return redirection

        # if redirection := self._check_addresses(order_sudo):
        #     return redirection

    @http.route('/get_states_by_country', type='json', auth='public', website=True)
    def get_states_by_country(self, country_id):
        current_user = request.env.user
        partner = current_user.partner_id
        if not country_id:
            return []
        states = request.env['res.country.state'].search([('country_id', '=', int(country_id))])
        if partner:
            partner.sudo().write({'country_id':int(country_id)})
        return [{'id': state.id, 'name': state.name} for state in states]

    @http.route('/update_location', type='json', auth='public', website=True)
    def update_partner_location(self, state_id=False):
        current_user = request.env.user
        partner = current_user.partner_id
        values = {}
        if not state_id:
            return []
        state_id = request.env['res.country.state'].search([('id', '=', int(state_id))],limit=1)
        if partner and state_id:
            partner.sudo().write({'state_id':state_id.id})
            values['success'] = True
            return values
        else:
            values['success'] = False
            return values


    @http.route('/partner-secondpage', type='http', auth='public', website=True)
    def partner_second_page(self, **kwargs):
        # Render the data page template
        return http.request.render('apg_signup.partner_signup_second_page')


    # @route('/signIn', type='http', auth='public', website=True, sitemap=False)
    # def custom_signin(self, **post):
    #     return request.render('apg_signup.custom_signin')

    # @route('/landing_page', type='http', auth='public', website=True, sitemap=False)
    # def landing_page(self, **post):
    #     landing_id = request.env['slide.channel'].sudo().search([('id', '=', 1)],limit=1)
    #     student = []  # List to hold the pairs
    #     first_record = None  # Store the first record for reuse
    #     data = {}     # Temporary dictionary for a single pair
    #     i = 1         # Counter to alternate between 'a' and 'b'

    #     if landing_id.student_line_ids:
    #         for rec in landing_id.student_line_ids:
    #             if first_record is None:  # Capture the first record
    #                 first_record = {
    #                     'name': rec.name,
    #                     'type': rec.content_type,
    #                     'content': rec.p1,
    #                     'rating': int(rec.rating),
    #                     'image': rec.image
    #                 }
    #             if i == 1:  # Populate 'a' part of the pair
    #                 data = {'a': {
    #                     'name': rec.name,
    #                     'type': rec.content_type,
    #                     'content': rec.p1,
    #                     'rating': int(rec.rating),
    #                     'image': rec.image
    #                 }}
    #                 i += 1
    #             else:  # Populate 'b' part of the pair
    #                 data['b'] = {
    #                     'name': rec.name,
    #                     'type': rec.content_type,
    #                     'content': rec.p1,
    #                     'rating': int(rec.rating),
    #                     'image': rec.image
    #                 }
    #                 student.append(data)  # Add the completed pair to the list
    #                 data = {}  # Reset for the next pair
    #                 i = 1

    #     # Handle the case of an unpaired last 'a' by repeating the first record in 'b'
    #     if data and 'a' in data:
    #         data['b'] = first_record  # Use the first record to fill the missing 'b'
    #         student.append(data)

    #     values = {
    #         'landing_id': landing_id,
    #         'students': student
    #     }
    #     return request.render('apg_signup.landing_page',values)
