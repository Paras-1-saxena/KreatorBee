# -*- coding: utf-8 -*-
from markupsafe import Markup

from odoo import http
from odoo.http import request
import datetime as datetime
import pytz
import json


class KreatorWebsite(http.Controller):

    @http.route('/gquh2blrsego3n2x0f629e1ks3uc5x.html', auth='public', website=True)
    def main_test(self, **kwargs):
        test = 'a'
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
        return request.redirect('/')
        course = request.env['slide.channel'].sudo().search([('id', '=', kwargs.get('course_id'))])
        values = self.fetch_values(**kwargs)

        intro_video = Markup(
            '''<iframe src="https://player.vimeo.com/video/1072780225?badge=0&amp;autopause=0&amp;player_id=0&amp;app_id=58479" frameborder="0"
             allow="autoplay; fullscreen; picture-in-picture; clipboard-write; encrypted-media"
              style="width:100%;height:40vh; border-radius: 25px;" title="Course Info"></iframe>''')
        values.update({'intro_video': intro_video})
        return request.render("kreator_website.video_editing_ayushman", values)

    @http.route('/landing/page/7', auth='public', website=True)
    def freelancing_employees_ayushman(self, **kwargs):
        return request.redirect('/')
        course = request.env['slide.channel'].sudo().search([('id', '=', kwargs.get('course_id'))])
        values = self.fetch_values(**kwargs)
        intro_video = Markup('''<iframe src="https://player.vimeo.com/video/1068749072?badge=0&amp;autopause=0&amp;player_id=0&amp;app_id=58479"
         frameborder="0" allow="autoplay; fullscreen; picture-in-picture; clipboard-write; encrypted-media"
          style="width:100%;height:40vh; border-radius: 25px;" title="Long Promo_1"></iframe>''')
        values.update({'intro_video': intro_video})
        return request.render("kreator_website.freelancing_employees_ayushman", values)

    @http.route('/landing/page/8', auth='public', website=True)
    def freelancing_genz_ayushman(self, **kwargs):
        return request.redirect('/')
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

    @http.route('/landing/page/10', auth='public', website=True)
    def affiliate_marketing_paras(self, **kwargs):
        course = request.env['slide.channel'].sudo().search([('id', '=', kwargs.get('course_id'))])
        values = self.fetch_values(**kwargs)
        intro_video = Markup("""
        <iframe src="https://player.vimeo.com/video/1076278508?badge=0&amp;autopause=0&amp;player_id=0&amp;app_id=58479"
         frameborder="0" allow="autoplay; fullscreen; picture-in-picture; clipboard-write; encrypted-media"
          style="width:100%; height:68vh;" title="Affiliate Marketing Millionaire Program Basic"></iframe>
        """)
        intro_video_mobile = Markup("""
        <iframe src="https://player.vimeo.com/video/1076278508?badge=0&amp;autopause=0&amp;player_id=0&amp;app_id=58479"
         frameborder="0" allow="autoplay; fullscreen; picture-in-picture; clipboard-write; encrypted-media"
          style="width:100%; height:30vh;" title="Affiliate Marketing Millionaire Program Basic"></iframe>
        """)
        values.update({'intro_video': intro_video, 'intro_video_mobile': intro_video_mobile, 'course_type': 'basic'})
        if request.session.get('referral_partner'):
            values.update({'price2': values.get('price2')-1000})
        return request.render("kreator_website.affiliate_marketing_basic_paras", values)

    @http.route('/landing/page/11', auth='public', website=True)
    def affiliate_marketing_paras_intermediate(self, **kwargs):
        course = request.env['slide.channel'].sudo().search([('id', '=', kwargs.get('course_id'))])
        values = self.fetch_values(**kwargs)
        intro_video = Markup('''<iframe src="https://player.vimeo.com/video/1076279089?badge=0&amp;autopause=0&amp;player_id=0&amp;app_id=58479"
         frameborder="0" allow="autoplay; fullscreen; picture-in-picture; clipboard-write; encrypted-media" 
         style="width:100%; height:68vh;" title="Affiliate Marketing Millionaire Program Intermidiate"></iframe>''')
        intro_video_mobile = Markup('''<iframe src="https://player.vimeo.com/video/1076279089?badge=0&amp;autopause=0&amp;player_id=0&amp;app_id=58479"
         frameborder="0" allow="autoplay; fullscreen; picture-in-picture; clipboard-write; encrypted-media" 
         style="width:100%; height:30vh;" title="Affiliate Marketing Millionaire Program Intermidiate"></iframe>''')
        stage_id = course.upgrade_stage_ids.filtered(lambda us: us.name == 'intermediate')
        partner_course_ids = request.env.user.partner_id.slide_channel_ids.product_id.ids
        price2 = sum([sc.list_price for sc in stage_id.product_ids if sc.id not in partner_course_ids])
        if request.session.get('referral_partner'):
            price2 = price2 - 1000 if price2 > 1000 else price2
        values.update(
            {'intro_video': intro_video, 'intro_video_mobile': intro_video_mobile, 'course_type': 'intermediate',
             'price1': 20000, 'price2': price2})
        return request.render("kreator_website.affiliate_marketing_basic_paras", values)

    @http.route('/landing/page/12', auth='public', website=True)
    def affiliate_marketing_paras_advance(self, **kwargs):
        course = request.env['slide.channel'].sudo().search([('id', '=', kwargs.get('course_id'))])
        values = self.fetch_values(**kwargs)
        intro_video = Markup('''<iframe src="https://player.vimeo.com/video/1076278055?badge=0&amp;autopause=0&amp;player_id=0&amp;app_id=58479"
         frameborder="0" allow="autoplay; fullscreen; picture-in-picture; clipboard-write; encrypted-media" 
         style="width:100%; height:68vh; " title="Affiliate Marketing Millionaire Program Advanced"></iframe>''')
        intro_video_mobile = Markup('''<iframe src="https://player.vimeo.com/video/1076278055?badge=0&amp;autopause=0&amp;player_id=0&amp;app_id=58479"
         frameborder="0" allow="autoplay; fullscreen; picture-in-picture; clipboard-write; encrypted-media" 
         style="width:100%; height:30vh; " title="Affiliate Marketing Millionaire Program Advanced"></iframe>''')
        stage_id = course.upgrade_stage_ids.filtered(lambda us: us.name == 'Advanced')
        partner_course_ids = request.env.user.partner_id.slide_channel_ids.product_id.ids
        price2 = sum([sc.list_price for sc in stage_id.product_ids if sc.id not in partner_course_ids])
        if request.session.get('referral_partner'):
            price2 = price2 - 1000 if price2 > 1000 else price2
        values.update(
            {'intro_video': intro_video, 'intro_video_mobile': intro_video_mobile, 'course_type': 'intermediate',
             'price1': 20000, 'price2': price2})
        values.update({'intro_video': intro_video, 'intro_video_mobile': intro_video_mobile, 'course_type': 'Advanced',
                       'price1': 20000, 'price2': price2})
        return request.render("kreator_website.affiliate_marketing_basic_paras", values)

    def fetch_values(self, **kwargs):
        request.session['data_submitted'] = 'No'
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
            'price1': course.regular_price, 'price2': course.sales_price,
            'num_to_word': {1: 'One', 2: 'Two', 3: 'Three',
                            4: 'Four', 5: 'Five', 6: 'Six',
                            7: 'Seven', 8: 'Eight', 9: 'Nine'}
        }
        expiry_time = kwargs.get('course_name')
        if expiry_time:
            expiry_time = int(''.join([x for x in expiry_time[::3]]))
            expiry_date = datetime.datetime.fromtimestamp(int(expiry_time), pytz.timezone("Asia/Calcutta")).strftime(
                "%b %d, %Y %H:%M:%S")
            value.update({'expired': expiry_date})
        return value

    @http.route('/lead/submission', auth='public', website=True, csrf=False)
    def captureLead(self, **kwargs):
        name, email, phno = kwargs.get('name', False), kwargs.get('email', False), int(kwargs.get('phno')) if kwargs.get('phno') else False
        if request.env['crm.lead'].sudo().search_count(['|', ('email_from', '=', email), ('phone', '=', phno)]):
            success_message = 'We’ve received your details successfully. We’ll get in touch with you soon.'
            request.session['data_submitted'] = 'yes'
        else:
            lead = request.env['crm.lead'].sudo().create({'name': name, 'email_from': email, 'phone': phno})
            lead.description = kwargs.get('course_name')
            success_message = 'We’ve received your details successfully. We’ll get in touch with you soon.'
            request.session['data_submitted'] = 'yes'
        return request.make_response(
            data=json.dumps({'response': "success", 'message': success_message}),
            headers=[('Content-Type', 'application/json')],
            status=200
        )

    @http.route('/preview/video', auth='public', website=True, csrf=False)
    def videoPreview(self, **kwargs):
        landing, video = int(kwargs.get('landing')), int(kwargs.get('video'))
        video = self.preview_vide_fetch(landing, video)
        if request.session.get('data_submitted') == 'yes':
            return request.make_response(
                data=json.dumps({'response': "success", 'video': video, 'submitted': 'yes'}),
                headers=[('Content-Type', 'application/json')],
                status=200
            )
        else:
            return request.make_response(
                data=json.dumps({'response': "success", 'submitted': 'no', 'video': video}),
                headers=[('Content-Type', 'application/json')],
                status=200
            )

    def preview_vide_fetch(self, landing, video):
        if landing == 10 and video == 1:
            return Markup('''<iframe src="https://player.vimeo.com/video/1073917141?badge=0&amp;autopause=0&amp;player_id=0&amp;app_id=58479"
             frameborder="0" allow="autoplay; fullscreen; picture-in-picture; clipboard-write; encrypted-media"
              style="width:80vw;height:60vh;" title="Lesson 01 Creator Bee.mp4"></iframe>
               <script src="https://player.vimeo.com/api/player.js"></script>''')
        if landing == 10 and video == 2:
            return Markup('''<iframe src="https://player.vimeo.com/video/1073917978?badge=0&amp;autopause=0&amp;player_id=0&amp;app_id=58479"
             frameborder="0" allow="autoplay; fullscreen; picture-in-picture; clipboard-write; encrypted-media"
              style="width:80vw;height:60vh;" title="Lesson 02 - Types of Lead Generation"></iframe>
                      <script src="https://player.vimeo.com/api/player.js"></script>''')
        if landing == 9 and video == 1:
            return Markup('''<iframe src="https://player.vimeo.com/video/1067319595?badge=0&amp;autopause=0&amp;player_id=0&amp;app_id=58479"
             frameborder="0" allow="autoplay; fullscreen; picture-in-picture; clipboard-write; encrypted-media"
              style="width:80vw;height:60vh;" title="Lesson 01 Creator Bee.mp4"></iframe>
               <script src="https://player.vimeo.com/api/player.js"></script>''')
        if landing == 9 and video == 2:
            return Markup('''<iframe src="https://player.vimeo.com/video/1067425388?badge=0&amp;autopause=0&amp;player_id=0&amp;app_id=58479"
             frameborder="0" allow="autoplay; fullscreen; picture-in-picture; clipboard-write; encrypted-media"
              style="width:80vw;height:60vh;" title="Lesson 02 - Types of Lead Generation"></iframe>
                      <script src="https://player.vimeo.com/api/player.js"></script>''')
        if landing == 6 and video == 1:
            return Markup('''<iframe src="https://player.vimeo.com/video/1067332188?badge=0&amp;autopause=0&amp;player_id=0&amp;app_id=58479"
             frameborder="0" allow="autoplay; fullscreen; picture-in-picture; clipboard-write; encrypted-media"
              style="width:80vw;height:60vh;"" title="L1"></iframe>
                      <script src="https://player.vimeo.com/api/player.js"></script>''')
        if landing == 6 and video == 2:
            return Markup('''<iframe src="https://player.vimeo.com/video/1067327437?badge=0&amp;autopause=0&amp;player_id=0&amp;app_id=58479"
             frameborder="0" allow="autoplay; fullscreen; picture-in-picture; clipboard-write; encrypted-media"
              style="width:80vw;height:60vh;" title="L2"></iframe>
                      <script src="https://player.vimeo.com/api/player.js"></script>''')
        if landing == 8 and video == 1:
            return Markup('''<iframe src="https://player.vimeo.com/video/1068787340?badge=0&amp;autopause=0&amp;player_id=0&amp;app_id=58479"
             frameborder="0" allow="autoplay; fullscreen; picture-in-picture; clipboard-write; encrypted-media"
              style="width:80vw;height:60vh;" title="Module-1.1"></iframe>
                      <script src="https://player.vimeo.com/api/player.js"></script>''')
        if landing == 8 and video == 2:
            return Markup('''<iframe src="https://player.vimeo.com/video/1068777332?badge=0&amp;autopause=0&amp;player_id=0&amp;app_id=58479"
             frameborder="0" allow="autoplay; fullscreen; picture-in-picture; clipboard-write; encrypted-media"
              style="width:80vw;height:60vh;" title="Module 1.2"></iframe>
                      <script src="https://player.vimeo.com/api/player.js"></script>''')
