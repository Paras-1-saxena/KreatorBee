# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request


class KreatorWebsite(http.Controller):

    @http.route('/landing/page/1', auth='public', website=True)
    def landing_page_1(self):
        return request.render("kreator_website.landing_page_1", {})

    @http.route('/landing/page/2', auth='public', website=True)
    def landing_page_2(self):
        return request.render("kreator_website.landing_page_2", {})

    @http.route('/landing/page/3', auth='public', website=True)
    def landing_page_3(self):
        return request.render("kreator_website.landing_page_3", {})

    @http.route('/landing/page/4', auth='public', website=True)
    def landing_page_4(self):
        return request.render("kreator_website.landing_page_4", {})

    @http.route('/landing/page/5', auth='public', website=True)
    def landing_page_5(self):
        return request.render("kreator_website.landing_page_5", {})
