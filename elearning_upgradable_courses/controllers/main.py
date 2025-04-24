from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo import http, _
from odoo.exceptions import AccessDenied, AccessError, UserError, ValidationError
from odoo.http import request, route
from odoo.tools.json import scriptsafe as json_scriptsafe
import logging

_logger = logging.getLogger(__name__)

class WebsiteSaleCustom(WebsiteSale):

    @route(['/shop/cart/update'], type='http', auth="public", methods=['POST'], website=True)
    def cart_update(
            self, product_id, add_qty=1, set_qty=0, product_custom_attribute_values=None,
            no_variant_attribute_value_ids=None, **kwargs
    ):
        """This route is called when adding a product to cart (no options)."""
        sale_order = request.website.sale_get_order(force_create=True)
        if sale_order.state != 'draft':
            request.session['sale_order_id'] = None
            sale_order = request.website.sale_get_order(force_create=True)

        if product_custom_attribute_values:
            product_custom_attribute_values = json_scriptsafe.loads(product_custom_attribute_values)

        # old API, will be dropped soon with product configurator refactorings
        no_variant_attribute_values = kwargs.pop('no_variant_attribute_values', None)
        if no_variant_attribute_values and no_variant_attribute_value_ids is None:
            no_variants_attribute_values_data = json_scriptsafe.loads(no_variant_attribute_values)
            no_variant_attribute_value_ids = [
                int(ptav_data['value']) for ptav_data in no_variants_attribute_values_data
            ]

        # user = request.env.user
        # public_user_id = request.website.user_id.id  # Get the public user ID
        # if user.id == public_user_id:  # if current user is public user
        #     # Store the current product URL to return after signup
        #     return request.redirect("/shop/cart")

        sale_order.order_line.unlink()
        request.session['coupon_status'] = ''
        course = request.env['slide.channel'].search([('product_id', '=', int(product_id))])
        coupon_id = course.referral_coupon_id
        if coupon_id and request.session.get('referral_partner') and (course.id not in request.env.user.partner_id.slide_channel_ids.ids):
            sale_order._cart_update(
                product_id=coupon_id.id,
                add_qty=add_qty,
                set_qty=set_qty,
                product_custom_attribute_values=product_custom_attribute_values,
                no_variant_attribute_value_ids=no_variant_attribute_value_ids,
                **kwargs
            )
        if kwargs.get('option'):
            stage_id = course.upgrade_stage_ids.filtered(lambda us: us.name == kwargs.get('option'))
            partner_course_ids = request.env.user.partner_id.slide_channel_ids.product_id.ids
            products_to_add = [sc.id for sc in stage_id.product_ids if sc.id not in partner_course_ids]

            if products_to_add:
                for product in products_to_add:
                    sale_order._cart_update(
                        product_id=product,
                        add_qty=add_qty,
                        set_qty=set_qty,
                        product_custom_attribute_values=product_custom_attribute_values,
                        no_variant_attribute_value_ids=no_variant_attribute_value_ids,
                        **kwargs
                    )
        else:
            sale_order._cart_update(
                product_id=int(product_id),
                add_qty=add_qty,
                set_qty=set_qty,
                product_custom_attribute_values=product_custom_attribute_values,
                no_variant_attribute_value_ids=no_variant_attribute_value_ids,
                **kwargs
            )

        request.session['website_sale_cart_quantity'] = sale_order.cart_quantity

        return request.redirect("/shop/cart")