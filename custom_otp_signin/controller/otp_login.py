from random import choice
import string

from odoo.addons.web.controllers.home import Home, ensure_db
from odoo import http, _
from odoo.exceptions import AccessDenied, AccessError, UserError, ValidationError
from odoo.http import request


class OtpLoginHome(Home):
    
    @http.route(website=True)
    def web_login(self, redirect=None, **kw):
        ensure_db()
        qcontext = request.params.copy()

        if request.httprequest.method == 'GET':

            if "otp_login" and "otp" in kw:
                if kw["otp_login"] and kw["otp"]:
                    return request.render("custom_otp_signin.custom_otp_signin", {'otp': True, 'otp_login': True})
            if "otp_login" in kw: #checks if the keyword "otp_login" exists in the dict "kw".
                if kw["otp_login"]: #checks if the value of "otp_login" is true.
                    return request.render("custom_otp_signin.custom_otp_signin", {'otp_login': True})
            else:
                return super(OtpLoginHome, self).web_login(redirect, **kw)
        else:
            if kw.get('login'):
                partner = request.env['res.partner'].sudo().search([('mobile', '=', kw.get('login'))], limit=1)
                if partner:
                    user_id = request.env['res.users'].sudo().search([('partner_id', '=', partner.id)], limit=1)
                    request.params['login'] = user_id.login
                    if user_id.partner_id.user_type == 'creator':
                        redirect = '/master'
                    elif user_id.partner_id.user_type == 'partner':
                        redirect = '/partner'
                    elif user_id.partner_id.user_type == 'customer':
                        redirect = '/customer'
                    else:
                        redirect=None
                else:
                    request.params['login'] = kw.get('login').strip()
                
            if kw.get('password'):
                request.params['password'] = kw.get('password')
            return super(OtpLoginHome, self).web_login(redirect, **kw)

        return request.render("custom_otp_signin.custom_otp_signin", {})

    @http.route('/web/otp/login', type='http', auth='public', website=True, csrf=False)
    def web_otp_login(self, **kw):
        qcontext = request.params.copy()
        mobile = str(qcontext.get('login'))
        partner = request.env['res.partner'].sudo().search([('mobile', '=', mobile)], limit=1)
        if partner:

            user_id = request.env['res.users'].sudo().search([('partner_id', '=', partner.id)], limit=1)

            if user_id:
                OTP = self.generate_otp_login(6)
                vals = {
                    'otp': OTP,
                    'mobile': mobile
                }
                
                response = request.render("custom_otp_signin.custom_otp_signin", {'otp': True, 'otp_login': True,
                                                                                   'login': qcontext["login"],
                                                                                   'otp_no': OTP})
                request.env['otp.verification'].sudo().create(vals)
                return response

        else:
            response = request.render("custom_otp_signin.custom_otp_signin", {'otp': False, 'otp_login': True,
                                                                               })
            return response

    @http.route('/web/otp/verify', type='http', auth='public', website=True, csrf=False)
    def web_otp_verify(self, *args, **kw):
        qcontext = request.params.copy()
        mobile = str(kw.get('login'))
        res_id = request.env['otp.verification'].search([('mobile', '=', mobile)], order="create_date desc", limit=1)

        try:
            otp = str(kw.get('otp'))
            otp_no = res_id.otp
            if otp_no == otp:
                res_id.state = 'verified'
                partner = request.env['res.partner'].sudo().search([('mobile', '=', mobile)], limit=1)
                user_id = request.env['res.users'].sudo().search([('partner_id', '=', partner.id)], limit=1)
                request.env.cr.execute(
                    "SELECT COALESCE(password, '') FROM res_users WHERE id=%s",
                    [user_id.id]
                )
                hashed = request.env.cr.fetchone()[0]
                qcontext.update({'login': user_id.sudo().login,
                                 'name': user_id.sudo().partner_id.name,
                                 'password': hashed + 'mobile_otp_login'})
                request.params.update(qcontext)
                return self.web_login(*args, **kw)
            else:
                res_id.state = 'rejected'
                response = request.render('custom_otp_signin.custom_otp_signin', {'otp': True, 'otp_login': True,
                                                                                   'login': mobile})
                return response
        except UserError as e:
            qcontext['error'] = e.name or e.value

        response = request.render('custom_otp_signin.custom_otp_signin', {'otp': True, 'otp_login': True,
                                                                           'login': mobile})
        return response

    def generate_otp_login(self, number_of_digits):
        otp = ''.join(choice(string.digits) for _ in range(number_of_digits))
        return otp
