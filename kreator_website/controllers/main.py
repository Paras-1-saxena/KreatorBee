# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request


class KreatorWebsite(http.Controller):

    @http.route('/landing/page/1', auth='public', website=True)
    def landing_page_1(self, **kw):
        return request.render("kreator_website.landing_page_1", {})

    @http.route('/landing/page/2', auth='public', website=True)
    def landing_page_2(self, **kw):
        return request.render("kreator_website.landing_page_2", {})

    @http.route('/landing/page/3', auth='public', website=True)
    def landing_page_3(self, **kw):
        return request.render("kreator_website.landing_page_3", {})
