# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime, timedelta
import json

from odoo import api, models, fields
from odoo.tools.misc import format_date, _format_time_ago


class SocialStreamPost(models.Model):
	_name = 'apg.social.stream.post'
    _description = 'Social Stream Post'

    message = fields.Text("Message")
    author_name = fields.Char('Author Name')
    published_date = fields.Datetime('Published date', help="The post published date based on third party information.")
    company_id = fields.Many2one('res.company', 'Company')
    
