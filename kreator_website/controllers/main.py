# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request


class KreatorWebsite(http.Controller):

    @http.route('/landing/page/1', auth='public', website=True)
    def landing_page_1(self, **kw):
        return request.render("kreator_website.landing_page_1", {})
