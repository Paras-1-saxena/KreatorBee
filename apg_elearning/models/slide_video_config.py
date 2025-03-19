from odoo import models, fields

class SlideVideoConfig(models.Model):
    _name = 'slide.video.config'
    _description = 'Slide Video Configuration'

    name = fields.Char(string="Page Name", required=True)
    page_key = fields.Selection([
        ('nmy_courses', 'My Courses'),
        ('sales_page', 'Sales Page'),
        ('creator_lead', 'Creator Lead'),
        ('creator_nkyc', 'Creator NKYC'),
        ('creator_link', 'Creator Links'),
        ('creator_leaderboard', 'Creator Leaderboard'),
        ('creator_offers', 'Creator Offers'),
        ('connect_partner', 'Creator Connect Partner'),
        ('master_course_detail', 'Master Course Detail'),
        ('master_course_standard', 'Master Course Standard'),
        ('master_terms', 'Master Terms'),
        ('master_welcome', 'Master Welcome'),
        ('creator_landing_page', 'Creator Landing Page'),
        ('creator_edit_landing_page', 'Creator Edit Landing Page'),
        ('customer_page', 'Customer Courses'),
        ('customer__recommended_page', 'Customer Recommended Course'),
        ('partner_income', 'Partner Income'),
        ('partner_lead', 'Partner Lead'),
        ('bee_partner', 'Partner Nkyc'),
        ('partner_links', 'Partner Links'),
        ('partner_leaderboard', 'Partner Leaderboard'),
        ('partner_my_product', 'Partner My Product'),
        ('partner_choose_product', 'Partner Choose Product'),
        ('partner_choose_product_detail', 'Partner Choose Product Detail'),
        ('partner_promotional_material', 'Partner Promotional Material'),
        ('partner_promotional_material_detail', 'Partner Promotional Material Detail'),
        ('partner_offers', 'Partner Offers'),
        ('partner_target', 'Partner Target'),
        ('partner_training', 'Partner Training'),
        ('partner_courses', 'Partner Courses'),
    ], string="Page Identifier", required=True, unique=True)
    video_url = fields.Char(string="YouTube Video URL", required=True)
