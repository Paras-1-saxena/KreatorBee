from odoo import http
from odoo.http import request

class RestrictMobileController(http.Controller):
    @http.route('/mobile-restricted', type='http', auth='public', website=True)
    def mobile_restricted(self, **kwargs):
        return request.render("apg_js.mobile_restricted_page")