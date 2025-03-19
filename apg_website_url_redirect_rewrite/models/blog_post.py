from odoo import models, fields

class BlogPost(models.Model):
    _inherit = "blog.post"

    destination_url = fields.Char(string="Destination URL", help="URL to redirect the user when clicking on the blog post.")

    def _compute_website_url(self):
        """Override default Odoo method to use `destination_url` instead of `website_url`."""
        super()._compute_website_url()
        for blog_post in self:
            if blog_post.destination_url:
                blog_post.website_url = blog_post.destination_url  # Override only for redirection


