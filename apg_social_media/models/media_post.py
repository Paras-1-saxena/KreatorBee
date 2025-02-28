# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import json
import threading

from collections import defaultdict
from markupsafe import Markup
from datetime import datetime,date
from odoo import _, api, fields, models
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools import format_list


class SocialPost(models.Model):
    """ A social.post represents a post that will be published on multiple social.accounts at once.
    It doesn't do anything on its own except storing the global post configuration (message, images, ...).

    This model inherits from `social.post.template` which contains the common part of both
    (all fields related to the post content like the message, the images...). So we do not
    duplicate the code by inheriting from it. We can generate a `social.post` from a
    `social.post.template` with `action_generate_post`.

    When posted, it actually creates several instances of social.live.posts (one per social.account)
    that will publish their content through the third party API of the social.account. """

    _name = 'apg.social.post'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'apg.social.post.template']#, 'utm.source.mixin'
    _description = 'Social Post'
    _order = 'message'

    state = fields.Selection([
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('posting', 'Posting'),
        ('posted', 'Posted')],
        string='Status', default='draft', readonly=True, required=True,
        help="The post is considered as 'Posted' when all its sub-posts (one per social account) are either 'Failed' or 'Posted'")
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 domain=lambda self: [('id', 'in', self.env.companies.ids)])
    #UTM
    utm_campaign_id = fields.Many2one('utm.campaign', domain="[('is_auto_campaign', '=', False)]",
        string="Campaign", ondelete="set null")
    post_method = fields.Selection([
        ('now', 'Send now'),
        ('scheduled', 'Schedule later')], string="When", default='now', required=True,
        help="Publish your post immediately or schedule it at a later time.")
    
    partner_type = fields.Selection([
        ('company', 'Company'),
        ('creator', 'Creator'),
        ('partner', 'Partner'),
        ('customer', 'Customer')], string="Post Type")
    scheduled_date = fields.Datetime('Scheduled Date')
    published_date = fields.Datetime('Published Date', readonly=True,
        help="When the global post was published. The actual sub-posts published dates may be different depending on the media.")
    comment_ids = fields.One2many('apg.post.comment', 'post_id')
    comment_count = fields.Integer(compute="_compute_comment_count")
    like_ids = fields.One2many('apg.post.like', 'post_id')
    like_count = fields.Integer(compute="_compute_like_count")

    def _compute_comment_count(self):
        for line in self:
            line.comment_count = len(line.comment_ids)

    def _compute_like_count(self):
        for line in self:
            line.like_count = len(line.like_ids)


    def action_view_comments(self):
        self.ensure_one()
        action = self.env['ir.actions.actions']._for_xml_id('apg_social_media.action_apg_post_comment')
        action['domain'] = [('id','in', self.comment_ids.ids)]
        return action

    def action_view_likes(self):
        pass
    # @api.depends(lambda self: [f'post_id.{field}' for field in self.env['social.post']._images_fields().values()])
    # def _compute_image_ids(self):
    #     images_field_per_media = self.env['social.post']._images_fields()
    #     for live_post in self:
    #         image_field = images_field_per_media.get(live_post.media_type)
    #         live_post.image_ids = live_post.post_id[image_field] if image_field else False

class SocialPostComment(models.Model):
    _name = 'apg.post.comment'
    _description = 'Social Post Comment'

    post_id = fields.Many2one('apg.social.post', string="Post", required=True)
    message = fields.Text("Message")
    parent_id = fields.Many2one('apg.post.comment', string="Parent Comment", index=True, ondelete='cascade')
    child_ids = fields.One2many('apg.post.comment', 'parent_id', string="Replies")
    user_id = fields.Many2one('res.users', string="User", default=lambda self: self.env.user)
    date_posted = fields.Datetime("Posted On", default=fields.Datetime.now)

    def get_nested_comments(self):
        """Recursively fetch nested comments with parent_id"""
        result = []
        for comment in self:
            result.append({
                'id': comment.id,
                'message': comment.message,
                'user': comment.user_id.name,
                'date': comment.date_posted.strftime("%Y-%m-%d %H:%M"),
                'parent_id': comment.parent_id.id if comment.parent_id else None,  # Add parent_id
                'replies': comment.child_ids.get_nested_comments() if comment.child_ids else []
            })
        return result

class SocialPostLike(models.Model):
    _name = 'apg.post.like'
    _description = 'Social Post Like'

    post_id = fields.Many2one('apg.social.post', string="Post")
