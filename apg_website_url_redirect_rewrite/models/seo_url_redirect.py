from odoo import models, fields

class SeoUrlRedirect(models.Model):
    _name = "seo.url.redirect"
    _description = "SEO URL Redirect"

    website_url = fields.Char(string="Website URL", required=True)
    destination_url = fields.Char(string="Destination URL", required=True)