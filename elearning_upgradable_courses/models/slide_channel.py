from odoo import api, fields, models, exceptions, _


class SlideChannel(models.Model):
    _inherit = 'slide.channel'

    is_upgradable = fields.Boolean(string="Is Upgradable Course?")
    upgrade_stage_ids = fields.One2many(comodel_name='slide.channel.upgrade.stage', inverse_name='channel_id')
    upgrade_option_ids = fields.One2many(comodel_name='slide.channel.upgrade.option', inverse_name='channel_id')
    user_ids = fields.Many2many('res.users', string='Users')
    not_display = fields.Boolean(string='Not Show')
    is_paid = fields.Boolean(string='Is Paid ?')
    partner_redirect = fields.Boolean(string='Redirect to Partner ?',
                                      help="Purchasing this course will redirect to creating a partner account instead of Customer")
    referral_coupon_id = fields.Many2one(comodel_name='product.product', string='Referral Coupon', help="if applicable a Discount Code is automatically Applicable to the Order Line")
    is_mandate = fields.Boolean(string='Is Mandate', help="User Needs to buy this course to Start the Affiliate Journey")
    brochure = fields.Binary(string='Brochure', help="Brochure")
    brochure_name = fields.Char(string='Brochure Name', help="Brochure Name")

class SlideSlide(models.Model):
    _inherit = 'slide.slide'
    upgrade_stage_id = fields.Many2many(comodel_name='slide.channel.upgrade.stage', string='Stage')


class SlideChannelUpgradeStage(models.Model):
    _name = 'slide.channel.upgrade.stage'
    _description = "Slide channel Upgrade Stage"

    name = fields.Char(string="Options")
    product_ids = fields.Many2many(comodel_name='product.product', string='Connected Products')
    channel_id = fields.Many2one(comodel_name='slide.channel', string='Channel')
    image_banner = fields.Image("Image")
    landing_page_record_id = fields.Many2one(comodel_name='landing.page.record', string='Landing Page')


class SlideChannelUpgradeOption(models.Model):
    _name = 'slide.channel.upgrade.option'
    _description = "Slide Channel Upgrade Options"

    name = fields.Char(string="Options")
    product_id = fields.Many2one(comodel_name='product.product')
    from_stage = fields.Many2one(comodel_name='slide.channel.upgrade.stage')
    to_statge = fields.Many2one(comodel_name='slide.channel.upgrade.stage')
    channel_id = fields.Many2one(comodel_name='slide.channel', string='Channel')
