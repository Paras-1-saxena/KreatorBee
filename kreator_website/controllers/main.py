# -*- coding: utf-8 -*-
from markupsafe import Markup

from odoo import http
from odoo.http import request
import datetime as datetime
import pytz

class KreatorWebsite(http.Controller):

    @http.route('/gquh2blrsego3n2x0f629e1ks3uc5x.html', auth='public', website=True)
    def main_test(self, **kwargs):
        test='a'
        return request.redirect('/kreator_website/static/src/html/gquh2blrsego3n2x0f629e1ks3uc5x.html')

    @http.route('/landing/page/1', auth='public', website=True)
    def landing_page_1(self, **kwargs):
        course = request.env['slide.channel'].sudo().search([('id', '=', kwargs.get('course_id'))])
        values = self.fetch_values(**kwargs)
        return request.render("kreator_website.landing_page_1", values)

    @http.route('/landing/page/2', auth='public', website=True)
    def landing_page_2(self, **kwargs):
        course = request.env['slide.channel'].sudo().search([('id', '=', kwargs.get('course_id'))])
        values = self.fetch_values(**kwargs)
        return request.render("kreator_website.landing_page_2", values)

    @http.route('/landing/page/3', auth='public', website=True)
    def landing_page_3(self, **kwargs):
        course = request.env['slide.channel'].sudo().search([('id', '=', kwargs.get('course_id'))])
        values = self.fetch_values(**kwargs)
        return request.render("kreator_website.landing_page_3", values)

    @http.route('/landing/page/4', auth='public', website=True)
    def landing_page_4(self, **kwargs):
        course = request.env['slide.channel'].sudo().search([('id', '=', kwargs.get('course_id'))])
        values = self.fetch_values(**kwargs)
        return request.render("kreator_website.landing_page_4", values)

    @http.route('/landing/page/5', auth='public', website=True)
    def landing_page_5(self, **kwargs):
        course = request.env['slide.channel'].sudo().search([('id', '=', kwargs.get('course_id'))])
        values = self.fetch_values(**kwargs)
        return request.render("kreator_website.landing_page_5", values)

    @http.route('/landing/page/6', auth='public', website=True)
    def video_editing_ayushman(self, **kwargs):
        course = request.env['slide.channel'].sudo().search([('id', '=', kwargs.get('course_id'))])
        values = self.fetch_values(**kwargs)
        intro_video = Markup('''<iframe src="https://player.vimeo.com/video/1067332531?badge=0&amp;autopause=0&amp;player_id=0&amp;app_id=58479"
                                    frameborder="0"
                                    allow="autoplay; fullscreen; picture-in-picture; clipboard-write; encrypted-media"
                                    style="width:100%;height:40vh; border-radius: 25px;"
                                    title="problem"></iframe>''')
        values.update({'intro_video': intro_video})
        return request.render("kreator_website.video_editing_ayushman", values)

    @http.route('/landing/page/7', auth='public', website=True)
    def freelancing_employees_ayushman(self, **kwargs):
        course = request.env['slide.channel'].sudo().search([('id', '=', kwargs.get('course_id'))])
        values = self.fetch_values(**kwargs)
        intro_video = Markup('''<iframe src="https://player.vimeo.com/video/1068749072?badge=0&amp;autopause=0&amp;player_id=0&amp;app_id=58479"
         frameborder="0" allow="autoplay; fullscreen; picture-in-picture; clipboard-write; encrypted-media"
          style="width:100%;height:40vh; border-radius: 25px;" title="Long Promo_1"></iframe>''')
        values.update({'intro_video': intro_video})
        return request.render("kreator_website.freelancing_employees_ayushman", values)

    @http.route('/landing/page/8', auth='public', website=True)
    def freelancing_genz_ayushman(self, **kwargs):
        course = request.env['slide.channel'].sudo().search([('id', '=', kwargs.get('course_id'))])
        values = self.fetch_values(**kwargs)
        intro_video = Markup('''<iframe src="https://player.vimeo.com/video/1068746592?badge=0&amp;autopause=0&amp;player_id=0&amp;app_id=58479"
         frameborder="0" allow="autoplay; fullscreen; picture-in-picture; clipboard-write; encrypted-media"
          style="width:100%;height:40vh; border-radius: 25px; title="Promotional  gen-z-"></iframe>''')
        values.update({'intro_video': intro_video})
        return request.render("kreator_website.freelancing_genz_ayushman", values)

    @http.route('/landing/page/9', auth='public', website=True)
    def lead_generation_lakshit(self, **kwargs):
        course = request.env['slide.channel'].sudo().search([('id', '=', kwargs.get('course_id'))])
        values = self.fetch_values(**kwargs)
        intro_video = Markup('''<iframe src="https://player.vimeo.com/video/1068746592?badge=0&amp;autopause=0&amp;player_id=0&amp;app_id=58479"
             frameborder="0" allow="autoplay; fullscreen; picture-in-picture; clipboard-write; encrypted-media"
              style="width:100%;height:40vh; border-radius: 25px; title="Promotional  gen-z-"></iframe>''')
        values.update({'intro_video': intro_video})
        return request.render("kreator_website.lead_generation_lakshit", values)

    def fetch_values(self, **kwargs):
        course = request.env['slide.channel'].sudo().search([('id', '=', kwargs.get('course_id'))])
        value = {
            'main_heading': course.name, 'p2': course.p2, 'creator_name': course.creator_name,
            'image_icon': course.image_icon, 'c1': course.c1, 'c2': course.c2, 'c3': course.c3, 'c4': course.c4,
            'course_line_ids': course.course_line_ids, 'individual_line_ids': course.individual_line_ids,
            'cc': course.line_ids, 'm1': course.m1, 'm2': course.m2, 'm3': course.m3, 'm4': course.m4, 'm5': course.m5,
            'm6': course.m6, 'my_image_icon': course.my_image_icon, 'about_me_line_ids': course.about_me_line_ids,
            'course_ids': course.course_ids, 'student_line_ids': course.student_line_ids, 'faq_ids': course.faq_ids,
            'h4': course.h4, 'c11': course.c11, 'image1': course.image1, 'course_id': course.id, 'course': course,
            'product_template_id': course.product_id.product_tmpl_id.id, 'product_id': course.product_id.id,
            'price1': course.price1, 'price2': course.price2, 'num_to_word': {1: 'One', 2: 'Two', 3: 'Three',
                                                                              4: 'Four', 5: 'Five', 6: 'Six',
                                                                              7: 'Seven', 8: 'Eight', 9: 'Nine'}
        }
        expiry_time = kwargs.get('exp')
        if expiry_time:
            expiry_date = datetime.datetime.fromtimestamp(int(expiry_time), pytz.timezone("Asia/Calcutta")).strftime(
                "%b %d, %Y %H:%M:%S")
            value.update({'expired': expiry_date})
        return value
