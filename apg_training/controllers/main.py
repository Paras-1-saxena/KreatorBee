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
import re
from urllib.parse import urlparse, parse_qs

_logger = logging.getLogger(__name__)
 
class PortalMyCourses(http.Controller):
    @http.route('/partner/training', type='http', auth='public', website=True)
    def partner_training(self, **kwargs):
        user = request.env.user
        partner = user.partner_id  # Get related partner

        training_courses = request.env['apg.course.training'].sudo().search([])
        print("training_courses", training_courses)
        return request.render('custom_web_kreator.partner_training', {
            'training_courses': training_courses,
        })
    
    @http.route('/partner/training/video', type='http', auth='user', website=True, methods=['GET', 'POST'], csrf=False)
    def partner_training_video(self, **kwargs):
        user = request.env.user
        partner = user.partner_id  # Get related partner

        video_data = ""
        if partner.user_type in ['internal_user', 'partner'] and kwargs.get('video_id'):
            # Get YouTube URL from training line
            training_video_link = request.env['apg.course.training.lines'].sudo().browse(int(kwargs.get('video_id'))).youtube_url

            convert_link = training_video_link  # fallback
            parsed_url = urlparse(training_video_link)
            query = parse_qs(parsed_url.query)

            # Case 1: Normal YouTube watch link
            if "youtube.com" in parsed_url.netloc and "watch" in parsed_url.path and "v" in query:
                video_id = query.get("v", [""])[0]
                playlist_id = query.get("list", [""])[0] if "list" in query else ""
                convert_link = f"https://www.youtube.com/embed/{video_id}"
                if playlist_id:
                    convert_link += f"?list={playlist_id}"

            # Case 2: Playlist link
            elif "youtube.com" in parsed_url.netloc and "playlist" in parsed_url.path and "list" in query:
                playlist_id = query.get("list", [""])[0]
                convert_link = f"https://www.youtube.com/embed/videoseries?list={playlist_id}"

            # Case 3: Short youtu.be link
            elif "youtu.be" in parsed_url.netloc:
                video_id = parsed_url.path.lstrip("/")
                convert_link = f"https://www.youtube.com/embed/{video_id}"

            # --- Create iframe HTML ---
            video_data = Markup(f'''
                <div style="width: 80dvw; height: 100dvh;" class="d-none d-md-block">
                    <iframe width="100%" height="60%" 
                        src="{convert_link}" 
                        title="YouTube video player" frameborder="0" 
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
                        referrerpolicy="strict-origin-when-cross-origin" allowfullscreen>
                    </iframe>
                </div>
                <iframe width="100%" height="auto" class="d-block d-md-none" 
                    src="{convert_link}" 
                    title="YouTube video player" frameborder="0" 
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
                    referrerpolicy="strict-origin-when-cross-origin" allowfullscreen>
                </iframe>
            ''')

        return request.make_response(
            data=json.dumps({'response': "success", 'video_data': video_data}),
            headers=[('Content-Type', 'application/json')],
            status=200
        )