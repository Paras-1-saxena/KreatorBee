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
 
class CourseTraining(payment_portal.PaymentPortal):
    @http.route('/partner/training', type='http', auth='public', website=True)
    def partner_training(self, **kwargs):
        user = request.env.user
        partner = user.partner_id  # Get related partner

        training_courses = request.env['apg.course.training'].sudo().search([])
        print("training_courses", training_courses)
        return request.render('apg_training.partner_course_training', {
            'training_courses': training_courses,
        })

    # @http.route('/partner/training', type='http', auth='public', website=True)
    # def partner_training(self, **kwargs):
    #     user = request.env.user
    #     partner = user.partner_id  # Get related partner

    #     training_courses = request.env['apg.course.training'].sudo().search([])
    #     print("training_courses", training_courses)
    #     return request.render('custom_web_kreator.partner_training', {
    #         'training_courses': training_courses,
    #     })
