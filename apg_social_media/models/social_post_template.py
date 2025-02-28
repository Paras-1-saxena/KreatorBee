# -*- coding: utf-8 -*-
import re
import json

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.osv import expression
from odoo.tools import format_datetime


class SocialPostTemplate(models.Model):
    """
    Models the abstraction of social post content.
    It can generate multiple 'social.post' records to be sent on social medias

    This model contains all information related to the post content (message, images) but
    also some common methods. They can be used to prepare a social post without creating
    one (that can be useful in other application, like `social_event` e.g.).

    'social.post.template' is therefore a template model used to generate `social.post`.
    It is inherited by `social.post` to extract common fields declaration and post
    management methods.
    """
    _name = 'apg.social.post.template'
    _description = 'Social Post Template'
    _rec_names_search = ['display_message']

    @api.model 
    def default_get(self, fields):
        result = super(SocialPostTemplate, self).default_get(fields)
        # When entering a text in a reference field, we should take the entered
        # text  and use it to initialize the message. As the reference widget might
        # share different models (and so not always write on "message" but sometimes on
        # "name" or whatever) it will not update the "create_name_field" parameter when
        # the model changes and we need this piece of code to set correctly the message
        if not result.get('message') and self.env.context.get('default_name'):
            result['message'] = self.env.context.get('default_name')
        return result

    # Content
    post_title = fields.Text("Title")
    message = fields.Text("Message")
    video_url = fields.Char(string='Video Url')
    image_ids = fields.Many2many(
        'ir.attachment', string='Attach Images',
        help="Will attach images to your posts (if the social media supports it).")
    display_message = fields.Char(string='Display Message')
    # JSON array capturing the URLs of the images to make it easy to display them in the kanban view
    image_urls = fields.Text(
        'Images URLs', compute='_compute_image_urls')
    is_split_per_media = fields.Boolean('Split Per Network')
    media_count = fields.Integer('Media Count', compute='_compute_media_count')
    # Account management
    # account_ids = fields.Many2many('social.account', string='Social Accounts',
    #                                help="The accounts on which this post will be published.",
    #                                compute='_compute_account_ids', store=True, readonly=False)
    # has_active_accounts = fields.Boolean('Are Accounts Available?', compute='_compute_has_active_accounts')
