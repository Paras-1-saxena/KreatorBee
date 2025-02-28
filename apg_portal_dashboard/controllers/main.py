# Part of Odoo. See LICENSE file for full copyright and licensing details.

import math
import re

from werkzeug import urls

from odoo import http, tools, _, SUPERUSER_ID
from odoo.exceptions import AccessDenied, AccessError, MissingError, UserError, ValidationError
from odoo.http import content_disposition, Controller, request, route
from odoo.tools import consteq


class PortalDashboard(Controller):

    def _prepare_portal_layout_values(self):
        """Values for /my/* templates rendering.

        Does not include the record counts.
        """
        # get customer sales rep
        sales_user_sudo = request.env['res.users']
        partner_sudo = request.env.user.partner_id
        if partner_sudo.user_id and not partner_sudo.user_id._is_public():
            sales_user_sudo = partner_sudo.user_id
        else:
            fallback_sales_user = partner_sudo.commercial_partner_id.user_id
            if fallback_sales_user and not fallback_sales_user._is_public():
                sales_user_sudo = fallback_sales_user

        return {
            'sales_user': sales_user_sudo,
            'page_name': 'home',
        }

    def _prepare_home_portal_values(self, counters):
        """Values for /my & /my/home routes template rendering.

        Includes the record count for the displayed badges.
        where 'counters' is the list of the displayed badges
        and so the list to compute.
        """
        return {}


    @route(['/dashboard'], type='http', auth="user", website=True)
    def portal_dashboard(self, **kw):
        values = self._prepare_portal_layout_values()
        values.update(self._prepare_home_portal_values([]))
        return request.render("apg_portal_dashboard.portal_my_dashboard", values)

class CustomMenuController(http.Controller):

    @http.route('/my/<string:page>', type='http', auth='public', website=True)
    def get_content(self, page):
        # Example of content loading logic
        if page == 'courses':
            return request.render('apg_portal_dashboard.custom_page_template')
        elif page == 'analytics':
            # content = '<h2>Page Not Found</h2>'
            return request.render('apg_portal_dashboard.analytics_page_template')
        elif page == 'products':
            # content = '<h2>Page Not Found</h2>'
            return request.render('apg_portal_dashboard.product_page_template')
        elif page == 'certificates':
            # content = '<h2>Page Not Found</h2>'
            return request.render('apg_portal_dashboard.certificates_page_template')
        elif page == 'workshops':
            # content = '<h2>Page Not Found</h2>'
            return request.render('apg_portal_dashboard.workshop_page_template')
        elif page == 'consultation':
            # content = '<h2>Page Not Found</h2>'
            return request.render('apg_portal_dashboard.consultation_page_template')
        else:
            content = '<h2>Page Not Found</h2>'
            return content
            # return request.render('apg_portal_dashboard.custom_page_template', {
            #     'page_title': 'Not Found',
            #     'page_content': '<h2>Page Not Found</h2>',
            # })